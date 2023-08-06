# don't want shebang because the script will likely need a venv which may not be known by the script

import os
import sys
import time
import json

from watchdog.tricks import ShellCommandTrick, Trick

with open("/home/pi/ingress/config.json", "r") as file:
	config = json.loads(file.read())

WATCH_PATH = config.get('WATCH_PATH', '/home/pi/ingress/queue')
EXEC_FILE = config.get('EXEC_FILE', '/home/pi/ingress/src/exec-ingress.sh')
QUEUE_DIR = config.get('QUEUE_DIR', 'queue')


class CreateTrick(Trick):

	def on_any_event(self, event):
		pass

	def on_created(self, event):
		# type of 'event': FileCreatedEvent
		
		print('\nfound:', event.src_path)
		
		if QUEUE_DIR in event.src_path:
			# only execute command if item is in the queue directory
			os.system('/bin/bash %s %s'%(EXEC_FILE, event.src_path))
	



