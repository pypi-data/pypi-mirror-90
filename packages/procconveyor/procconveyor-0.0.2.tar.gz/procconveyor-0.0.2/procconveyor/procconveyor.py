from abc import ABC, abstractmethod
from multiprocessing import Process, Queue, Value, Event
import queue
import ctypes
import time


class MySafeValue:
    """
    Класс безопасного инкремента многопоточной переменной
    """
    def __init__(self, *args, **kwargs):
        self.__multiproc_value = Value(*args, **kwargs)

    @property
    def value(self): 
        return self.__multiproc_value.value

    def safe_increment(self):
        with self.__multiproc_value.get_lock():
            self.__multiproc_value.value += 1


class AbstractProcess(ABC):
    """
    Общее описание класса процесса
    Без создания своих очередей
    """
    def __init__(                  # как в multiprocessing.Process
            self,
            target_proc,           # target - обязательно функция - генератор. В ней основная работа
                                   # target_proc(in_obj, *args, **kwargs) или target_proc(*args, **kwargs)
                                   # в зависимости от того, подаем на вход очередь или нет
            src=None,              # входная очередь (если есть)
            dst=None,              # выходная очередь (если есть)
            args=(),               # аргументы
            kwargs={}              # аргументы
    ):

        self.__received = MySafeValue("L", 0)
        self.__received_bytes = MySafeValue("L", 0)
        self.__transmitted = MySafeValue("L", 0)
        self.__transmitted_bytes = MySafeValue("L", 0)
        self.__stopped = Value(ctypes.c_bool, True)  # from ctypes
        self.__stop_event = Event()

        self.__process = Process(
            target=self._loop,
            args=(
                self.__stop_event,
                self.__stopped,
                self.__received,
                self.__transmitted,
                src,
                dst,
                target_proc,
                tuple(args),
                dict(kwargs)
            )
        )

    @property
    def stopped(self):
        return self.__stopped.value

    @property
    def received(self):
        return self.__received.value

    @property
    def received_bytes(self):
        raise Exception("not implemented yet in __loops")
        # return self.__received_bytes.value

    @property
    def transmitted(self):
        return self.__transmitted.value

    @property
    def transmitted_bytes(self):
        raise Exception("not implemented yet in __loops")
        # return self.__transmitted_bytes.value

    @staticmethod
    @abstractmethod
    def _loop(stop_evt, stopped, received, transmitted, src, dst, target_proc, args, kwargs):
        pass

    def stop(self):
        # Отправляет команду на остановку
        self.__stop_event.set()

    def start(self):
        self.__process.start()
        time.sleep(0.5)  # Даем время процессу запуститься

    def join(self):
        # блокируем поток-хозяин пока внутренний поток не перешел в состояние stopped = True
        while not self.stopped:
            time.sleep(0.5)

    def terminate(self):
        # прерывает процесс не дожидаясь остановки (с потерей данных)
        self.__stopped.value = True
        self.__process.terminate()


class Generator(AbstractProcess):
    """
    Класс генератора данных
    """
    def __init__(self,  target_proc, out_queue_len, args=(), kwargs={}):
        self.__out_queue = Queue(out_queue_len)
        super().__init__(target_proc=target_proc, src=None, dst=self.__out_queue, args=args, kwargs=kwargs)

    @property
    def out_queue(self):
        return self.__out_queue

    @staticmethod
    def _loop(stop_evt, stopped, received, transmitted, src, dst, target_proc, args, kwargs):
        stopped.value = False

        # В генераторе функция-обработчик не должна принимать входной объект
        rez_generator = target_proc(*args, **kwargs)

        for rez in rez_generator:
            # проходим по всем результатам генератора
            while True:
                try:
                    dst.put(rez, block=False)
                except queue.Full:
                    time.sleep(0.1)  # todo !!! Проверить
                    continue
                else:
                    # если не было except то выходим из цикла while True
                    break

            transmitted.safe_increment()
            if stop_evt.is_set():
                # Реакция на остановку только после обработки текущего полученного объекта
                # в генераторе можно прерывать вывод по событию
                break

        # dst.close()  # todo !!! А нужно ли это ??
        stopped.value = True


class Consumer(AbstractProcess):
    """
    Класс потребителя данных
    """
    def __init__(self, target_proc, src, args=(), kwargs={}):
        self.__src_queue = src
        super().__init__(target_proc=target_proc, src=self.__src_queue, dst=None, args=args, kwargs=kwargs)

    @staticmethod
    def _loop(stop_evt, stopped, received, transmitted, src, dst, target_proc, args, kwargs):
        stopped.value = False
        while not stop_evt.is_set():
            # Если задан источник юданных то берем из него очередной объект
            try:
                in_obj = src.get(block=False)
            except queue.Empty:
                # если очередь пустая, ждем немного и опять в цикл
                time.sleep(0.1)
                continue

            received.safe_increment()

            target_proc(in_obj, *args, **kwargs)  # Обрабатываем объект из очереди процедурой

        stopped.value = True


