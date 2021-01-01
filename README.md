# Key-value-lru
This is a file-based key-value data store that supports the basic CRD(create, read, delet) operations.
To use this, follow the following steps:
1. Clone this repo to your local machine
2. Run this code by "python main.py"
3. Open postman and tinker with the following options
    -- http://0.0.0.0:5000/set-path 
    This is a POST request. This is basically used to set the path of the file that will be our data store, by default the file gets saved to the root of this project directory.
    We can pass a json with "filepath" as a parameter to set our file path, like this
    {
    "filepath":"C:\\Users\\debjitdbb\\Documents\\Work\\Projects\\Freshworks"
    }

    -- http://0.0.0.0:5000/create
    This is a POST request. This is used to add a record to the data store. The json object should have the following parameters:
        -- "key" - str - The key for the datastore
        -- "val" - json - The value in json
        -- "ttl"(optional) - int (in secs) - The time(secs) for which the data will be stored in the datastore, after which it will be removed automatically
    For eg:
        {
        "key":"3",
        "val": {"message":"dfssdf dsfsdf sdfgdsf"},
        "ttl":3
        }


    --  http://0.0.0.0:5000/read
    This is a POST request. The json object takes the key and gives out the value. For eg:
    {
        "key":"3"
    }

    -- http://0.0.0.0:5000/delete
    This is a POST request. The json object takes the key and removes the element from the datastore. For eg:
    {
        "key":"3"
    }

I have used a LRU cache for this datastore which will just store 1gb of data in the memory and will omit the least recently used data when it surpasses the limit.
The entire process is thread safe which means that a client process is allowed to access the data from multiple threads.