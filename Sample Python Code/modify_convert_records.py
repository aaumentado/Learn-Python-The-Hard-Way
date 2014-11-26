#!/usr/bin/env python
#
# Convert Records Maintenance Script

import traceback
import sys, subprocess, os, shutil
from datetime import datetime,timedelta
import time

# string of the path directory to the convert_records.txt file
RECORDS_DIR = '/var/seeo/arbin/convert_records.txt'

# header line of the convert_records.txt file
CONVERT_RECORDS_HEADS = ['resfile', 'date_converted', 'res_filesize', 'csv_filesize']

# defines an array called RECORDS_TO_DELETE, each element of the array is a string
RECORDS_TO_DELETE = []

# HOW TO USE THIS SCRIPT: #

# Example:
# To delete L13-039-2_CT1-1.res from the convert records, set
# RECORDS_TO_DELETE = ['L13-039-2_CT1-1.res']
# (line 14)

# you can delete multiple files by separating the filenames with , see below:
# RECORDS_TO_DELETE = ['L13-039-2_CT1-1.res', 'L13-039-3_CT1-1.res']

# function to convert microsoft datetime to a string
# accepts value "lt"
def convertDatetimeToStringTime(lt):
	date_vals = lt.year, lt.month, lt.day
	time_vals = lt.hour, lt.minute, lt.second

	d, t = [], []

	for ea in date_vals:	
		ea = str(ea)
		if len(ea) == 1:
			ea = '0' + ea
		d.append(ea)
	for ea in time_vals:
		ea = str(ea)
		if len(ea) == 1:
			ea = '0' + ea
		t.append(ea)

	return '%s  %s' % ('/'.join(d), ':'.join(t))

def convertStringTimeToDatetime(stringtime):
	d, t = stringtime.split('  ')
	year, month, day = [ int(ea) for ea in d.split('/') ]
	hour, min, sec = [ int(ea) for ea in t.split(':') ]
	lt = datetime(year, month, day, hour, min, sec)
	return lt




try:
                
        # open records

        f = open(RECORDS_DIR, 'r')
        s = f.read()
        convert_records = {}

        for row in s.split('\n')[1:]:
            filename, date_converted, res_filesize, csv_filesize = row.split('\t')
            date_converted = convertStringTimeToDatetime(date_converted)
            info = [filename, date_converted, res_filesize, csv_filesize]
            convert_records[filename] = info
        f.close()

        # modify records

        modify_counter = 0
        
        for filename in convert_records.keys():

            if filename in RECORDS_TO_DELETE:
                
                print 'Found ' + filename
                del convert_records[filename]
                print 'Deleted ' + filename
                
        if modify_counter == 0:
                print 'No files were removed from the convert_records'
                
        # save modified records

        s = ['\t'.join(CONVERT_RECORDS_HEADS)]
        for k in convert_records.keys():
            filename, date_converted, res_filesize, csv_filesize = convert_records[k]
            date_converted = convertDatetimeToStringTime(date_converted)
            res_filesize = str(res_filesize)
            csv_filesize = str(csv_filesize)
            s.append('\t'.join([filename, date_converted, res_filesize, csv_filesize]))
        s = '\n'.join(s)
        f = open(RECORDS_DIR, 'w')
        f.write(s)
        f.close()
except Exception, err:
        print 'Error encountered'
        print str(err)
        
time.sleep(3600)


