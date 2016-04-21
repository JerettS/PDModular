import sys
import os
import threading

from socket     import *
from time       import *  
from subprocess import *



PORT=8666
IP="127.0.0.1"
LOCATION = "./PdObjects/"
PUREDATA = "pd-extended"






class PD():
	def __init__(self):
		os.system("%s  %sserver.pd &" % (PUREDATA, LOCATION))
		self.modules = {}
		self.connections = {}
		self.UIDcounter = 0
		self.curX = 5
		self.curY = 5
		self.objectCount = 0

		#creates module and returns UID
	def create(self, name):
		msg = "pd-new obj %d %d %s \;" % (self.curX, self.curY,name)
		self.modules[self.UIDcounter] = [name,self.objectCount, self.curX, self.curY]
		curUID = self.UIDcounter
		self.UIDcounter += 1
		self.objectCount += 1
		self.curY += 30
		self.systemCall(msg)
		return curUID

	def connect(self, mod1ID, outputNum, mod2ID, inputNum):
		id1=self.getID(mod1ID)
		id2=self.getID(mod2ID)
		# self.connections[(mod1ID, outputNum, mod2ID, inputNum)] = cid
		msg = "pd-new connect %d %d %d %d \;" %  (id1, outputNum, id2, inputNum)
		self.systemCall(msg)
		# msg = "pd-new connect %d %d %d %d \;" %  (self.getID(cid), 0, )
		# self.systemCall(msg)

	def remove(self, modID):
		self.objectCount -= 1
		_,curid,x,y = self.modules[modID]
		msg = "pd-new editmode 1, mouse %d %d 0 0, mouseup %d %d 0, cut \;" % (max(0,x - 5), max(0,y - 5), x + 400, y + 25)
		self.systemCall(msg)
		del self.modules[modID]
		for i in self.modules.keys():
			(n, uid, x, y) = self.modules[i]
			if uid > curid:
				print "updating uids"
				self.modules[i] = (n, uid - 1, x, y)
		for (mod1ID, outputNum, mod2ID, inputNum) in self.connections.keys():
			if self.getID(mod1ID) == modID or self.getID(mod2ID) == modID:
				self.disconnect(mod1ID, outputNum, mod2ID, inputNum)

	def disconnect(self, uid):
		print "DISCONNECTING " + str(uid)
		for key in self.connections.keys():
			if uid == self.connections[keys]:
				del self.connections[key]
				self.remove(uid)
				return
		print "NOT FOUND IN PD"

	def disconnect(self, mod1ID, outputNum, mod2ID, inputNum):
		try:
			uid = self.connections[(mod1ID, outputNum, mod2ID, inputNum)]
			del self.connections[(mod1ID, outputNum, mod2ID, inputNum)]
			self.remove(uid)
		except (KeyError):
			print "DISCONNECT PROBLEM"


	def getID(self, modID):
		if modID in self.modules.keys():
			_,uid,_,_ = self.modules[modID]
			return uid
		return -1

	def systemCall(self, msg):
		#print "MESAGE IS " + msg
		os.system(" echo %s | pdsend %d" % (msg, PORT))
		
	def kill(self):

		os.system("pkill Pd-extended" )

	def save(self):
		msg = "pd-new menusaveas \;" 
		self.systemCall(msg)



