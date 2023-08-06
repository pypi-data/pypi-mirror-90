from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
lib = path.join(here, "lib")

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tsetmc-api",
    version="4.3.1",
    python_requires=">=3.7",
    install_requires=[
        "requests",
        "beautifulsoup4",
        "lxml",
        "python-dateutil",
        "jdatetime",
        "schedule",
    ],
    extras_require={
        "dev": []
    },
    package_dir={"": "lib"},
    packages=find_packages(where=lib, exclude=["scripts"]),
    entry_points={
        "console_scripts": ["tsetmc-loader = tsetmc_api.bin.tsetmc_loader:main"]
    },
    url="https://github.com/mahs4d/tsetmc-api",
    license="MIT",
    author="Mahdi Sadeghi",
    author_email="mail2mahsad@gmail.com",
    description="getting data from tehran stock exchange",
)
