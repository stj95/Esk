import time

class logit(object):

    _logfile = r"logs\branch.log"

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):

        # time the function
        t1 = time.time()
        result = self.func(*args, **kwargs)
        t2 = time.time()

        log_string = "{} took {}s".format(self.func.__name__, (t2 - t1))
        print(log_string)

        with open(self._logfile, 'a') as opened_file:
            opened_file.write(log_string + "\n")


        return result

