import json
import os


def _update_class_with_dict(attr, attr_name, class_instance, data):
    if hasattr(attr, "__dict__"):
        for attr_attr_name in data:
            if hasattr(attr, attr_attr_name):
                _update_class_with_dict(
                    getattr(attr, attr_attr_name), attr_attr_name, attr, data[attr_attr_name])
    else:
        try:
            setattr(class_instance, attr_name, data)
        except Exception:
            pass

def set_dict_into_class(data_dic, class_instance):
    for data_key in data_dic:
        if hasattr(class_instance, data_key):
            attr = getattr(class_instance, data_key)
            _update_class_with_dict(
                attr, data_key, class_instance, data_dic[data_key])

    return class_instance

def generate_json_from_class(cls):
    result = {}
    if hasattr(cls, "__dict__"):
        for key, value in cls.__dict__.items():
            if not key.startswith("_"):
                if isinstance(value, object):
                    attr_result = generate_json_from_class(value)
                else:
                    attr_result = getattr(cls, key)
                result[key] = attr_result
    else:
        return cls
    return result

def get_dict_from_file(file_path):
    if os.path.isfile(file_path) and os.path.getsize(file_path) >0: 
        with open(file_path,"r") as f:
            return json.load(f)
    else:
        return {}

def set_file_from_dict(file_path, data):
    with open(file_path,"w") as f:
        return json.dump(data,f)

def remove_none_values(d):
    if not isinstance(d, dict):
        return d
    new_dict = {}
    for k, v in d.items():
        if v is not None:
            new_dict[k] = remove_none_values(v)
    return new_dict

def process_configuration_file(cls, configuration_file):
    if configuration_file is not None:
        configuration_object = {}
        if os.path.isfile(configuration_file) and os.path.getsize(configuration_file) >0:
            file = open(configuration_file, "r+")
            configuration_object = json.load(file)
        else:
            file = open(configuration_file, "w")

        class_name = cls.__class__.__name__
        class_name = cls.__name__ if class_name == "type" else class_name
        if class_name in configuration_object:
            set_dict_into_class(configuration_object[class_name], cls)
        else:
            configuration_object[class_name] = generate_json_from_class(cls)
            file.seek(0)
            json.dump(configuration_object,file, indent=4)
            file.truncate()
            
        file.close()