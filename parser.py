# ! usr/bin/env python
# ryuuu

from pwn import *
import re


f=open("./$MFT.copy0",'rb')

def hex_ch(buf,num):
	string=''
	i=num
	while i>=0:
		string += "%02X" % (ord(buf[i]))
		i=i-1

	return string


def entry_header():
	entry_header=entry[:48]
	sig=entry_header[0:4]
	off_fixup_buf=entry_header[4:6]
	entries_fixup_array_buf=entry_header[6:8]	

	Offset_to_fixup_array = int(hex_ch(off_fixup_buf,1),16)
	entries_fixup_array = int(hex_ch(entries_fixup_array_buf,1),16)
	
	return Offset_to_fixup_array+entries_fixup_array+6

def header_property(num):
	if num <= 984:
#		print num
		property_con_buf = entry[num:num+4]
		property_len_buf = entry[num+4:num+8]

		property_con = int(hex_ch(property_con_buf,3),16)
		property_len = int(hex_ch(property_len_buf,3),16)

		resident = num+16
	
		property_info_size_buf = entry[resident:resident+4]
		property_info_offset_buf = entry[resident+4:resident+6]

		property_info_size = int(hex_ch(property_info_size_buf,3),16)
		property_info_offset = int(hex_ch(property_info_offset_buf,1),16)

		property_info_offset=num+property_info_offset			
		property_size=num+property_len

		if property_len > 0:
			
			if property_con==0x10:
				std_information(property_size,property_info_offset)
			elif property_con==0x30:
				filename(property_size,property_info_offset)
			elif property_con==0x80:
				data(property_size,property_info_offset)
			else :
				other(property_size,property_info_offset)

def std_information(size, offset):
#	print "std information"

	file_create_time_buf = entry[offset:offset+8]
	file_create_time = int(hex_ch(file_create_time_buf,7),16)	
#	date_create_time = filetime_to_dt(file_create_time)

	print "create_time : "+str(hex(file_create_time))
	header_property(size)

def filename(size, offset):
	pattern = "\x00"
	filename_len_buf = entry[offset+64:offset+65]
	
	filename_len = int(hex_ch(filename_len_buf,0),16)
	
	filename = entry[offset+66:offset+66+(filename_len*2)]
	filename=re.sub(pattern,'',filename)

#	print "filename!!"
#	print "file name len : "+str(filename_len)
	print "file name : "+filename
	header_property(size)

def data(size, offset):
	print "data"
	header_property(size)

def other(size, offset):
#	print "else"
	header_property(size)

while 1:
	entry=f.read(1024)
	entrylen = len(entry) 
	if entrylen == 0: break
	header_property(entry_header()-1)
#	print "cycle!!"
	pause()
f.close()