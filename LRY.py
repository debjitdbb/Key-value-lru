from collections import OrderedDict


class LRUCache:


    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity


    def get(self, key):
        if key not in self.cache:
            return -1 
        else:
            self.cache.move_to_end(key)
            return self.cache[key]


    def put(self, key, value):
        if key in self.cache:
            print("The entered key in already present....")
            return
        self.cache[key] = value 
        self.cache.move_to_end(key)
        if len(self.cache.cache) > self.capacity:
            self.cache.popitem(last = False)
        return   

    
    def remove(self, key):
        if key not in self.cache:
            print("Key not found...")
            return
        self.cache.pop(key)
        return  
