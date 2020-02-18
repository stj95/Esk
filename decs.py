import time

class timeit(object):

    _logfile = r"logs\esk_timings.log"

    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):

        # time the function
        t1 = time.process_time()
        result = self.func(*args, **kwargs)
        t2 = time.process_time()

        delta = round(t2 - t1)
        log_string = "{} took {}s".format(self.func.__name__, delta)
        print(log_string)

        with open(self._logfile, 'a') as opened_file:
            opened_file.write(log_string + "\n")

        return result


class memoize(object):

    def __init__(self, func):
        self.func = func
        self.memo = {}

    def __call__(self, *args):

        if args in self.memo:
            return self.memo[args]

        else:
            out = self.func(*args)
            self.memo[args] = out
            return out



