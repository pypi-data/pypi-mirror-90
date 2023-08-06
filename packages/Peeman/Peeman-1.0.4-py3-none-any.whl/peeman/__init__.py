import json
import os
import yaml

from .errors import OpenmanException
from .schema_converter import SchemaConvertor


def from_collection(postmanfile=None):
    if postmanfile is None:
        raise OpenmanException('Empty file is not allowed')
    if not os.path.isfile(postmanfile):
        raise FileNotFoundError("Postman collection not found")
    with open(postmanfile, 'r') as fp:
        if postmanfile.endswith("yaml"):
            return ("yaml", yaml.safe_load(fp))
        if postmanfile.endswith("json"):
            return ("json", json.load(fp))


def from_ignore(ignorefile=None):
    ignoreschema = {}
    if not ignorefile:
        return ignoreschema
    with open(ignorefile, 'r') as f:
        try:
            ignoreschema = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            ignoreschema = json.load(f)
    return ignoreschema
