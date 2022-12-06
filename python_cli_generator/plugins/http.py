import copy
import inspect

from enum import Enum
from python_cli_generator.input_processor import generate_json_from_class
from python_cli_generator.utils import decorator_factory


class HTTPError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message

class HTTPMethods(Enum):
    get = "GET"
    post = "POST"
    update = "UPDATE"
    patch = "PATCH"
    put = "PUT"
    delete = "DELETE"


class HTTPSession:
    def __init__(self, *args, session=None, url_base=None, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.session = session
        self.url_base = url_base

    def _http_transform_function_values(self, fn, *args, **kwargs):
        signature = inspect.signature(fn)

        json_data = {}
        params = {}

        position=-1
        for parameter_name in signature.parameters:
            position+=1

            if parameter_name in ["self"] or parameter_name.startswith("_"):
                if parameter_name == "_data":
                    json_data = args[position]
                continue
            parameter_value = signature.parameters[parameter_name]
            kwarg_element = None

            if parameter_name not in kwargs and position < len(args):
                kwargs[parameter_name] = args[position]
            if parameter_name in kwargs:
                kwarg_element = kwargs[parameter_name]
                def adapt_kwarg(value): 
                    value_type = type(value)
                    if value_type.__module__ != "builtins":
                        if issubclass(value_type, Enum) or value_type == Enum or value_type.__name__ == "EnumMeta":
                            return  {parameter_value.name: value}
                        return  generate_json_from_class(value)
                    else:
                        return {parameter_value.name: value}
                    
                if parameter_value.default == inspect._empty:
                    json_data = {
                        **json_data, **adapt_kwarg(kwarg_element)
                    }
                else:
                    params = {
                        **params, **adapt_kwarg(kwarg_element)
                    }
        return (json_data, params)

    def _http_process_url(self, url: str, attributes: dict):
        for key, value in copy.copy(attributes).items():
            url_attribute = "{"+key+"}"
            if url_attribute in url:
                url = url.replace("{"+key+"}", value)
                del attributes[key]
        return url

    def _request(self, url, method, decode="UTF-8", **kwargs):
        import requests
        from requests import Session     

        if self.session is None:
            self.session = Session()  
            for kwarg_name, kwarg_value in self.kwargs.items():
                if hasattr(self.session,kwarg_name):
                    setattr(self.session,kwarg_name, kwarg_value)   
        try:
            url = self.url_base + url
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            if response.headers.get("Content-Type").startswith("application/json"):
                return response.json()
            else:
                return response.content.decode(decode)
        except requests.HTTPError as e:
            raise HTTPError(e.response.status_code,e.response.text)

    def fetch(self, url: str = "", method: HTTPMethods = "GET", json_type=True, **request_options, ):
        def _http_call(fn, *args, url=url, **kwargs):
            json_data, params = self._http_transform_function_values(
                fn, *args, **kwargs)
            url = self._http_process_url(url, json_data)
            request_options["json" if json_type else "data"] = json_data if json_data else None
            request_options["params"] = params=params if params else None
            response = self._request(
                url, method,  **request_options)

            if inspect.signature(fn).parameters.get("_response"):
                kwargs["_response"] = response

            result = fn(*args,  **kwargs)
            return result if result is not None else response

        return decorator_factory(_http_call)
