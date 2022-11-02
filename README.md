<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<div align="center">

<h1 align="center">python-cli-generator</h1>

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
      </ul>
    </li>
    <li>
	<a href="#usage">Usage</a>
	<ul>
        <li><a href="#import-the-library"> Import the library</a></li>
        <li><a href="#create-input-classes">Create input classes</a></li>
        <li><a href="#generate-cli">Generate CLI</a></li>
        <li><a href="#cli-results">Cli results</a></li>
      </ul>
	</li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>
</br>

## About The Project
This library allows a rapid creation of a CLI by automatically reading the attributes, methods and function parameters inside a class and generating its corresponding Command Line Interface through the built-in argparse library. The module contains an optional output processor able to print the result of the executed command in different formats.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
The necessary steps to get the library working on your environment.


### Prerequisites

Before using the application you need to have installed [python](https://www.python.org/). You can get instructions on how to install it by following the link shown before.



### Install the library

```bash
pip3 install git+https://github.com/AlexSua/python-cli-generator.git
```
> In the future the library will be published in PyPI. For now you can use the command above. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

### Import the library
Import the controller class "Cli" that contains the main functionality for initializing the generation process.

```Python
from python_cli_generator import Cli
```


### Create input classes
Create the classes the generator will use to generate the Command line interface.
> Notice that comments are as well parsed and automatically added to the CLI.
```Python
class ParameterTest:
    """Parameter test class
    parameter_test_required (str): optional parameter parameter_test_attr1
    parameter_test_optional (str): optional parameter parameter_test_attr2.

    """
    #If it doesn't have default value is not generated.
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


class Test5:
    def __init__(self,attr_construct_t5:str) -> None:
        """
        Args:
            attr_construct_t5 (str): This attribute is introduced in the constructor of Test5
        """        
        self.attr_construct_t5 = attr_construct_t5

class Test4:
    def __init__(self,attr_construct_t4:str, attr_t5:Test5) -> None:
        """
        Args:
            attr_construct_t4 (str): This attribute is introduced in the constructor of Test4
        """        
        self.attr_construct_t4 = attr_construct_t4
        self.attr_t5 = attr_t5


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

    def t3_method1(self, test1:Test4):
        """Method 1 for subcommand3. This method contains an object as parameter.

        Args:
            test1 (Test4): Parameter as a class.

        """        
        return {"test1":test1.attr_t5.attr_construct_t5}

    def t3_method2(self, test1:datetime):
        """Method 2 for subcommand3.

        Args:
            test1 (datetime): A datetime
        """        
        print(test1)

    def t3_method3(self, test1):
        """Method 3 for subcommand3

        Args:
            test1 (test1): attr1
        """        
        print(test1)

def test(x: str):
    """
    Args:
        x (str): is an x parameter
    """    
    print(x)

```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Generate CLI
The following code shows how to generate the CLI given the classes created above.

```python
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
    "builtin_full_help_argument": True,
    "builtin_verbose_argument": True,
    "builtin_class_attributes_generator": True,
    "builtin_class_functions_generator": False
}

# Create CLI class with the selected configuration.
cli = Cli(**options)

# Generate CLI arguments for Test class
cli.generate_arguments(Test())

# Generate CLI arguments for the following dictionary.
cli.generate_arguments({
    "subcommand1": (Test1()),
    "subcommand2": [test, (Test2(), generate_arguments_options)],
    "subcommand3": (Test3()),
})

# Obtain the arguments that are introduced in the cli as a dictionary.
args = cli.parse()

# print(args)
# Execute the selected command in the cli. 
# If no arguments are introduced the function 
# you select in the CLI will be executed with 
# the arguments you have introduced in the CLI.
cli.execute_command()
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### CLI results
The following logs show how the CLI was generated from the classes declared above.

```bash
# python3 examples/test.py

usage: examples/test.py [-h] [-ta1 test_attr_1] [-ta2 test_attr_2] {t_method,subcommand1,subcommand2,subcommand3} ...

positional arguments:
  {t_method,subcommand1,subcommand2,subcommand3}
                        Test class
    t_method            A method1 example
    subcommand1         test1 description
    subcommand2
    subcommand3         test3 description

options:
  -h, --help            show this help message and exit
  -ta1 test_attr_1, --ta1 test_attr_1, --test_attr_1 test_attr_1
                        (str): optional parameter test_attr_1
  -ta2 test_attr_2, --ta2 test_attr_2, --test_attr_2 test_attr_2
                        (str): optional parameter test_attr_2.
```

```bash
# python3 examples/test.py subcommand3 -h

usage: examples/test.py subcommand3 [-h] [-ta4 t3_attr_4 [t3_attr_4 ...]] [-ta1 t3_attr_1] [-ta2 t3_attr_2] [-ta3 t3_attr_3] {t3_method1,t3_method2,t3_method3} ...

positional arguments:
  {t3_method1,t3_method2,t3_method3}
    t3_method1          Method 1 for subcommand3. This method contains an object as parameter.
    t3_method2          Method 2 for subcommand3.
    t3_method3          Method 3 for subcommand3

options:
  -h, --help            show this help message and exit
  -ta4 t3_attr_4 [t3_attr_4 ...], --ta4 t3_attr_4 [t3_attr_4 ...], --t3_attr_4 t3_attr_4 [t3_attr_4 ...]
                        (list): optional parameter test2.
  -ta1 t3_attr_1, --ta1 t3_attr_1, --t3_attr_1 t3_attr_1
                        (str): optional parameter test1
  -ta2 t3_attr_2, --ta2 t3_attr_2, --t3_attr_2 t3_attr_2
                        (int): optional parameter test2.
  -ta3 t3_attr_3, --ta3 t3_attr_3, --t3_attr_3 t3_attr_3
                        (datatime): optional parameter test2.
```
```bash
# python3 examples/test.py subcommand3 t3_method1 -h

usage: examples/test.py subcommand3 t3_method1 [-h] [-f {json,table,raw}] [-v] [-s search] [-a attribute [attribute ...]] attr_construct_t4 attr_construct_t5

positional arguments:
  attr_construct_t4     (str): This attribute is introduced in the constructor of Test4
  attr_construct_t5     (str): This attribute is introduced in the constructor of Test5

options:
  -h, --help            show this help message and exit
  -f {json,table,raw}, --f {json,table,raw}, --format {json,table,raw}
                        Specify the format that is going to be used as output
  -v, --v, --verbose    Set the log level to debug
  -s search, --s search, --search search
                        Search inside all values of a list
  -a attribute [attribute ...], --a attribute [attribute ...], --attribute attribute [attribute ...]
                        Only print the attributes you select
```
```bash
# python3 examples/test.py subcommand3 t3_method1 t4construct t5construct

{
    "test1": "t5construct"
}
```

```bash
# python3 examples/test.py  t_method -h 

usage: examples/test.py t_method [-h] [-f {json,table,raw}] [-v] [-s search] [-a attribute [attribute ...]] [-t test4] [-tpta test5.parameter_test_attr2] test3

positional arguments:
  test3                 (str): required parameter test3

options:
  -h, --help            show this help message and exit
  -f {json,table,raw}, --f {json,table,raw}, --format {json,table,raw}
                        Specify the format that is going to be used as output
  -v, --v, --verbose    Set the log level to debug
  -s search, --s search, --search search
                        Search inside all values of a list
  -a attribute [attribute ...], --a attribute [attribute ...], --attribute attribute [attribute ...]
                        Only print the attributes you select
  -t test4, --t test4, --test4 test4
                        (str, optional): optional parameter test4. Defaults to "test4".
  -tpta test5.parameter_test_attr2, --tpta test5.parameter_test_attr2, --test5.parameter_test_attr2 test5.parameter_test_attr2

```

```bash
# python3 examples/test.py -ta1 tt1 -ta2 tt2 t_method tt3 --t tt4 -tpta tt5 -f table

+--------------------------------------------------------------+
| Parameter_name |               Parameter_value               |
+----------------+---------------------------------------------+
|     test_1     |                     tt1                     |
|     test_2     |                     tt2                     |
|     test3      |                     tt3                     |
|     test4      |                     tt4                     |
|     test5      | {'test5': {'parameter_test_attr2': 'tt5'... |
+----------------+---------------------------------------------+
```





<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Roadmap

* [x] Added options to disable/enable class attributes arguments generation.
* [x] Support for class with non empty constructors.
* [x] Support for list of classes in json format.
* [ ] Support for list of classes with non empty constructors.
* [x] Support for datetime with the following formats 2022-12-20/00:00:20 and 2022-12-20
* [x] Support for enumeration type. It will be interpreted as argparse "choices".
* [x] _default method inside a class will be treated as the method that is going to be executed in the specified subparser. 
* [ ] Generate a log file with last commands executed.
* [x] Improve performance with argument prediction. Only generate the arguments that the program know that are introduced.
* [ ] Improve documentation
* [ ] Add tests
* [ ] Add argument that supports write into a file instead of printing in the terminal.
* [ ] Possibility to add custom arguments.
* [ ] Add decorators to change the behavior of the arguments generated.
  
See the [open issues](https://github.com/AlexSua/python-cli-generator/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

Project Link: [https://github.com/AlexSua/python-cli-generator](https://github.com/AlexSua/python-cli-generator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[issues-shield]: https://img.shields.io/github/issues/AlexSua/python-cli-generator?style=flat-square
[issues-url]: https://github.com/AlexSua/python-cli-generator/issues

[license-shield]: https://img.shields.io/github/license/AlexSua/python-cli-generator?style=flat-square
[license-url]: https://github.com/AlexSua/python-cli-generator/blob/main/LICENSE.txt
