from collections import OrderedDict
import json
import os
import calendar
import time

class LRUCache:


    def __init__(self):
        self.cache = OrderedDict()


    def get(self, key):
        if key not in self.cache:
            return 'NOT_FOUND' 
        else:
            time_now = calendar.timegm(time.gmtime()) #get the current time
            val = self.cache[key]
            if val['ttl'] is not False and val['ttl'] < time_now: # time for previous record expired
                self.remove(key)
                return 'NOT_FOUND'
            self.cache.move_to_end(key)
            return self.cache[key]


    def put(self, key, value):
        if self.cache.__sizeof__() > 1e9:
            self.cache.popitem(last = False)
        self.cache[key] = value
        self.cache.move_to_end(key)
        return True

    
    def remove(self, key):
        if key not in self.cache:
            return False
        self.cache.pop(key)
        return True

    def getCache(self):
        return self.cache

temp = LRUCache()


from flask import Flask,jsonify,request

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


INITIALISE = False
FILEPATH = None

def init():
    global INITIALISE
    global FILEPATH
    if not FILEPATH:
        FILEPATH = './file.json'
    try:
        with open(FILEPATH,'r') as f:
            try:
                x = json.loads(f.read())
                for k,v in x.items():
                    temp.put(k,v)
            except:
                pass
    except:
        abc = open(FILEPATH, 'a')
        abc.close()

def save_file():
    with open(FILEPATH, 'w') as f:
        f.write(json.dumps(temp.getCache()))

def time_to_live(ttl):
    return calendar.timegm(time.gmtime()) < ttl



@app.route('/set-path', methods=['POST'])
def initFile():
    global FILEPATH
    data = request.get_json()
    FILEPATH = os.path.join(data['filepath'], 'file.json')
    f = open(FILEPATH, 'w+')
    f.close()
    return jsonify(message = 'Filepath set successfully.',value = FILEPATH)

@app.route('/create', methods = ['POST'])
def create():

    init()

    data = request.get_json()
    value = data['val']
    key = data['key']

    try:
        ttl = data['ttl']
    except:
        ttl = False
    time_now = calendar.timegm(time.gmtime())
    val = {
        'data':value,
        'ttl': ttl
        }
    if val['ttl'] is not False:
        val = {
            'data': value,
            'ttl': ttl + time_now
        }
    flag = True
    if key in temp.getCache(): 
    # and (ttl is False or (ttl is not False and temp.getCache()[key]['ttl'] >= time_now)):
        # Case 1: prev is False and curr is True
        # Case 2: prev is False and curr is False
        # Case 3: prev is True and curr is True 
        # Case 4: prev is True and curr is False
        # Note: prev = temp.getCache()[key]['ttl']    curr = ttl
        # Case 1 and Case 2 done
        if temp.getCache()[key]['ttl'] is False or temp.getCache()[key]['ttl'] < time_now:
            flag = False

    else:
        flag = temp.put(key,val)
    if flag:
        save_file()
        return jsonify(message = 'Key value pair added.')
    else:
        return jsonify(message = 'Key is already present.')
        


@app.route('/read',methods = ['POST'])
def read():

    init()

    key = request.get_json()['key']
    val = temp.get(key)
    if val == "NOT_FOUND":
        save_file()
        return jsonify(message = 'Key not found.')
    else:
        return jsonify(message = 'Found.',value = val['data'])



@app.route('/delete', methods = ['POST'])
def erase():
    
    init()

    key = request.get_json()['key']
    time_now = calendar.timegm(time.gmtime())
    if key in temp.getCache() and temp.getCache()[key]['ttl'] is not False and temp.getCache()[key]['ttl'] < time_now: # Time expired for previous key
        val = temp.remove(key)
        save_file()
        return jsonify(message='Key not found.')
    val = temp.remove(key)
    save_file()
    if not val:
        return jsonify(message = 'Key not found.')
    else:
        save_file()
        return jsonify(message = 'Key successfully deleted.')




app.run(host='0.0.0.0', port=5000)
