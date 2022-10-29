import json

def print_format_raw(json_object):
    print(str(json_object))

def print_format_json(json_object):
    print(json.dumps(json_object, indent=4))

def print_format_table(json_list, title = None, filtered_attributes = None):
    if len(json_list) <= 0:
        print("No elements to show.")
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
        # print("+{title:-^{width}}+".format(title=" {} ".format(title).upper(), width=max_line_size-2))
        print("+{title:-^{width}}+".format(title="", width=max_line_size-2))
        print(line)
        print("{}".format(underline))
        for json_el in json_list:
            line = ""
            for f_attribute in filtered_attributes:
                title = " "
                if f_attribute in json_el:
                    title = json_el[f_attribute]

                line += "| {title: ^{width}} ".format(title=title, width=size_keys_dict[f_attribute])
            line += "|"
            print(line)
        print("{}".format(underline))


def print_json_value( json_value, title=None, filtered_attributes=None, output_format=None):

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
        "table": lambda: print_format_table(json_value,title, filtered_attributes),
        "raw": lambda: print_format_raw(json_value)
    }

    print_functions.get(output_format,lambda: print_format_json(json_value))()


