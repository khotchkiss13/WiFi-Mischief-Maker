import sys

PY_PACKAGES = './pypackages'
sys.path.append(PY_PACKAGES)

import paramiko 
import threading

class workerThread (threading.Thread):
	def __init__(self, host, user):
		threading.Thread.__init__(self)
		self.client = paramiko.SSHClient()
		self.host = host
		self.user = user
		self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.client.connect(host, username=user)
	
	def run(self):		
		print "Starting run on host {}".format(self.host)
		self.worker_main()
		self.client.close()
		print "Finished run on host {} .... Exiting.".format(self.host)
	 
	def worker_main(self):
		'''Use this method to execute the main call to oclhashcat and return the results'''
		stdin, stdout, stderr = self.client.exec_command('sleep 10')
		lines = stdout.readlines()
		
#create new threads
login = input("What is your cs199 login: ")
thread1 = workerThread('hive2.cs.berkeley.edu', login)
thread2 = workerThread('hive3.cs.berkeley.edu', login)

thread1.start()
thread2.start()

threads = [thread1, thread2]

for t in threads:
    t.join()

print "Exit Main"	
	
