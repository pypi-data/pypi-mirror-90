import importlib
import inspect

from .wrappers import KafkaTask


def collect_tasks(modules, base_dir, logger):
    """
    Collecting kafka tasks for handling them
    Variable TASK_MODULES contains list of paths<str> to files\modules with handlers tasks starting from BASE_DIR
    BASE_DIR - project root

    Script detect kafka handling tasks if:
    1. Parent of handling class in KafkaTask
    or
    2. Function have decorator @task

    """
    tasks = {}
    for module_name in modules:
        try:
            module = importlib.import_module(module_name, base_dir)
            for func_name in dir(module):
                func = getattr(module, func_name)
                if inspect.isclass(func) and func != KafkaTask and issubclass(func, KafkaTask):
                    presented = tasks.get(func.__action__, [])
                    presented.append(func(logger=logger))
                    tasks[func.__action__] = presented
                elif inspect.isfunction(func) and hasattr(func, '__is_kafka__'):
                    presented = tasks.get(func.__action__, [])
                    presented.append(func)
                    tasks[func.__action__] = presented
        except ModuleNotFoundError as e:
            logger.error(f"Module {module_name}, missed")
    logger.info(f'Parsed: {tasks}')
    return tasks
