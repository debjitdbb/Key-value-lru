from collections import OrderedDict
import json

class LRUCache:


    def __init__(self):
        self.cache = OrderedDict()
        # self.capacity = capacity


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
        elif self.cache.__sizeof__() > 1e9:
            self.cache.popitem(last = False)

        self.cache[key] = value 
        self.cache.move_to_end(key)
        # if len(self.cache.cache) > self.capacity:
        #     self.cache.popitem(last = False)
        return   

    
    def remove(self, key):
        if key not in self.cache:
            print("Key not found...")
            return
        self.cache.pop(key)
        return  

temp = LRUCache()

from flask import Flask,jsonify
app = Flask(__name__)

@app.route('/create', methods = ['PUT'])
def create():
    val = {'dsdfgs':'uhjdsgfkjsgd'}
    key = '1'
    temp.put(key,val)
    # print(temp.cache)
    with open('file.json', 'w') as f:
        dictionaries = [temp.cache]
        f.write(json.dumps(dictionaries))
    with open('file.json','r') as read_file:
        loaded_dict = json.loads(read_file.read())
        print(loaded_dict[0])
    # for i in temp:
    #     print(i)
    # return json.dumps(temp)
    return loaded_dict[0], 200

@app.route('/read',methods = ['PUT'])
def read():
    key = '1'
    val = temp.get(key)
    print(val)
    return jsonify(temp.cache), 200

@app.route('/delete', methods = ['PUT'])
def erase():
    key = 1
    temp.remove(key)
    return jsonify(temp.cache), 200