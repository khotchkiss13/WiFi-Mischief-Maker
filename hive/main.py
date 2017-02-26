import sys

PY_PACKAGES = './pypackages'
sys.path.append(PY_PACKAGES)

import paramiko 
import threading
import getpass

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
		for line in lines:
			line = line.split(':')
			if answer == None:
				answer = line[-1]
			else:
				if line[-1] != answer:
					print "Mulitple Answers: " + line[-1] 
		
	def construct_string(self):
		return "./hashcat-3.30/hashcat64.bin -m 2500 ./warring_hashcat-01.hccap ./passwords-" + str(self.number) + ".txt --force --quiet --show"

#create new threads
login = getpass.getuser()
print("Logging in as " + login)
threads = []
current = 2
while current <= 4:
	thread = workerThread('hive'+str(current)+'.cs.berkeley.edu', login, current)
	thread.start()
	threads.append(thread)
	current += 1

for t in threads:
    t.join()

print "Result:"	
print answer
	
