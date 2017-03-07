import requests 

files = {'h_file': open('file.txt','rb')}

r = requests.post("http://localhost:8000/hive/crack/", files=files)
print r.text