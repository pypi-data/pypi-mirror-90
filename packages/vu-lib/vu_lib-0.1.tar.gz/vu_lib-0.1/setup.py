from setuptools import setup, find_packages
from vu_lib.version import __version__


def readme():
    with open("README.md") as f:
        README = f.read()
    return README


setup(
    name="vu_lib",
    version=__version__,
    description="PyPi package of the Vrije Universiteit Amsterdam ipy_lib3 module.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/markmelnic/VU-Lib",
    author="Mark Melnic",
    author_email="commerce.markmelnic@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": []},
)
