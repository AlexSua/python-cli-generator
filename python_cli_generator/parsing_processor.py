import copy


def _merge_dictionary(dic1: dict, dic2: dict):
    result = copy.copy(dic1)
    for key in dic2.keys():
        if key in result and isinstance(dic2[key], dict):
            result[key] = _merge_dictionary(result[key], dic2[key])
        else:
            result[key] = dic2[key]
    return result


def _process_nest_arguments(args: dict):
    nested_arguments = {}
    for arg_key in args:
        arg_key_split = arg_key.rsplit(".", 1)
        arg_key_split_len = len(arg_key_split)
        if arg_key_split_len > 1:
            nested_arguments = _merge_dictionary(nested_arguments, _process_nest_arguments({arg_key_split[0]:
                                                                                            {arg_key_split[1]: args[arg_key]}}))
        else:
            nested_arguments = _merge_dictionary(
                nested_arguments, {arg_key: args[arg_key]})
    return nested_arguments

def _instantiation(args, cls, store):
    kwargs = {}
    for key,value in args.items():
        if isinstance(value,dict):
            kwargs[key] = _process_class_arguments(value,store)
        else:
            kwargs[key] = value
    return cls(**kwargs)


def _process_class_arguments(args:dict,store:dict):
    result = {}
    for key,value in args.items():
        if key.startswith("$constructor"):
            class_name = key.split("_")[1]
            return _instantiation(value, store[class_name], store)
        elif isinstance(value,dict):
            result[key] = _process_class_arguments(value,store)
        else:
            result[key] = value
    return result


def _clean_arguments(args, arguments_to_delete=[]):
    for element in arguments_to_delete:
        if hasattr(args, element):
            delattr(args, element)
    return {k: v for k, v in vars(args).items() if v is not None}


def _update_class_with_args(attr, attr_name, class_instance, data):
    if hasattr(attr, "__dict__"):
        for attr_attr_name in data:
            if hasattr(attr, attr_attr_name):
                _update_class_with_args(
                    getattr(attr, attr_attr_name), attr_attr_name, attr, data[attr_attr_name])
    else:
        try:
            setattr(class_instance, attr_name, data)
        except Exception:
            pass


def validate_json(json, cls):
    result = True
    for attr in json:
        if hasattr(cls, attr):
            cls_attr = getattr(cls, attr)
            if hasattr(cls_attr, "__dict__"):
                result = validate_json(json[attr], cls_attr)
            else:
                result = False
                if cls_attr.__class__ == json[attr].__class__:
                    result = True
        else:
            result = False
        if not result:
            break
    return result


def process_parsed_arguments(args, store):
    args = _clean_arguments(args)
    args = _process_nest_arguments(args)
    args = _process_class_arguments(args,store)
    return args


def set_args_into_class(args, class_instance):
    class_name = type(class_instance).__name__
    if class_name in args:
        data_dic = args[class_name]
        for data_key in copy.copy(data_dic):
            if hasattr(class_instance, data_key):
                attr = getattr(class_instance, data_key)
                _update_class_with_args(
                    attr, data_key, class_instance, data_dic[data_key])

    return class_instance
