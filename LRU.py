from collections import OrderedDict
import json
import os

class LRUCache:


    def __init__(self):
        self.cache = OrderedDict()


    def get(self, key):
        if key not in self.cache:
            return 'NOT_FOUND' 
        else:
            self.cache.move_to_end(key)
            return self.cache[key]


    def put(self, key, value):
        if key in self.cache:
            return False 
        elif self.cache.__sizeof__() > 1e9:
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
    # FILEPATH = str(filepath) + 'file.json'
    if not FILEPATH:
        FILEPATH = './file.json'
    with open(FILEPATH,'r') as f:
        try:
            x = json.loads(f.read())
            for k,v in x.items():
                temp.put(k,v)
        except:
            pass
    INITIALISE = True


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
    if not INITIALISE:
        init()
    data = request.get_json()
    # data['data']['ttl'] = timestamp + data['data']['ttl']
    val = data['data']
    key = data['key']
    flag = temp.put(key,val)
    if flag:
        return jsonify(message = 'Key value pair added.')
    else:
        return jsonify(message = 'Key is already present.')


@app.route('/read',methods = ['POST'])
def read():
    if not INITIALISE:
        init()
    key = request.get_json()['key']
    val = temp.get(key)
    if val == "NOT_FOUND":
        return jsonify(message = 'Key not found.')
    else:
        return jsonify(message = 'Found.',value = json.dumps(val))

@app.route('/delete', methods = ['POST'])
def erase():
    if not INITIALISE:
        init()
    key = request.get_json()['key']
    val = temp.remove(key)
    if not val:
        return jsonify(message = 'Key not found.')
    else:
        return jsonify(message = 'Key successfully deleted.')


@app.route('/save', methods=['GET'])
def save():
    if not INITIALISE:
        return jsonify(message = 'Nothing to save.')
    with open(FILEPATH, 'w') as f:
        f.write(json.dumps(temp.getCache()))
    return jsonify(message = 'File saved')


app.run(host='0.0.0.0', port=5000)
