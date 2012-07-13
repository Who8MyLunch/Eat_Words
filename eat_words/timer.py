"""
Derived from http://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python
"""

import time

class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.time_start = time.time()

    def __exit__(self, type, value, traceback):
        time_delta = time.time() - self.time_start
        
        if self.name:
            print('%s: %.3f' % (self.name, time_delta))
        else:
            print('Time: %.3f' % (time_delta))

            
if __name__ == '__main__':
    """
    Example.
    """
    
    def fn():
        # dummy function.
        t = 1.010101
        time.sleep(t)
        return t
        
        
    with Timer():
        print('sds')
        
        d = fn()
        
    print('sad')
    
        