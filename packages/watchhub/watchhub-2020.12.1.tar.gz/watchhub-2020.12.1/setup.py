from setuptools import setup
import os

with open("README.rst") as f:
    readme = f.read()


def get_version():
    about = {}
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "watchhub/__version__.py")) as f:
        exec(f.read(), about)
    return about["__version__"]


setup(
    name="watchhub",
    version=get_version(),
    description="Communicate with the watchub API to find streams from IMDB IDs.",
    long_description=readme,
    keywords=["watchhub"],
    url="https://github.com/imduffy15/python-watchhub/",
    license="MIT",
    author="Ian Duffy",
    author_email="ian@ianduffy.ie",
    packages=["watchhub"],
    install_requires=["aiohttp>=0.4.0"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    test_suite="tests",
)
