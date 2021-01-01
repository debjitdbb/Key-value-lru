import calendar
import time
x = calendar.timegm(time.gmtime())
ttl = 10
while True:
    if calendar.timegm(time.gmtime()) >= x + ttl :
        print("time is over")
        break