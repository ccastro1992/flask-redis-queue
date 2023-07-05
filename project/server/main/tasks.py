import time


def create_task(task_type):
    import os
    import random
    path = '/home/cristhian/TESTQUEUE'
    try:
        name = '%s/%s' % (path, random.randint(0, 1000000))
        os.mkdir(name)
        time.sleep(int(task_type) * 2)
    except OSError as error:
        return False

    return False