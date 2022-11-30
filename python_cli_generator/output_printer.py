import json

def stdout(print_result, file=None):
    if file is not None:
        with open(str(file), 'w') as f:
            f.write(print_result+"\n")
    else:
        print(print_result)


def print_format_raw(json_object):
    return str(json_object)

def print_format_json(json_object):
    try:
        return json.dumps(json_object, indent=4)
    except:
        return json_object

def print_format_yaml(json_object):
    import yaml
    yaml_result = yaml.dump(json_object)
    return yaml_result

def print_format_table(json_list, title = None, filtered_attributes = None):
    print_result = ""
    if len(json_list) <= 0:
        print_result+="No elements to show.\n"
        return

    if isinstance(json_list, list) and isinstance(json_list[0], dict) and filtered_attributes is None:
        filtered_attributes = []
        for key in json_list[0]:
            filtered_attributes.append(key)

    if filtered_attributes is not None:
        filtered_attributes = list(map(lambda x: x.split(".")[-1], filtered_attributes))
        size_keys_dict = {}
        for f_attribute in filtered_attributes:
            size_keys_dict[f_attribute] = len(f_attribute)
        for json_el in json_list:
            for f_attribute in filtered_attributes:
                if f_attribute in json_el:
                    if not json_el[f_attribute]:
                        json_el[f_attribute] = " "
                    json_el[f_attribute] = str(json_el[f_attribute])
                    if len(json_el[f_attribute]) >= 40:
                        json_el[f_attribute] = json_el[f_attribute][:40] + "..."
                    value_len = len(json_el[f_attribute])
                    size_keys_dict[f_attribute] = value_len if f_attribute not in size_keys_dict else size_keys_dict[f_attribute]
                    size_keys_dict[f_attribute] = value_len if value_len > size_keys_dict[f_attribute] else size_keys_dict[f_attribute]

        line = ""
        underline = ""
        for f_attribute in filtered_attributes:
            line += "| {title: ^{width}} ".format(title=f_attribute.capitalize(), width=size_keys_dict[f_attribute])
            underline += "+{title:-^{width}}".format(title="", width=size_keys_dict[f_attribute]+2)
        line = line + "|"
        underline = underline+"+"
        max_line_size = len(line)
        print_result+="+{title:-^{width}}+\n".format(title="", width=max_line_size-2)
        print_result+=line+"\n"
        print_result+="{}\n".format(underline)
        for json_el in json_list:
            line = ""
            for f_attribute in filtered_attributes:
                title = " "
                if f_attribute in json_el:
                    title = json_el[f_attribute]

                line += "| {title: ^{width}} ".format(title=title, width=size_keys_dict[f_attribute])
            line += "|"
            print_result+=line+"\n"
        print_result+="{}\n".format(underline)
    return print_result

def print_format_csv(json_list,filtered_attributes=None):
    import csv
    import io

    mem_file = io.StringIO()

    if isinstance(json_list, list) and isinstance(json_list[0], dict) and filtered_attributes is None:
        filtered_attributes = []
        for key in json_list[0]:
            filtered_attributes.append(key)
        
        writer = csv.DictWriter(mem_file, fieldnames=filtered_attributes, quotechar="\"")
        writer.writeheader()
        for json_element in json_list:
            writer.writerow(json_element)

    return mem_file.getvalue()


def print_json_value( json_value, title=None, filtered_attributes=None, output_format=None, file = None):

    if isinstance(json_value, list) and len(json_value)>0 and isinstance(json_value[0], dict) :
        if output_format is None:
            output_format = "table"
    elif isinstance(json_value, list) and len(json_value)==0:
        pass
    else:
        if output_format is None or output_format in ["table","csv"]:
            output_format="json"

    print_functions = {
        "json": lambda: print_format_json(json_value),
        "csv": lambda: print_format_csv(json_value,filtered_attributes),
        "table": lambda: print_format_table(json_value,title, filtered_attributes),
        "raw": lambda: print_format_raw(json_value),
        "yaml": lambda: print_format_yaml(json_value)
    }

    print_result = print_functions.get(output_format,lambda: print_format_json(json_value))()
    stdout(print_result, file)