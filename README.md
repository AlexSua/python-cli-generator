<a name="readme-top"></a>
<!-- PROJECT LOGO -->
<div align="center">

<h1 align="center">python-cli-generator</h1>

  <p align="center">
    A Python framework that allows an automatic generation of a CLI given a class, a function or a list of classes.
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
This library allows rapid creation of a CLI by automatically reading the attributes, methods and function parameters inside a class and generating its corresponding Command Line Interface through the built-in argparse library. The module contains an optional output processor able to print the result of the executed command in different formats.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
The necessary steps to get the library working on your environment.


### Prerequisites

Before using the application you need to have installed [python](https://www.python.org/). You can get instructions on how to install it by following the link shown before.



### Install the library

#### Get the latest version of the library from the github repository
```bash
pip3 install git+https://github.com/AlexSua/python-cli-generator.git
```

#### Get the stable version from the PyPI repository
```bash
pip3 install python-cli-generator
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Usage

### Import the library
Import the controller class "Cli" which contains the main functionality for initializing the generation process.

```Python
from python_cli_generator import Cli
```

### Initialize HTTPSession and CacheStorage (Optional)
Initialize classes HTTPSession and CacheStorage for fetching from a REST API and cache the result of a method into a file respectively. These classes contain a method that acts as a decorator for another method providing extra functionality. You can see the example that follows to see how it works.

```python
from python_cli_generator.plugins.cache import CacheStorageFile
from python_cli_generator.plugins.http import HTTPSession

# Introduce as arguments here all parameters who wish to be passed as attributes to session of the requests library. Every request through the method decorator called fetch from HTTPSession will use this parameters on each request.
jikanmoe = HTTPSession(url_base="https://api.jikan.moe/v4/", headers={
  'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
})

# Initialize the file where the result of cached methods will be stored.
cache_storage = CacheStorageFile(file_name=".cache.example_filename")

```


### Create input classes
Create the classes the generator will use to generate the Command line interface.
> Notice that comments are as well parsed and automatically added to the CLI.
```Python
from datetime import datetime
from enum import Enum
from typing import List

class ParameterTest:
    """Parameter test class
    parameter_test_required (str): optional parameter parameter_test_attr1
    parameter_test_optional (str): optional parameter parameter_test_attr2.

    """
    #If it doesn't have default value is not generated.
    parameter_test_attr1: str
    parameter_test_attr2: str = ""

class AnimeType(Enum):
    tv = "tv"
    movie = "movie"
    ova = "ova"
    special = "special"
    ona = "ona"
    music = "music"
    
class Test:
    """Test class
    test_attr_1 (str): optional parameter test_attr_1
    test_attr_2 (str): optional parameter test_attr_2.
    """
    test_attr_1: str
    test_attr_2: str

    def __init__(self):
        # self.test_attr_1 = "test1"
        # self.test_attr_2 = "test2"
        pass

    # Store cache for a maximum of 60 seconds.
    @cache_storage.cache(expiration=60)

    # Fetch anime from the path /anime of jikanmoe. Query params are automatically introduced given the optional parameters of the method.
    # _response gives you the response of the request. If you use the POST method positional parameters are introduced as body parameters.
    @jikanmoe.fetch("anime", method="GET")
    def anime_search(self, q: str = None,  min_score: int = None, type: AnimeType = None, sort: str = "desc", _response: dict = None):
        """Get anime list from mal
        Args:
            q (str, optional): Query anime. Defaults to None.
            min_score (int, optional): Minimum score. Defaults to None.
            type (AnimeType, optional): Type of anime. Defaults to None.
            sort (str, optional): Sort anime. Defaults to None.

        """
        return list(map(lambda x: {"mal_id": x["mal_id"], "title": x["titles"][0]["title"], "genres": ",".join(list(map(lambda y: y["name"], x["genres"]))), "score": x["score"]}, _response["data"]))



    def t_method2(self, test3, test4="test4", **test5: ParameterTest):
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
        return test1 

    def t2_method2(self, **test1: Test1):
        return test1


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
    # Enable/disable the output processing. The automatically format of the executed method.
    "enable_output_processing": True,

    # Enable/disable the argument that specify the format with which the user can specify a print format to the output processor.
    "enable_format_argument": True,

    # Default format for the output processor
    "format": "json",

    # Enable/disable the argument that tells the program to output the result inside a file.
    "enable_file_argument":True,

    # Enable/disable the argument that allows to search for elements inside a result that is a list of elements.
    "enable_search_argument": True,

    # Enable/disable the argument that allows to hide the full list of optional arguments.
    "enable_full_help_argument": False,

    # Enable/disable the argument that allows to set the log level to debug.
    "enable_verbose_argument": True,

    # Configuration file where configuration of classes (attributes) will be stored between executions.
    "configuration_file": "./configuration_file.json"
}

