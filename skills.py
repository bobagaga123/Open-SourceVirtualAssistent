import os
import importlib.util


def import_all_py_files(directory="skills"):
    files = [f for f in os.listdir(directory) if f.endswith(".py")]

    for file in files:
        module_name = os.path.splitext(file)[0]
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Добавляем импортированный модуль в словарь глобальных переменных
        globals()[module_name] = module

def execute_skill(skill_category, skill_name):
    func = getattr(globals()[skill_category], skill_name)
    print(func)

import_all_py_files(directory="skills")