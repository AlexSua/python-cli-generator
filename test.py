


from python_cli_generator.cli import Cli

class ParameterTest:
    """Parameter test class
    parameter_test_required (str): required parameter parameter_test_required
    parameter_test_optional (str): optional parameter parameter_test_optional.

    """    
    parameter_test_required:str
    parameter_test_optional:str = ""

class Test:
    """Test class
    test_1 (str): optional parameter test1
    test_2 (str): optional parameter test2.
    """    
    test_1:str
    test_2:str

    def __init__(self):
        self.test_1 =  "test1"
        self.test_2 =  "test2"

    def _default(self, test3, test4="test4", **test5:ParameterTest):
        """A method1 example

        Args:
            test3 (str): required parameter test3
            test4 (str, optional): optional parameter test4. Defaults to "test4".
        """        
        return [
            {"parameter_name":"test_1","parameter_value":self.test_1},
            {"parameter_name":"test_2","parameter_value":self.test_2},
            {"parameter_name":"test3","parameter_value":test3},
            {"parameter_name":"test4","parameter_value":test4},
            {"parameter_name":"test5","parameter_value":test5},
        ]
        
cli = Cli()
cli.generate_arguments(Test())
cli.parse()
cli.execute_command()