# Options per subcommand
generate_arguments_options = {
    "enable_format_argument": True,
    "format": "json",
    "enable_file_argument":True,
    "enable_search_argument": True,
    "enable_full_help_argument": True,
    "enable_verbose_argument": True,

    # Enable/disable the generation of arguments from attributes of a class.
    "enable_class_attributes_generator": True,

    # Enable/disable the generation of arguments from functions of a class.
    "enable_class_functions_generator": False
}

# Create CLI class with the selected configuration.
cli = Cli(**options)

# Generate CLI arguments for Test class
cli.generate_arguments(Test())

# Geberate CLI arguments for the following dictionary.
cli.generate_arguments({
    "subcommand1": (Test1()),
    "subcommand2": [(Test2(), generate_arguments_options)],
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
# python3 examples/example.py

usage: examples/example.py [-h] [-ta1 test_attr_1] [-ta2 test_attr_2] {t_method,subcommand1,subcommand2,subcommand3} ...

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
# python3 examples/example.py subcommand3 -h

usage: examples/example.py subcommand3 [-h] [-ta4 t3_attr_4 [t3_attr_4 ...]] [-ta1 t3_attr_1] [-ta2 t3_attr_2] [-ta3 t3_attr_3] {t3_method1,t3_method2,t3_method3} ...

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
# python3 examples/example.py subcommand3 t3_method1 -h

usage: examples/example.py subcommand3 t3_method1 [-h] [-f {json,table,raw}] [-v] [-s search] [-a attribute [attribute ...]] attr_construct_t4 attr_construct_t5

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
# python3 examples/example.py subcommand3 t3_method1 t4construct t5construct

{
    "test1": "t5construct"
}
```

```bash
# python3 examples/example.py  t_method -h 

usage: examples/example.py t_method [-h] [-f {json,table,raw}] [-v] [-s search] [-a attribute [attribute ...]] [-t test4] [-tpta test5.parameter_test_attr2] test3

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
# python3 examples/example.py -ta1 tt1 -ta2 tt2 t_method tt3 --t tt4 -tpta tt5 -f table

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

```bash
# python3 examples/example.py -ta1 tt1 -ta2 tt2 t_method tt3 --t tt4 -tpta tt5 -f table

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

```bash
# python3 examples/example.py anime_search -q naruto -f table

+-------------------------------------------------------------------------------------------------+
| Mal_id |                    Title                    |              Genres              | Score |
+--------+---------------------------------------------+----------------------------------+-------+
|   20   |                   Naruto                    |     Action,Adventure,Fantasy     | 7.98  |
|  1735  |             Naruto: Shippuuden              |     Action,Adventure,Fantasy     | 8.25  |
| 34566  |       Boruto: Naruto Next Generations       |     Action,Adventure,Fantasy     | 5.75  |
| 16870  |         The Last: Naruto the Movie          | Action,Adventure,Fantasy,Romance | 7.78  |
| 28755  |          Boruto: Naruto the Movie           |     Action,Adventure,Fantasy     | 7.41  |
| 13667  | Naruto: Shippuuden Movie 6 - Road to Nin... |     Action,Adventure,Fantasy     | 7.67  |
|  2472  |         Naruto: Shippuuden Movie 1          |     Action,Adventure,Fantasy     | 7.29  |
|  442   | Naruto Movie 1: Dai Katsugeki!! Yuki Him... |     Action,Adventure,Fantasy     | 7.11  |
|  4437  |     Naruto: Shippuuden Movie 2 - Kizuna     |     Action,Adventure,Fantasy     | 7.28  |
|  8246  | Naruto: Shippuuden Movie 4 - The Lost To... |     Action,Adventure,Fantasy     | 7.42  |
| 10589  | Naruto: Shippuuden Movie 5 - Blood Priso... |     Action,Adventure,Fantasy     | 7.45  |
|  936   | Naruto Movie 2: Dai Gekitotsu! Maboroshi... |     Action,Adventure,Fantasy     | 6.87  |
|  2144  | Naruto Movie 3: Dai Koufun! Mikazuki Jim... |     Action,Adventure,Fantasy     | 6.91  |
|  6325  | Naruto: Shippuuden Movie 3 - Hi no Ishi ... |     Action,Adventure,Fantasy     | 7.33  |
| 32365  | Boruto: Naruto the Movie - Naruto ga Hok... |     Action,Adventure,Fantasy     | 7.35  |
| 12979  | Naruto SD: Rock Lee no Seishun Full-Powe... |          Action,Comedy           | 7.16  |
|  594   | Naruto: Takigakure no Shitou - Ore ga Ei... |     Action,Adventure,Fantasy     | 6.76  |
|  761   | Naruto: Akaki Yotsuba no Clover wo Sagas... |         Adventure,Comedy         | 6.55  |
|  1074  | Naruto Narutimate Hero 3: Tsuini Gekitot... |              Action              | 6.78  |
|  2248  | Naruto: Dai Katsugeki!! Yuki Hime Shinob... |      Action,Comedy,Fantasy       | 6.86  |
| 10686  | Naruto: Honoo no Chuunin Shiken! Naruto ... |         Action,Adventure         | 7.17  |
| 19511  |   Naruto: Shippuuden - Sunny Side Battle    |      Comedy,Fantasy,Gourmet      | 7.55  |
|  4134  | Naruto: Shippuuden - Shippuu! "Konoha Ga... |              Action              | 7.14  |
| 10659  | Naruto Soyokazeden Movie: Naruto to Mash... |          Action,Comedy           | 6.96  |
|  7367  |           Naruto: The Cross Roads           |          Action,Fantasy          | 6.79  |
+--------+---------------------------------------------+----------------------------------+-------+
```





<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Roadmap

* [x] Added options to disable/enable class attributes arguments generation.
* [x] Support for class with non-empty constructors.
* [x] Support for a list of classes in JSON format.
* [ ] Support for a list of classes with non-empty constructors.
* [x] Support for DateTime with the following formats 2022-12-20/00:00:20 and 2022-12-20
* [x] Support for enumeration type. It will be interpreted as argparse "choices".
* [x] _default method inside a class will be treated as the method that is going to be executed in the specified subparser. 
* [ ] Generate a log file with last commands executed.
* [x] Improve performance with argument prediction. Only generate the arguments that the program know that are introduced.
* [ ] Improve documentation
* [ ] Add tests
* [x] Add an argument that supports writing into a file instead of printing in the terminal.
* [ ] Possibility to add custom arguments.
* [ ] Add decorators to change the behavior of the arguments generated.
* [x] Add configuration file. The CLI can fetch/store the configuration for classes introduced as arguments in 'generate_arguments'
* [x] Add cache. A cache decorator can be used to save the result between executions of a function for a given set of arguments during a given time.
* [x] Add REST API support. A REST API decorator can be used to use an API using the python method parameters as input for generating the request.
* [x] Add multiple output support. CSV and YAML.
  
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
