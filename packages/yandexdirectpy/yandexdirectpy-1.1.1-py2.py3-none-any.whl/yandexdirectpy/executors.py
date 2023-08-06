from concurrent.futures import ThreadPoolExecutor

from typing import Any

executor = ThreadPoolExecutor(max_workers=10)


def execute_func_in_individual_thread(func: Any, ex: ThreadPoolExecutor = executor, **kwargs, ):
    task = ex.submit(func, **kwargs)
    res = task.result()
    return res
