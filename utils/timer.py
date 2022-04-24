import time

'''
Use this class to track the time performance of your code.
'''

class TimeError(Exception):
    """Add custom error. Ex. raise TimeError(f"Custom Error")"""

logger = None
timers = {}

class Timer:

    # def __init__(self, logger=None):
    #     self.logger = logger
    #     self.timers = {}

    @staticmethod
    def start(name_of_timer: str):
        if name_of_timer in timers:
            raise TimeError(f"Timer {name_of_timer} already started.")

        start_time = time.perf_counter()
        timers.setdefault(name_of_timer, start_time)

    # Stops the timer and returns elapsed time.
    @staticmethod
    def stop(name_of_timer):
        if name_of_timer not in timers:
            raise TimeError(f"Timer {name_of_timer} is not started.")

        start_time = timers.get(name_of_timer)
        end_time = time.perf_counter()
        timers.pop(name_of_timer)
        return end_time - start_time

    @staticmethod
    def stop_and_print_elapsed_time(name_of_timer):
        elapsed_time = Timer.stop(name_of_timer)
        print(f"Timer '{name_of_timer}' elapsed time: {elapsed_time:0.4f}")