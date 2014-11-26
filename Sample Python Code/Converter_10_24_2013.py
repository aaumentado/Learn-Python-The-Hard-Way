#!/usr/bin/env python
#
# Converter_1_15_2013.py
# A simple script to dump the contents of a Microsoft Access dir.
# It depends upon the mdbtools suite:
#   http://sourceforge.net/projects/mdbtools/

import traceback
import sys, subprocess, os, MySQLdb, shutil
from datetime import datetime,timedelta
import time

SOURCE_DIR='/var/seeo/arbin'
SECOND_DEST_DIR = '/var/seeo/arbin/HighLevel/IgorInput'
RECORDS_DIR = '/var/seeo/arbin/convert_records.txt'
MAX_FILESIZE = 200 * 1048576 #bytes
FILE_LIMIT = 20 # after 20 files, end script

PREFIXES = ['L', 'EXC', 'SQC', 'GB']

CONVERT_RECORDS_HEADS = ['resfile', 'date_converted', 'res_filesize', 'csv_filesize']


connection = MySQLdb.connect(host='localhost', user='kohai', passwd='bM747k3T9WTsPYN382a5', db='seeo_mfg')
cursor = connection.cursor()


########################
# if in progress, exit #
########################

cursor.execute('SELECT message2 FROM debug WHERE script = "Converter" AND message = "Converter active?";')
res = cursor.fetchone()
if res[0] == 'yes':
        print 'Flag indicates script is already running'
	sys.exit()
elif res[0] == 'no':
        print 'Not running'
else:
        print res
        print 'script flag error...'
        sys.exit()
cursor.execute('UPDATE debug SET message2 = "yes" WHERE script = "Converter" AND message = "Converter active?";')

###############################
# if drive getting full, exit #
###############################

s = os.statvfs('/var/seeo/arbin')
mb_available = s.f_bsize * s.f_bavail/1048576.0 #megabytes
if mb_available < 500:
        print 'Less than 500MB available on drive'
        sys.exit()
        

########################
######## functions #####
########################

def sortRows(s):
        s = s.split('\n')
        print 'CONTAINS  ' + str(len(s)) + '  ROWS'
        head = s.pop(0)

        dict = {}
        new_s = ""
        for row in s:
                rowsplit = row.split(',')
                if len(rowsplit) == 18:
                        dict[int(rowsplit[1])] = row
        for k in sorted(dict.keys()):
                new_s += dict[k] + '\n'
        new_s = head + '\n' + new_s
                   
        return new_s


def getConvertRecords():
    f = open(RECORDS_DIR, 'r')
    s = f.read()
    convert_records = {}
    for row in s.split('\n')[1:]:
        row = row.split('\t')
        filename = row[0]
        date_converted = convertStringTimeToDatetime(row[1])
        res_filesize = float(row[2])
        csv_filesize = float(row[3])
        info = [filename, date_converted, res_filesize, csv_filesize]
        if filename in convert_records.keys():
            print 'duplicate file record'
            sys.exit()
        else:
            convert_records[filename] = info
    f.close()
    return convert_records


def overwriteRecords(convert_records):
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

def updateArbinMaps(arbin_channel_dict):
        
        for filename in arbin_channel_dict.keys():
                channel, schedule, start_date = arbin_channel_dict[filename]
                filename = filename.replace('"','')
                schedule = schedule.replace('"','')
                #convert start date from scientific notation#
                number, exp = str(start_date).split('e+')
                start_date = float(number)
                for i in range(int(exp)):
                        start_date = start_date * 10
                start_date = int(str(int(start_date)).split('.')[0]) #truncate to integer#
                start_date = datetime(1900, 1, 1) + timedelta(days=start_date)
                start_date = str(start_date).split(' ')[0]

                # delete duplicates from table, then insert #

                cursor.execute('DELETE FROM arbin_maps WHERE filename = "%s" AND channel = "%s" AND schedule = "%s"' % (filename, channel, schedule))
                cursor.execute('INSERT INTO arbin_maps (filename, channel, schedule, start_date) VALUES ("%s", "%s", "%s", "%s")' % (filename, channel, schedule, start_date))
                


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


###         begin conversion script         ###


arbindir_contents = [ea for ea in os.listdir(SOURCE_DIR) if ea[-4:] == ".res"]  # target filetype = '.res' #
print 'Found %d files! B-)' % (len(arbindir_contents))


convert_records = getConvertRecords()
convert_count = 0
arbin_channel_dict = {}

