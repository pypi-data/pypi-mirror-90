
import os
import re
import json
import logging



def check_regex_unique(data, file_type = "json"):
    regex_pattern_json = r'[^{]\{\{([^{}]+)\}\}[^}]'
    regex_pattern_yaml = r'[^{]\{([^{}:,]+)\}[^}]'
    if file_type == "json":
        match = re.findall(regex_pattern_json, data)
    elif file_type == "yaml":
        match = re.findall(regex_pattern_yaml, data)
    else:
        return None
    return list(set(match))


def replace_placeholders(replace_dict, data, file_type = "json"):
    for string_to_replace, value in replace_dict.items():
        if file_type == "json":
            replace_pattern = '(\{\{' + string_to_replace + '\}\})'
        elif file_type == "yaml":
            replace_pattern = '(\{' + string_to_replace + '\})'
        replace_pattern_complied = re.compile(replace_pattern)
        data = re.sub(replace_pattern_complied, value, data)
    return data


def write_json(filename, data):
    with open(filename, "w") as outfile:
        outfile.write(data)


def get_place_holders(data, file_type = "json"):
    placeholders = None
    try:
        placeholders = check_regex_unique(data, file_type)
    except Exception as err:
        logging.error(err)
        raise err
    return placeholders


def place_holder_check_replace(data, list_replace, file_type = "json"):
    placeholders = None
    flag_replace = True
    placeholders = check_regex_unique(data, file_type)
    if list_replace and placeholders:
        for placeholder in placeholders:
            if not placeholder in list_replace:
                flag_replace = False
                break
    elif placeholders and not list_replace:
        flag_replace = False
        raise Exception(f"please provide the following placeholder value : {placeholders}")
    elif not (placeholders and list_replace):
        flag_replace = True
    else:
        flag_replace = False
        raise Exception("error in input commands , please check again.")
    return flag_replace
