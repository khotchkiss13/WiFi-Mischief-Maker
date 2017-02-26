import sys

PY_PACKAGES = './pypackages'
sys.path.append(PY_PACKAGES)

import paramiko 
import threading
import getpass
import time

answer = None

class workerThread (threading.Thread):
	def __init__(self, host, user, number):
		threading.Thread.__init__(self)
		self.client = paramiko.SSHClient()
		self.host = host
		self.user = user
		self.number = number
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.client.connect(host, username=user)
	
	def run(self):		
		print "Starting run on host {}".format(self.host)
		self.worker_main()
		self.client.close()
		print "Finished run on host {} .... Exiting.".format(self.host)
	 
	def worker_main(self):
		'''Use this method to execute the main call to oclhashcat and return the results'''
		global answer
		stdin, stdout, stderr = self.client.exec_command(self.construct_string())
		lines = stdout.readlines()
		if answer == None:
			for line in lines:
				line = line.split(':')
				answer = line[-1]
		
	def construct_string(self):
		# return 'ls'
		return "./Downloads/hashcat-3.30/hashcat64.bin -m 2500 ./warring_hashcat-01.hccap ./passwords-" + str(self.number) + ".txt --force --quiet --show"

#create new threads
start = time.time()
login = getpass.getuser()
print("Logging in as " + login)
threads = []
current = 1
while current <= 30:
	if current == 16:
		current += 1
		continue
	try:
		thread = workerThread('hive'+str(current)+'.cs.berkeley.edu', login, current)
		thread.start()
		threads.append(thread)
	except:
		print("Could not connect to hive" + str(current))
	current += 1

for t in threads:
    t.join()

print "Result:"	
print answer
print ("Time elapsed: %s seconds" % (time.time() - start))
	
