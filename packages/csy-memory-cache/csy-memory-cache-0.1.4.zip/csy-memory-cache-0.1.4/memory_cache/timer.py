# coding=gbk

"""
定时器
"""
import threading


class Timer:
    def __init__(self, interval_time=5):
        self.interval_time = interval_time

    def do(self, func):
        func()
        timer = threading.Timer(self.interval_time, self.do, args=(func, ))
        timer.start()
