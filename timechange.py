import time
import datetime

s = '1487063988711'
t = datetime.datetime.fromtimestamp(float(s)/1000.)

fmt = "%Y-%m-%d %H:%M:%S"
print (t.strftime(fmt))