for resfile in arbindir_contents:

    if convert_count >= FILE_LIMIT:
        break

    print '--------------'
    print 'Now processing ' + resfile

    # determine whether to convert or delete #

    convert_it = True
    res_filesize = os.path.getsize(SOURCE_DIR + '/' + resfile)
    if res_filesize > MAX_FILESIZE:
        convert_it = False
        print 'File not converted because it exceeds MAX_FILESIZE'
    if resfile in convert_records.keys():
        previous_res_filesize = convert_records[resfile][CONVERT_RECORDS_HEADS.index('res_filesize')]
        if res_filesize <= previous_res_filesize:
            convert_it = False
            print 'File not converted because it was already converted'


    if convert_it == True or resfile == 'ET1-116A-RT1-1.res':   #use ET1-116A-RT1-1.res for testing#

        # Get the data from 'Channel_Normal_Table' in mdb file #
        
        #try:
        print 'Trying to open '
        print SOURCE_DIR + '/' + resfile
        contents_and_error = subprocess.Popen(["mdb-export", SOURCE_DIR + '/' + resfile, 'Channel_Normal_Table'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        contents = contents_and_error[0]
        error = contents_and_error[1]
        #except:
        #    cmd = 'insert into arbin_entries( barcode, debug )values( "{0}", "{1}" )'.format( resfile , 'exception on Popen' )
        #    cursor.execute( cmd )
        #    print 'bad contents'
        #    contents = False

        # determine prefix #
        
        prefix = 'Other'
        prefixes = PREFIXES
        for p in prefixes:
            if resfile.startswith(p):
                prefix = p
        if resfile.startswith('LW'):
            prefix = 'Other'
            
        # determine new filename #
        
        csvfile = resfile.split('.')[0] + '.csv'
        destination = SOURCE_DIR + '/' + prefix + '/' + csvfile

        # process data and write #

        if contents:
            contents = sortRows(contents)

            # write to CSV folder destination #
            
            f = open(destination, 'w')
            f.write(contents)
            f.close()
            try:
                os.system("chmod 777 %s" % (destination))
            except Exception, err:
                print 'Could not change permissions'
                print destination
                print str(err)
                cursor.execute('INSERT INTO debug (script, message, message2) VALUES ("Converter", "Failed to change permission %s", "%s")' % (destination, str(err)))

            # write to Igor input folder (SECOND_DEST_DIR) #
            
            f = open(SECOND_DEST_DIR + '/' + csvfile, 'w')
            f.write(contents)
            f.close()
            try:
                os.system("chmod 777 %s" % (SECOND_DEST_DIR + '/' + csvfile))
            except Exception, err:
                print 'Could not change permissions'
                print SECOND_DEST_DIR + '/' + csvfile
                print str(err)
                cursor.execute('INSERT INTO debug (script, message, message2) VALUES ("Converter", "Failed to change permission %s", "%s")' % (SECOND_DEST_DIR + '/' + csvfile, str(err)))

            # create new record of conversion #

            record = [resfile, datetime.now(), res_filesize, os.path.getsize(destination)]
            convert_records[resfile] = record

            print 'Conversion successful'
            convert_count += 1

        else:
            print 'no contents'

        # get data from Global_Table #
        
        global_table_contents = subprocess.Popen(["mdb-export", SOURCE_DIR + '/' + resfile, 'Global_Table'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        if global_table_contents:
                global_table_contents = global_table_contents.split('\n')

                heads = global_table_contents[0].split(',')
                lines = global_table_contents[1:]

                for line in lines:

                        line = line.split(',')
                        if len(line) >= heads.index('Start_DateTime'):

                                channel = line[heads.index('Channel_Index')]
                                schedule = line[heads.index('Schedule_File_Name')]
                                start_date = line[heads.index('Start_DateTime')]
                                arbin_channel_dict[resfile] = [channel,schedule, start_date]
        

        # delete res file #
        os.remove(SOURCE_DIR + '/' + resfile)

    else:
        # otherwise just delete it #
        os.remove(SOURCE_DIR + '/' + resfile)


if convert_count > 0:

        print '-------------------'

        # update arbin map #

        try:
                updateArbinMaps(arbin_channel_dict)
                print 'Arbin maps updated'
        except Exception, err:
                print 'ERROR: FAILED TO UPDATE ARBIN MAPS'
                print str(err)
                cursor.execute('INSERT INTO debug (script, message, message2) VALUES ("Converter", "Failed to update Arbin maps", "%s")' % (str(err)))

        # update convert records #

        try:
                overwriteRecords(convert_records)
                print 'Convert records updated'
        except Exception, err:
                print 'ERROR: FAILED TO OVERWRITE RECORDS'
                print str(err)
                cursor.execute('INSERT INTO debug (script, message, message2) VALUES ("Converter", "Failed to overwrite records", "%s")' % (str(err)))



# unflag script and close #
cursor.execute('UPDATE debug SET message2 = "no" WHERE script = "Converter" AND message = "Converter active?";')

cursor.close ()
connection.commit ()
connection.close ()
print 'Connection closed'

