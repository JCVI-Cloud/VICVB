"""Configuration and resources of this package"""
from pkg_resources import Requirement, resource_filename, resource_string
import os,json

pkg_name = "VICVB"
pkg_data = pkg_name+"/data"

def get_pkg_data_dir():
    return resource_filename(Requirement.parse(pkg_name),pkg_data)

def get_pkg_data_file(name):
    return resource_filename(Requirement.parse(pkg_name),pkg_data+"/"+name)

def get_pkg_data_string(name):
    return resource_string(Requirement.parse(pkg_name),pkg_data+"/"+name)

def get_data_file(name=None,name_pkg=None):
    if name is None:
        return get_pkg_data_file(name_pkg)
    else:
        return name

def get_data_string(name=None,name_pkg=None):
    if name is None:
        return get_pkg_data_string(name_pkg)
    else:
        with open(name,'r') as f:
            return f.read()

def set_data_string(s,name):
    with open(name,'w') as f:
        f.write(s)

def load_config_json(config_file):
    if os.path.exists(config_file):
        with open(config_file,'r') as f:
            return json.load(f)
    else:
        return {}

def save_config_json(config,config_file):
    with open(config_file,'w') as f:
        json.dump(config,f)

