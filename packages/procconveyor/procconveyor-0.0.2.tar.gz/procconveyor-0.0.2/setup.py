from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="procconveyor",
    version="0.0.2",
    author="aver",
    author_email="a.v.e.r@mail.ru",
    description="A package to make conveyor of parallel data processing",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/aver007/proc-conveyor/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
)
