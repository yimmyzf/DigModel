#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import MySQLdb
import sys
import os

host=os.getenv('HOST_RD')
user = os.getenv('USER_RD')
passwd=os.getenv('PASSWD_RD')
db=os.getenv('DB_RD')
port=int(os.getenv('PORT_RD'))
charset=os.getenv('CHARSET_RD')
table1=os.getenv('COMMONLINETABLE_RD')
table2=os.getenv('MODELONLINETABLE_RD')


def formalizebrand(brand):
	brand = brand.strip()
	if '{|||}' in brand:
		tmplist = brand.split('{|||}')
	elif "/" in brand:
		tmplist = brand.split('/')
	elif " " in brand:
		tmplist = brand.split(' ')
	else:
		tmplist = [brand]
	
	for i in tmplist:
		if i in sysBranddict:
			brand=sysBranddict[i]
			break
		else:
			brand=tmplist[0]
	return brand
		

def forsysBrand():
	global sysBranddict
	sysBranddict={}
	for line in open('sysBrand.txt'):
		line=line.strip()
		(eng,chn)=line.split('\t')
		sysBranddict.setdefault(eng,chn)
		sysBranddict.setdefault(chn,chn)
		sysBranddict.setdefault(eng+chn,chn)
		sysBranddict.setdefault(chn+eng,chn)
	
def execute_for_CommInfo():
	fp = open("commData",'w')
	conn=MySQLdb.connect(host,user,passwd,db,port,charset)
	cursor = conn.cursor()

#	m = cursor.execute("select docid,title,inAppDataInfo from %s limit 1" % table1)
#	typeori= eval(cursor.fetchone()[2])["type"] #to find the keyword to match [attention encoding]
	typeori=" ÷ª˙"

	m = cursor.execute("select docid,title,inAppDataInfo,pid_low from %s" % table1)	
	for row in cursor.fetchall():
		docid = row[0]
		title = row[1].lower()
		inAppDataInfo = row[2]
		dict = eval(inAppDataInfo)
		model = dict["model"].lower()
		brand = dict["brand"].lower()
		brand = formalizebrand(brand)
		type1 = dict["type"]
		pid_low=row[3]
		if type1 == typeori:
			fp.write(str(docid)+'\t'+title+'\t'+model+'\t'+brand+'\t'+type1+'\t'+str(pid_low)+'\n')
#			print str(docid)+'\t'+title+'\t'+model+'\t'+brand+'\t'+type1
	fp.close()	
	cursor.close()
	conn.close()

def execute_for_ModelInfo():
	fp = open('modelInfo','w')
	
	conn=MySQLdb.connect(host,user,passwd,db,port,charset)
	cursor = conn.cursor()
	m = cursor.execute("select docid,model_new,model_ori from %s" % table2)
	for row in cursor.fetchall():
		docid = row[0]
		model_new = row[1]
		model_ori = row[2]
		fp.write(str(docid)+'\t'+model_new+'\t'+model_ori+'\n')
#		print str(docid)+'\t'+model_new+'\t'+model_ori
	fp.close()
	cursor.close()
	conn.close()
	
if __name__ == '__main__':
	forsysBrand()
	execute_for_CommInfo()
	execute_for_ModelInfo()
