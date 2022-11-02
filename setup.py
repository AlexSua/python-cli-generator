import os
from setuptools import PEP420PackageFinder, setup
find_packages = PEP420PackageFinder.find

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
    
setup(
    name="python-cli-generator",
    version="0.1",
    author="Alejandro Suárez",
    author_email="alejandrosuarez.eu@gmail.com",
    description=("A library that allows a rapid creation of a CLI by automatically reading the attributes and parameters inside a class and generating its corresponding Command Line Interface."),
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    license="MIT",
    include_package_data=True,
    keywords="python cli generator class output parsing",
    url="https://github.com/AlexSua/python-cli-generator",
    packages=find_packages(
        exclude=("build*", "dist*", "docs*", "tests*", "coverage*", "*.egg-info")
    ),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires=">=3.6"
)