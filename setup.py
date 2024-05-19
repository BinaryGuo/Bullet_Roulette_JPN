from setuptools import find_packages,setup
from os.path import dirname

with open(f"{dirname(__file__)}/README.md" ,"r",encoding="utf-8") as fh:
    dis = fh.read()

setup(
    name = "sockettoolkit",
    version = "1.0.0",
    author = "GQX",
    author_email = "kill114514251@outlook.com",
    description = "A toolkit that combines many functions of Socket",
    long_description = dis,
    long_description_content_type = "text/markdown",
    url = "https://github.com/BinaryGuo/Socket_Toolkit",
    packages = find_packages(),
    package_data = {
        "sockettoolkit/" : ["*"]
    },
    classifiers = [
        "Intended Audience :: Developer",
        "Development Status :: 4 - Beta",
        "Natural Language :: Chinese (Simplified)?",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8"
    ],
    python_requires = ">=3.8"
)