import os
import importlib.util


def import_all_py_files(directory="skills"):
    files = [f for f in os.listdir(directory) if f.endswith(".py")]

    skills_counter = 0
    skill_names = []
    for file in files:
        module_name = os.path.splitext(file)[0]
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(directory, file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Добавляем импортированный модуль в словарь глобальных переменных
        globals()[module_name] = module
        skills_counter +=1
        skill_names.append(module_name)

    return skills_counter, skill_names

def execute_skill(skill_category, skill_name, *args):
    object = getattr(globals()[skill_category], skill_name)
    if callable(object):
        if len(args) > 0:
            return object(args)
        else:
            return object()
    else:
        return object