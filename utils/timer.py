import time

'''
Use this class to track the time performance of your code.
'''

class TimeError(Exception):
    """Add customer error. Ex. raise TimeError(f"Custom Error")"""

class Timer:
    def __init__(self, logger=None):
        self.logger = logger
        self.timers = {}

    def start(self, name_of_timer: str):
        if name_of_timer in self.timers:
            raise TimeError(f"Timer {name_of_timer} already started.")

        start_time = time.perf_counter()
        self.timers.setdefault(name_of_timer, start_time)

    # Stops the timer and returns elapsed time.
    def stop(self, name_of_timer):
        if name_of_timer not in self.timers:
            raise TimeError(f"Timer {name_of_timer} is not started.")

        start_time = self.timers.get(name_of_timer)
        end_time = time.perf_counter()
        self.timers.pop(name_of_timer)
        return end_time - start_time

    def stop_and_print_elapsed_time(self, name_of_timer):
        elapsed_time = Timer.stop(self, name_of_timer)
        print(f"Timer '{name_of_timer}' elapsed time: {elapsed_time:0.4f}")