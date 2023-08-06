# Python script for testing procconveyor
# one more line
import time
from procconveyor.procconveyor import Generator, HandlersPool, Watchdog


def main_proc_multiple_10(ll):
    """
    Пример процедуры-генератора
    Args:
        ll (int): num of generated objects
    Returns:
        генератор объектов
    """
    for x in range(ll):
        yield (x*10, "1" * 10000000)


def main_proc_handler(obj, prefix):
    """
    Пример процедуры-обработчика
    Args:
        obj: Объект для обработки (извлекается из очереди)
        prefix: доп. аргумент
    Returns:
        генератор результатов обработки входного объекта
    """
    obj, data = obj
    result = [prefix + '_1_' + str(obj), prefix + '_2_' + str(obj)]
    for r in result:
        yield r, data


def main_proc_consumer(obj, dobavka):
    """
    Пример процедуры-потребителя
    Args:
        obj: Объект для получения потребителем (извлекается из очереди)
        dobavka: доп. аргумент
    Returns:
        None
    """
    obj, data = obj
    str1 = (obj + dobavka + "consumer_pervaya")
    str2 = (obj + dobavka + "consumer_vtoraya")
    with open('out\\'+str1, 'w') as out1:
        out1.write(data)
    with open('out\\'+str2, 'w') as out1:
        out1.write('2'+data)


if __name__ == "__main__":
    gen = Generator(target_proc=main_proc_multiple_10, out_queue_len=30, args=(100,))
    handlers = HandlersPool(target_proc=main_proc_handler,
                            num_handlers=4,
                            src=gen.out_queue,
                            out_queue_len=200,
                            args=('_pref_',)
                            )
    consumer = Consumer(target_proc=main_proc_consumer, src=handlers.out_queue, args=('_abc_',))

    for statistics in Watchdog(gen, handlers, consumer).start_and_watch():
        print("(gen {}, {}, {})\t(handlers {}, {}, {}, {})\t(cons {}, {})".format(
            statistics["GENERATOR"]["working"],
            statistics["GENERATOR"]["transmitted"],
            statistics["GENERATOR"]["out_queue_size"],

            statistics["HANDLERS"]["working"],
            statistics["HANDLERS"]["received"],
            statistics["HANDLERS"]["transmitted"],
            statistics["HANDLERS"]["out_queue_size"],

            statistics["CONSUMER"]["working"],
            statistics["CONSUMER"]["received"],
                          )
        )
        time.sleep(1)
