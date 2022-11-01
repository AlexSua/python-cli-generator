

from datetime import datetime
from typing import List
from python_cli_generator import Cli


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

# print(args)
# Execute the selected command in the cli. 
# If no arguments are introduced the function 
# you select in the CLI will be executed with 
# the arguments you have introduced in the CLI.
cli.execute_command()
