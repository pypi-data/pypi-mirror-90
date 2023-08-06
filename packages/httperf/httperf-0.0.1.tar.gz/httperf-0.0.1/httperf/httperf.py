import requests
import time


class HTTPerf:
    def __init__(self, url, count=5, location=None):
        self.url = url 
        self.count = count
        if location:
            self.location = location

    def get(self):
        """Get the timings for self.count GET requests to self.url."""
        get_times = {}
        timings_sum = 0
        for i in range(self.count):
            timing = get_timing(self.url)
            get_times[i] = timing
            timings_sum += timing
        get_times["avg"] = timings_sum / self.count
        return get_times

    def get_parallel(self):
        """Do a whole bunch of get or post requests in parallel"""
        raise NotImplementedError

    def post_timing(self, args):
        resp = requests.post(self.endpoint, args)
        return resp.elapsed.total_seconds()


def get_timing(url):
    resp = requests.get(url)
    return resp.elapsed.total_seconds()

