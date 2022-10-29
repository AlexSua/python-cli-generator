<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<div align="center">

<h1 align="center">python-cli-generator</h2>

  <p align="center">
    A Python library that automatically generates a CLI given a class, a function or a list of classes.
    <br />
    <br />
 <div align="center">


[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



</div>
    <a href="https://github.com/AlexSua/python-cli-generator/issues">Report Bug</a>
    ·
    <a href="https://github.com/AlexSua/python-cli-generator/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <!-- <li><a href="#install-required-python-dependencies">Install required python dependencies</a></li> -->
      </ul>
    </li>
    <!-- <li> -->
	<!-- <a href="#usage">Usage</a>
	<ul>
        <li><a href="#parameters">Parameters</a></li>
        <li><a href="#get-youtube-playlist/element">Options</a></li>
      </ul>
	</li>
    <li><a href="#contact">Contact</a></li> -->
  </ol>
</details>
</br>

<!-- ABOUT THE PROJECT -->
## About The Project
This library allows a rapid creation of a CLI by automatically reading the attributes, methods and function parameters inside a class and generating its corresponding Command Line Interface through the built-in argparse library. The module contains an optional output processor able to print the result of the executed command in different formats.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
The necessary steps to get the library working on your environment.

</br>

### Prerequisites

Before using the application you need to have installed [python](https://www.python.org/). You can get instructions on how to install it by following the link shown before.

</br>


### Install the library

```bash
pip3 install git+https://github.com/AlexSua/python-cli-generator.git
```
> In the future the library will be published in PyPI. For now you can use the command above. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

```Python
from datetime import datetime
from typing import List
from python_cli_generator import Cli


class ParameterTest:
    """Parameter test class
    parameter_test_required (str): required parameter parameter_test_attr1
    parameter_test_optional (str): optional parameter parameter_test_attr2.

    """
    parameter_test_attr1: str
    parameter_test_attr2: str = ""


class Test:
    """Test class
    test_attr_1 (str): optional parameter test_attr_1
    test_attr_2 (str): optional parameter test_attr_2.
    """
    test_attr_1: str
    test_attr_2: str

    def __init__(self):
        self.test_attr_1 = "test1"
        self.test_attr_2 = "test2"

    def t_method(self, test3, test4="test4", **test5: ParameterTest):
        """A method1 example

        Args:
            test3 (str): required parameter test3
            test4 (str, optional): optional parameter test4. Defaults to "test4".
        """
        return [
            {"parameter_name": "test_1", "parameter_value": self.test_attr_1},
            {"parameter_name": "test_2", "parameter_value": self.test_attr_2},
            {"parameter_name": "test3", "parameter_value": test3},
            {"parameter_name": "test4", "parameter_value": test4},
            {"parameter_name": "test5", "parameter_value": test5},
        ]


class Test1:
    """test1 description
    t2_attr_1 (str): optional parameter test1
    t2_attr_2 (int): optional parameter test2.
    t2_attr_3 (datatime): optional parameter test2.
    t2_attr_4 (list): optional parameter test2.
    """
    t1_attr_1: str
    t1_attr_2: int
    t1_attr_3: datetime
    t1_attr4: list[str] = []

    def _default(self, param1: str):
        print(param1)


class Test2:
    """test2 description
    t2_attr_1 (str): optional parameter test1
    t2_attr_2 (int): optional parameter test2.
    t2_attr_3 (datatime): optional parameter test2.
    t2_attr_4 (list): optional parameter test2.
    """
    t2_attr_1: str
    t2_attr_2: int
    t2_attr_3: datetime
    t2_attr_4: List[str] = []

    def t2_method1(self, **test1: Test1):
        print(test1)

    def t2_method2(self, **test1: Test1):
        print(test1)


class Test3:
    """test3 description
    t3_attr_1 (str): optional parameter test1
    t3_attr_2 (int): optional parameter test2.
    t3_attr_3 (datatime): optional parameter test2.
    t3_attr_4 (list): optional parameter test2.
    """
    t3_attr_1: str
    t3_attr_2: int
    t3_attr_3: datetime
    t3_attr_4: List[str] = []

    def t3_method1(self, test1):
        print(test1)

    def t3_method2(self, test1):
        print(test1)

    def t3_method2(self, test1):
        print(test1)

def test(x: str):
    """function that does something

    Args:
        x (str): is an x parameter
    """    
    print(x)



options = {
    "builtin_output_processing": True,
    "builtin_format": "json",
    "builtin_search_argument": True,
    "builtin_full_help_argument": False,
    "builtin_verbose_argument": True,
}
generate_arguments_options = {
    "builtin_output_processing": True,
    "builtin_format": "json",
    "builtin_search_argument": True,
    "builtin_full_help_argument": False,
    "builtin_verbose_argument": True,
    "builtin_class_attributes_generator": True,
    "builtin_class_functions_generator": False
}

# Create CLI class with the selected configuratio.
cli = Cli(**options)

# Generate CLI arguments for Test class
cli.generate_arguments(Test())

# Geberate CLI arguments for the following dictionary.
cli.generate_arguments({
    "subcommand1": (Test1()),
    "subcommand2": [test, (Test2(), generate_arguments_options)],
    "subcommand3": (Test3()),
})

# Obtain the arguments that are introduced in the cli as a dictionary.
args = cli.parse()

# Execute the selected command in the cli. 
# If no arguments are introduced the function 
# you select in the CLI will be executed with 
# the arguments you have introduced in the CLI.
cli.execute_command()

```

</br>

### Options




<!-- ### Execute examples

To get the script working you need to follow the steps shown below.

1. Clone the repo

   ```bash
   git clone https://github.com/AlexSua/python-cli-generator.git
   ```

2. Enter the project directory:

   ```bash
   cd python-cli-generator
   ```

3. Install python dependencies by executing the following command.

   ```bash
   pip3 install -r requirements.txt
   ```

With the steps mentioned above, you should be ready to use the script.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
You can check the documentation of the script by typing:

   ```bash
   python3 python-cli-generator.py
   ```

### Parameters


### Options -->

## Contact

Project Link: [https://github.com/AlexSua/python-cli-generator](https://github.com/AlexSua/python-cli-generator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[issues-shield]: https://img.shields.io/github/issues/AlexSua/python-cli-generator?style=flat-square
[issues-url]: https://github.com/AlexSua/python-cli-generator/issues

[license-shield]: https://img.shields.io/github/license/AlexSua/python-cli-generator?style=flat-square
[license-url]: https://github.com/AlexSua/python-cli-generator/blob/main/LICENSE.txt