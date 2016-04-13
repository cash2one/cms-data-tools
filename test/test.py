#! /usr/bin/env python
import time


class Mytime(object):
    def __init__(self, mtime=time.time()):
        self.mtime = mtime

    def update(self,mytime=time.time()):
        self.mtime = mytime

    def display(self, format=None):
        try:
            if format is None:
                print time.ctime(self.mtime)
            else:
                ltime = time.localtime(self.mtime)
                print time.strftime(format, ltime)
        except TypeError:
            print "param %s is incorrect, float is required!" % self.mtime
            exit()


class Stack(object):
    def __init__(self):
        self.list = []
        self.point = 0

    def push(self, obj):
        self.list.append(obj)
        self.point += 1

    def pop(self):
        return self.list.pop(self.point)

    def isempty(self):
        if self.point == 0:
            return 1
        return 0

    def peek(self):
        if self.point > 0:
            obj = self.list[self.point-1: self.point]
            obj.index()
            obj = obj.pop(0)
        else:
            raise IndexError
        return obj

class CapOpen(object):
    def __init__(self, fn, mode='r', buf=-1):
        self.file = open(fn, mode, buf)

    def __str__(self):
        return str(self.file)

    def __repr__(self):
        return 'self.file'

    def write(self, line):
        self.file.write(line.upper())

    def __getattr__(self, item):
        return getattr(self.file, item)

class SortedKeyDict(dict):
    def keys(self):
        return sorted(super( SortedKeyDict, self).keys())



def main():
    d = SortedKeyDict((('zheng-cai', 67), ('hui-jun', 68), ('xin-yi', 2)))
    print 'By iterator:'.ljust(12), [key for key in d]
    print 'By keys():'.ljust(12), d.keys()
if __name__ == "__main__":
    main()