import logging

from python_cli_generator import output_printer

class OutputProcessor:

    def __init__(self, logger):
        self.logger = logger
        self.format = "json"
        self.filter_list_search = None
        self.filter_list_attributes = None

    def _get_json_values(self, json_obj):
        arr = []

        def extract(obj, arr):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr)
                    else:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr)
            return arr

        values = extract(json_obj, arr)
        return values

    def _filter_list_search(self, json_list):
        json_list_result = []
        if self.filter_list_search is not None:
            for result in json_list:
                for value in self._get_json_values(result):

                    if value is not None and self.filter_list_search in str(value):
                        json_list_result.append(result)
                        break
        else:
            json_list_result = json_list
            
        return json_list_result

    def _filter_list_attributes(self, json_list):
        def deep_access(x, keylist):
            val = x
            for key in keylist:
                if key in val:
                    val = val[key]
                else:
                    val = None
            return val

        result = []
        if self.filter_list_attributes is not None:
            for json in json_list:
                element = {}
                found_attribute = False
                for attribute in self.filter_list_attributes:
                    arrayAttributes = attribute.split(".")
                    deep_access_result = deep_access(json, arrayAttributes)
                    if deep_access_result is not None:
                        element[arrayAttributes[-1]] = deep_access_result
                        found_attribute = True
                if found_attribute: result.append(element)
        else:
            result = json_list 
        return result

    def _print_result(self,result):
        output_printer.print_json_value(result, output_format=str(self.format))


    def _process_result(self, result):
        if self.logger is not False:
            self.logger.debug("Result: {}\n".format(result))
        if not isinstance(result, dict) and not isinstance(result, list):
            return {"result": result}
        self._print_result(result)


    def _process_result_list(self, item_list, titles=None):
        result = []
        for item in item_list:
            result_item = {}
            if not isinstance(item, dict):
                item = vars(item)
            for attr in item:
                if titles is None or attr in titles:
                    result_item[attr] = item[attr]
            result.append(result_item)

        result = self._filter_list_attributes(result)
        result = self._filter_list_search(result)
        self._print_result(result)


    def process_args(self,args):
        if "verbose" in args and args["verbose"]:
            self.logger.setLevel(logging.DEBUG)
        self.format = args.get("format", self.format)
        self.filter_list_search = args.get("search", self.filter_list_search)
        self.filter_list_attributes = args.get("attributes", self.filter_list_attributes)
        

    def process_result(self, result):
        if type(result) is list:
            return self._process_result_list(result)
        else:
            return self._process_result(result)
