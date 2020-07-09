from importlib import util
import os


def get_py_files(src):
    py_files = []
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files


def dynamic_import(module_name, py_path):
    module_spec = util.spec_from_file_location(module_name, py_path)
    module = util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def dynamic_import_from_src(src, register_global=False, star_import=False):
    my_py_files = get_py_files(src)
    for py_file in my_py_files:
        f = os.path.split(py_file)[-1]
        module_name = f[:f.rindex('.')]
        imported_module = dynamic_import(module_name, py_file)
        if register_global:
            if star_import:
                for obj in dir(imported_module):
                    globals()[obj] = imported_module.__dict__[obj]
            else:
                globals()[module_name] = imported_module
    return
