import urllib.request
import datetime
# url = urllib.request.urlopen('http://silverrb.lu.im.ntu.edu.tw/add.html')
# page = url.read()
# print(page)

url = 'http://silverrb.lu.im.ntu.edu.tw/add_v2.php'

myfile = open("read.txt","r") 
for line in myfile: 
	val = line.split();
	# print(len(val))

	t = datetime.datetime.fromtimestamp(float(val[0])/1000.)
	fmt = "%Y-%m-%d %H:%M:%S"
	finaltime=t.strftime(fmt)

	if len(val)<5:
		params = urllib.parse.urlencode({'inputtime':finaltime, 'xvalue':val[1], 'yvalue':val[2], 'zvalue':val[3]}).encode("utf-8")
		send = urllib.request.urlopen(url,params)
		# print ("1")
	else:
		commentStr=''
		i=4
		for i in range(4,len(val)):
			commentStr=commentStr+val[i]+" "
			i+=1
		params = urllib.parse.urlencode({'inputtime':finaltime, 'xvalue':val[1], 'yvalue':val[2], 'zvalue':val[3], 'memo':commentStr}).encode("utf-8")
		send = urllib.request.urlopen(url,params)
		# print ("2")
	# print (val[3]), 
