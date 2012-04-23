'''
Created on Apr 18, 2012

@author: mikko
'''
import heapq
import itertools

class PriorityQueue(object):
    '''
    Creates Priority queue to use with Fortunes's algorithm
    item is a tuple of ((x,y), pointer_to_leaf)
    '''
    #heap = []

    def __init__(self, items=[]):
        '''
        Constructor
        '''
        self.heap = []
        self.entries = {}
        self.counter = itertools.count(0,-1)
        for i in items:
            self.add(i)

    def add(self, item):
        # Check for duplicate
        if item in self.entries:
            return

        count = next(self.counter)
        # use negative y-coordinate as a primary key
        # heapq in python is min-heap and we need max-heap
        entry = [item[0][1]*-1, count, item]
        self.entries[item] = entry
        heapq.heappush(self.heap, entry)

    def pop(self):
        while self.heap:
            temp = heapq.heappop(self.heap)
            #print "p" + str(temp[2])
            if not temp[2] == 'DELETED':
                del self.entries[temp[2]]
                return temp[2]
        raise KeyError('pop from an empty priority queue')

    def delete(self, item):
        entry = self.entries.pop(item)
        entry[2] = 'DELETED'

