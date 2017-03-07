import sys

PY_PACKAGES = './pypackages'
sys.path.append(PY_PACKAGES)

import paramiko 
import threading
import getpass
import time

answer = None
start = -1

def crack_password(hccap_filename, blacklist):
	global start
	start = time.time()

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
			self.worker_main()
			self.client.close()
		 
		def worker_main(self):
			'''Use this method to execute the main call to oclhashcat and return the results'''
			global answer
			global start
			stdin, stdout, stderr = self.client.exec_command(self.construct_string())
			lines = stdout.readlines()
			for line in lines:
				line = line.split(':')
				canidate = line[-1].strip()
				if len(canidate) > 0:
					print("Match found: " + canidate)
					print ("Time elapsed: %s seconds" % (time.time() - start))
					answer = canidate
			
		def construct_string(self):
			# return 'ls'
			return "./hashcat-" + str(self.number) + "/hashcat-3.30/hashcat64.bin -m 2500 ./" + hccap_filename + " ./passwords-" + str(self.number) + ".txt -w 3 --force --quiet --potfile-disable"

	#create new threads

	login = getpass.getuser()
	threads = []
	current = 1
	while current <= 30:
		if current in blacklist:
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

	return answer
