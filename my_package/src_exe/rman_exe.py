import os
import sys
import datetime
from traceback import format_exc
from my_package.classes.rman_api import QueryParser


def pop_arg(name, array):
    result = None
    try:
        n = array.index(name)
        result = array.pop(n + 1)
        array.pop(n)
    except:
        pass

    return result


def collect_kwargs(array):
    result = {}
    for item in array:
        if "--KWARG_" in item:
            name = item.replace("--KWARG_")
            value = pop_arg(item, array)
            result[name] = value

    return result


if __name__ == '__main__':
    cls = None
    date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    exe_location = ''
    try:
        parse = sys.argv
        kwargs = collect_kwargs(parse)
        debug = pop_arg('--debug', parse)
        exe_location = os.sep.join(parse.pop(0).split(os.sep)[:-1])
        cls = QueryParser(parse, debug=debug, workdir=exe_location)
        rman, action = cls.create()
        try:
            if action == 'backup_task':
                rman.run('backup', **kwargs)
                rman.run('obsolete', **kwargs)
                rman.run('delete', **kwargs)
            else:
                rman.run(action, **kwargs)
        finally:
            rman.close()
    except:
        with open(os.path.join(exe_location,'critical_error_report_{}'.format(date)), 'w') as stream:
            stream.write(format_exc())

