#!/usr/bin/python
import os
import time
import csv
import sqlite3 as mydb
import sys

""" Log Current Time, Temperature in Celsius and Fahrenheit
 Returns a list [time, tempC, tempF] """

def readTemp():
	tempfile = open("/sys/bus/w1/devices/28-000006974ebe/w1_slave")
	tempfile_text = tempfile.read()
	currentTime=time.strftime('%x %X %Z')
	tempfile.close()
	tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
	tempF=tempC*9.0/5.0+32.0
	return [currentTime, tempC, tempF]

def writeCsv():
	outfile = open('temperatureData.csv', 'a')
	writer = csv.writer(outfile, delimiter='|', quotechar="'", quoting=csv.QUOTE_ALL)
	writer.writerow(readTemp())

def writeToDatabase():
	con = None

	try:
		con = mydb.connect('temperature.db')
		cur = con.cursor()
		data = str(readTemp()).strip('[]')
		cur.execute('INSERT INTO tempData VALUES ('+data+');')
		con.commit()
                
	except mydb.Error, e:
    		print "Error %s:" % e.args[0]
    		sys.exit(1)
    
	finally:
   		if con:
        		con.close()


tempData = readTemp()
print "Current temperature: " + str(tempData[2]) + " F"
writeCsv()
writeToDatabase()
print "Temperature logged"