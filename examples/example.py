

from datetime import datetime
from enum import Enum
from typing import List
from python_cli_generator import Cli
from python_cli_generator.plugins.cache import CacheStorageFile
from python_cli_generator.plugins.http import HTTPSession

# Introduce as arguments here all parameters who wish to be passed as attributes to requests session. This was done in this way to lazy import the requests library due to its impact on the performance.
jikanmoe = HTTPSession(url_base="https://api.jikan.moe/v4/", headers={
  'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
})
cache_storage = CacheStorageFile(file_name=".cache.example_filename")

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

class AnimeOrderBy(Enum):
    mal_id = "mal_id"
    title = "title"
    rating = "rating"
    type = "type"
    start_date = "start_date"
    end_date = "end_date"
    episodes = "episodes"
    score = "score"
    scored_by = "scored_by"
    rank = "rank"
    popularity = "popularity"
    members = "members"
    favorites = "favorites"
    
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
    def anime_search(self, q: str = None,  min_score: int = None, page=None, type: AnimeType = None, order_by:AnimeOrderBy = None, sort: str = None, _response: dict = None):
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

# Create CLI class with the selected configuratio.
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