class Handler(AbstractProcess):
    """
    Класс единственного обработчика данных
    Очереди не создает
    """
    @staticmethod
    def _loop(stop_evt, stopped, received, transmitted, src, dst, target_proc, args, kwargs):
        stopped.value = False
        while not stop_evt.is_set():
            # Берем из источника очередной объект
            try:
                in_obj = src.get(block=False)
            except queue.Empty:
                # если очередь пустая, ждем немного и опять в цикл
                time.sleep(0.1)
                continue

            received.safe_increment()

            rez_generator = target_proc(in_obj, *args, **kwargs)

            for rez in rez_generator:
                # проходим по всем результатам генератора, отправляем их в выходную очередь
                dst.put(rez, block=True)  # Здесь будем ждать до победного а не как в Generator._loop

                transmitted.safe_increment()
                # todo !! Рассмотреть случай большого входного объекта,
                #  при его обработке остановки по stop_evt.is_set() не будет. Придется ждать пока не обработается.
                #  Может сюда вставить if stop_evt.is_set() ???

        stopped.value = True


class HandlersPool:
    """
    Пул обработчиков. Для всех процессоыв-обработчиков создает общую выходную очередь
    """
    def __init__(self, target_proc, num_handlers, src, out_queue_len, args=(), kwargs={}):
        self.__stop_event = Event()
        self.__received = 0
        self.__transmitted = 0
        self.__stopped = True

        self.__proc_list = []
        self.__src_queue = src
        self.__out_queue = Queue(out_queue_len)

        for i in range(num_handlers):
            proc = Handler(target_proc=target_proc, src=src, dst=self.__out_queue,  args=args, kwargs=kwargs)

            self.__proc_list.append(proc)

    @property
    def out_queue(self):
        return self.__out_queue

    @property
    def received(self):
        return sum([proc.received for proc in self.__proc_list])

    @property
    def transmitted(self):
        return sum([proc.transmitted for proc in self.__proc_list])

    @property
    def stopped(self):
        for process in self.__proc_list:
            if not process.stopped:
                return False  # если хоть один процесс не остановлен то возвращаем False

        return True  # Возвращаем True только если все завершены

    def start(self):
        for process in self.__proc_list:
            process.start()

    def terminate(self):
        for process in self.__proc_list:
            process.terminate()

    def stop(self):
        for process in self.__proc_list:
            process.stop()

    def join(self):
        # делаем join для всех процессов-обработчиков
        for process in self.__proc_list:
            process.join()


class Watchdog:
    """
    Класс - отслеживатель состояния частей конвеера
    """
    def __init__(self, gen_obj, handlers_obj, cons_obj):
        assert type(gen_obj) == Generator
        assert type(handlers_obj) == HandlersPool
        assert type(cons_obj) == Consumer

        self.__gen_obj = gen_obj
        self.__handlers_obj = handlers_obj
        self.__cons_obj = cons_obj

    @staticmethod
    def __get_data(obj):
        data = dict()
        data["working"] = not obj.stopped
        data["received"] = obj.received
        data["transmitted"] = obj.transmitted

        return data

    def __get_statistic_once(self):
        stat = dict()

        stat["GENERATOR"] = self.__get_data(self.__gen_obj)
        stat["GENERATOR"]["out_queue_size"] = self.__gen_obj.out_queue.qsize()

        stat["HANDLERS"] = self.__get_data(self.__handlers_obj)
        stat["HANDLERS"]["out_queue_size"] = self.__handlers_obj.out_queue.qsize()

        stat["CONSUMER"] = self.__get_data(self.__cons_obj)

        return stat

    def start(self):
        print("Starting consumer")
        self.__cons_obj.start()

        print("Starting handlers")
        self.__handlers_obj.start()

        print("Starting generators")
        self.__gen_obj.start()
        time.sleep(0.5)

        print("All started")

    def watch(self):
        # Пока конвеер работает он выдает статистику по своим компонентам
        while (not self.__gen_obj.stopped) or (self.__cons_obj.received < self.__handlers_obj.transmitted):
            yield self.__get_statistic_once()  # Каждую итерацию возвращает статистику работы

        # после чего-останавливает
        self.__handlers_obj.stop()
        self.__cons_obj.stop()

    def start_and_watch(self):
        self.start()
        return self.watch()

    def terminate_all(self):
        self.__gen_obj.terminate()
        self.__handlers_obj.terminate()
        self.__cons_obj.terminate()

    def stop(self):
        self.__gen_obj.stop()
        self.__handlers_obj.stop()
        self.__cons_obj.stop()
