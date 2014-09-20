#!/usr/bin/ev python
# -*- coding:utf-8 -*-

import sys
import copy

modeldict={}
docidmodeldict={}
branddict={}
tmpmap={}
titleSplitSet=set()
sysBrandSet=set()
docidmodeldictDeepcopy={}
	
def commBrandDict():
	global branddict
	for line in open('brandData'):
		try:
			line =line.strip()
			if len(line.split())==1:
				docid=line.split('\t')[0]
				branddict.setdefault(docid,[])
			else:
				docid,brand = line.split('\t',1)
				branddict.setdefault(docid,brand)
		except Exception,e:
			continue

def modeldict_and_docidmodellist():
	global docidmodeldict,modeldict
	for line in open('modelInfo'):
		line=line.strip()
#		docidmodellist.append(docid)
		if len(line.split())==1:
			docid=line.split('\t')[0]
			docidmodeldict.setdefault(docid,[])
		else:
			(docid,model_new,other) = line.split('\t',2)
			com_modellist=model_new.split('{|||}')
			docidmodeldict.setdefault(docid,com_modellist)
			for model in com_modellist:
				if model == '':
					continue
				else:
					if model in modeldict:
						modeldict[model].append(docid)
					else:
						modeldict.setdefault(model,[docid])
	global docidmodeldict2
	docidmodeldict2=copy.deepcopy(docidmodeldict)

#tmpmap={}
#titleSplitSet=set()
def executeSplitTitle(input,modeldict):
#	if input in modeldict:
#		tmpSplitSet.add(input)
#		return tmpSplitSet
	global tmpmap
	if input in tmpmap:
		return tmpmap[input]
	tmpSplitSet=set()
	length = len(input)
	for i in range(1,length+1):
		prefix = input[0:i]
		suffix = input[i:length]
		
		if prefix in modeldict:
			tmpSplitSet.add(prefix)
		if suffix=='':
			tmpmap.setdefault(prefix,tmpSplitSet)
			tmpSplitSet = set()
			return tmpmap[prefix]
		else:
			segSuffix = executeSplitTitle(suffix,modeldict)
			tmpSplitSet= tmpSplitSet|segSuffix

	
#	tmpmap.setdefault(input,set())
#	return set()
	
	
	
def dealWithTitle():#deal file CommonData_lower
	global tmpmap,modeldict,docidmodeldict,branddict 
	for line in sys.stdin:
		line = line.strip()
		docid = line.split('\t')[0]
		title = line.split('\t')[1]
		brand = line.split('\t')[3]
#		global tmpmap={}??
		tmpmap={}
		titleSplitSet=executeSplitTitle(title,modeldict)
		for word in titleSplitSet:
			if docid in docidmodeldict:
				if word in docidmodeldict[docid]:
					pass #alresy exist , no need to add
				else:
#					print 'aaaaaaaa',docid,word
					for i in modeldict[word]:
#						print i,brand,branddict[i]
						if brand==branddict[i]:
							docidmodeldict[docid].append(word)
							break
			else:
				for i in modeldict[word]:
					if brand==branddict[i]:
						docidmodeldict.setdefault(docid,[word])
						break	

def forsysBrandSet(): #using import from dataOperation
	global sysBrandSet
	for line in open('sysBrand.txt'):
		line=line.strip()
		(eng,chn)=line.split('\t')
		sysBrandSet.add(eng)
		sysBrandSet.add(chn)
		sysBrandSet.add(eng+'/'+chn)

					
def dealDocidModelDict():
	global docidmodeldict,sysBrandSet,docidmodeldictDeepcopy
	docidmodeldictDeepcopy=copy.deepcopy(docidmodeldict)
	for dockey in docidmodeldictDeepcopy:
		for i in docidmodeldictDeepcopy[dockey]:
			try:#maybe problem :after ***4 delete ***1 will not delete none factor
				if len(i.decode('gbk'))==1:#***1 remove single word model
					docidmodeldict[dockey].remove(i)
				elif i in sysBrandSet:# ***2 i is a brand name
					docidmodeldict[dockey].remove(i)	
				elif '/' in i:#***3 split chn&eng brand+model
					if len(i.split(' '))>1 :
						(mixbrand,mbtype)=i.split(' ',1)
						(engb,chnb)=mixbrand.split('/',1)
						docidmodeldict[dockey].remove(i)
						docidmodeldict[dockey].append(engb+' '+mbtype)
						docidmodeldict[dockey].append(chnb+' '+mbtype)
				else:
					pass
				if i[0:-1] in docidmodeldict[dockey]:#***4
					docidmodeldict[dockey].remove(i[0:-1])
			except Exception,e:
				continue
						
if __name__=='__main__':
	modeldict_and_docidmodellist()
	commBrandDict()
	dealWithTitle()
	forsysBrandSet()	
	dealDocidModelDict()
	
#	for i in docidmodeldict2.keys():
#		print i,docidmodeldict2[i]
#	for i in branddict.keys():
#		print i,branddict[i]	
	
#	for i in docidmodeldict.keys():
#		l=''
#		for model in docidmodeldict[i]:
#			l=l+'{|||}'+model
#		l=l.strip('{|||}')
#		print i+'\t'+l
	
	for doc in docidmodeldict:#uniq the models in docidmodeldict
		docidmodeldict[doc]={}.fromkeys(docidmodeldict[doc]).keys()
	for doc in docidmodeldict2:
		docidmodeldict2[doc]={}.fromkeys(docidmodeldict2[doc]).keys()
	for line in open('commData'):
		try:
			line = line.strip()
			(docid,title,model,brand,type,pid_low)=line.split('\t')
			if docid in docidmodeldict and docidmodeldict[docid]!= []:
				l1,l2='',''
				for model in docidmodeldict[docid]:
					l2=l2+'{|||}'+model
				for model in docidmodeldict2[docid]:#add up the origin model
					if model not in docidmodeldict[docid]:
						l2=l2+'{|||}'+model
				l2=l2.strip('{|||}')
				
				if docid in docidmodeldict2:
					for model in docidmodeldict2[docid]:
						l1=l1+'{|||}'+model
					l1=l1.strip('{|||}')
				print docid+'\t'+brand+'\t'+title+'\t'+l2+'\t'+l1+'\t'+pid_low
		except Exception:
			continue




	
