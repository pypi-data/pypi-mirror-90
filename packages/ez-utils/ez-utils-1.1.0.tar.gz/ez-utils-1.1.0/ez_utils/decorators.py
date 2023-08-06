import time
import sys
import logging

def timeit(method):
    """
    Good ol' timing decorator

    :param method:
    :return:
    """
    def timed(*args, **kwargs):
        module_name = sys.modules[method.__module__].__name__

        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()

        logging.debug('%s: %s  %2.2f ms' % (module_name, method.__name__, (end - start) * 1000))

        return result
    return timed
