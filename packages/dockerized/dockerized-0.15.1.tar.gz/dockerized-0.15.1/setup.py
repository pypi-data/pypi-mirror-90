from setuptools import setup, find_packages
import json

with open("README.md", "r") as fh:
    long_description = fh.read()

version = "0.15.1"

setup(
    install_requires=["click==7.1.2", "pyyaml==5.3.1"],
    name="dockerized",
    version=version,
    author="Itamar Ben-Zaken",
    author_email="benzaita@gmail.com",
    description="Seamlessly execute commands in a container",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://benzaita.github.io/dockerized-cli/index.html",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    scripts=["bin/dockerized"],
)
