from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name = "qwertywertyerty12",
    version = "1.0.0",
    description = "A discrete event simulator",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/darrenkhlim/qwertywertyerty12",
    author = "NUS",
    author_email = "e0426117@u.nus.edu",
    license = "NUS",
    classsifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    packages = ["qwertywertyerty123", "qwertywertyerty123.log", "qwertywertyerty123.application", "qwertywertyerty123.demos"],
    include_package_data = True,
)

