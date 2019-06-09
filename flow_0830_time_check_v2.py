#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 17:56:03 2018

@author: caca
"""


# argv[1] = 'C:/Users/caca/Documents/CAD_Contest_2018_A/cases8/test_names.json'
# agrv[2] = 'C:/Users/caca/Documents/CAD_Contest_2018_A/cases8/testtmpout.json'




#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# just a brutal mapping version

import json
import sys
import zlib
import bz2
import re
import base64
import time

# timer start
t_start = time.time()
t_start_plus_29m = t_start + 29*60 + 40
t_now = time.time()







def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(l, key=alphanum_key)




# pure Run-Length Encode, comma
# element,repeat_count
#
# input: offset list
# output: offset list, with RLE representation

def pureRLE_encode(input_list):
    repeat_count = 1
    prev = input_list[0]
    tmp_list = [] 
    
    for element_index in range(1,len(input_list)):
        if(input_list[element_index] != prev):
            entry = (prev,repeat_count)
            tmp_list.append(entry)
            #
            repeat_count = 1
            prev = input_list[element_index]
        else:
            repeat_count += 1
    else:
        entry = (prev,repeat_count)
        tmp_list.append(entry)
        
    return tmp_list


#
# pure Run-Length Decode
# input: str compress by pure RLE
# process: 
# output: offset once list, type(element) = int  
def pRLEstr_o1_decoder(input_str):
    tmp_list = input_str.split(",")
    e = []
    for t_index in range(0,len(tmp_list),2):
        for r_time in range(int(tmp_list[t_index+1])):
            e.append(int(tmp_list[t_index]))
    return e



# bias Run-Length Encode, comma version
# 
# input: offset list (with int element)
# output: offset list with bias RLE representation

def biasRLE_encode(input_list):

    repeat_count = 1
    prev = input_list[0]
    bias = prev   # bias 0
    tmp_list = [] 
    
    for element_index in range(1,len(input_list)):
        if(input_list[element_index] != prev):
            entry = (bias,repeat_count)
            tmp_list.append(entry)
            #
            repeat_count = 1
            prev = input_list[element_index] 
            bias = input_list[element_index] - input_list[element_index-1]
            
        else:
            repeat_count += 1
    else:
        # append last one
        entry = (bias,repeat_count)
        tmp_list.append(entry)
        
    return tmp_list



#
# bias Run-Length Decode  
# 
# input: str compress by bias RLE
# output: offset once list
def bRLEstr_o1_decoder(input_str):
    tmp_list = input_str.split(",")
    e=[]
    current_value = 0
    for t_index in range(0,len(tmp_list),2):
        current_value += int(tmp_list[t_index])
        for r_time in range(int(tmp_list[t_index+1])):
            e.append(current_value)
    return e



#
# pure Run-Length Decode for offset-twice
#
# input: str compressed by pure RLE from offset-twice index set
# output: offset once list
def pRLEstr_o2_decoder(input_str):
    tmp_list = input_str.split(",")
    e=[]
    current_value = 0
    for t_index in range(0,len(tmp_list),2):        
        for r_time in range(int(tmp_list[t_index+1])):
            current_value += int(tmp_list[t_index])
            e.append(current_value)
    return e





# evaluator
"""
input: index string that only apply one offset operation (qq/zz)
output:
    compressed binary string
    compress_mode = 'zlib' or 'bz2'
    rle_mode = 'pureRLE' or 'biasRLE' 
    offset_mode = '1' or '2'
"""

def evaluatorAll(input_str):
    
    # transform str->list, seperate by ","
    # input_list = input_str.split(",")
    
    # transfrom type(element) in list from str to int
    # offset*1 version
    input_list =[int(x) for x in input_str.split(',')]
    
    # get offset_twice list
    input_list_offset2 = []
    #
    input_list_offset2.append(input_list[0])
    for i in range(1,len(input_list)):
        input_list_offset2.append(input_list[i]-input_list[i-1])
    
    
    
    # initialize str
    pureRLE_o1_str = ''
    biasRLE_o1_str = ''
    pureRLE_o2_str = ''
    
    
    #
    # pureRLE, offset once:
    tmp_list = pureRLE_encode(input_list)
    # construct pureRLE_o1_str
    for element,repeat_count in tmp_list:
        pureRLE_o1_str += str(element) + ',' + str(repeat_count) + ','
    pureRLE_o1_str = pureRLE_o1_str[:-1]
    
    
    #
    # bias RLE, offset once:
    tmp_list = biasRLE_encode(input_list)
    # construct biasRLE_o1_str
    for element,repeat_count in tmp_list:
        biasRLE_o1_str += str(element) + ',' + str(repeat_count) + ','
    biasRLE_o1_str = biasRLE_o1_str[:-1]
    
    
    #
    # pure RLE, offset twice
    tmp_list = pureRLE_encode(input_list_offset2)
    # construct pureRLE_o2_str
    for element,repeat_count in tmp_list:
        pureRLE_o2_str += str(element) + ',' + str(repeat_count) + ','
    pureRLE_o2_str = pureRLE_o2_str[:-1]
    


    # show information

    #'''
    ##number of char of each append string 
    #from not include p2(sort or natural sort) & p5(intact or prune)
    #'''
    
    nc_zlib = 48
    nc_bz2 = 47
    nc_prle_o1_decode = 103
    nc_brle_o1_decode = 115
    nc_prle_o2_decode = 116
    
    
    #print('--------------------------------------------------')
    #print('--------------------------------------------------')
    #print('\ncompressed by zlib + base64.b64')
    
    # compress the str by zlib + base64.b64encode()
    pureRLE_o1_str333 = base64.b64encode( zlib.compress(str(pureRLE_o1_str).encode('utf-8'), 9) )
    biasRLE_o1_str333 = base64.b64encode( zlib.compress(str(biasRLE_o1_str).encode('utf-8'), 9) )
    pureRLE_o2_str333 = base64.b64encode( zlib.compress(str(pureRLE_o2_str).encode('utf-8'), 9) )

    
    # len of compressed str (includes upzip & RLdecode)
    len_pureRLE_o1_str333 = len(str(pureRLE_o1_str333)) + nc_zlib + nc_prle_o1_decode #case0
    len_biasRLE_o1_str333 = len(str(biasRLE_o1_str333)) + nc_zlib+ nc_brle_o1_decode #case1
    len_pureRLE_o2_str333 = len(str(pureRLE_o2_str333)) + nc_zlib+ nc_prle_o2_decode #case2
    
    
    #'''
    #not include nc_sort/nc_natural_sort !!!!!!!!!!!!!
    #'''
    #print('pureRLE_o1_str333: ')
    #print(len_pureRLE_o1_str333)
    #print('--')
    #
    #print('biasRLE_o1_str333: ')
    #print(len_biasRLE_o1_str333)
    #print('--')
    #
    #print('pureRLE_o2_str333: ')
    #print(len_pureRLE_o2_str333)
    #print('--')

    
    
    #print('--------------------------------------------------')
    #print('\ncompressed by bz2 + base.b64')
    
    # compress the str by bz2
    pureRLE_o1_str444 = base64.b64encode( bz2.compress(str(pureRLE_o1_str).encode('utf-8'), 9) )
    biasRLE_o1_str444 = base64.b64encode( bz2.compress(str(biasRLE_o1_str).encode('utf-8'), 9) )
    pureRLE_o2_str444 = base64.b64encode( bz2.compress(str(pureRLE_o2_str).encode('utf-8'), 9) )
    
    # len of compressed str (includes upzip & RLdecode)
    len_pureRLE_o1_str444 = len(str(pureRLE_o1_str444)) + nc_bz2+ nc_prle_o1_decode #case3
    len_biasRLE_o1_str444 = len(str(biasRLE_o1_str444)) + nc_bz2+ nc_brle_o1_decode #case4
    len_pureRLE_o2_str444 = len(str(pureRLE_o2_str444)) + nc_bz2+ nc_prle_o2_decode #case5

    #print('pureRLE_o1_str444: ')
    #print(len_pureRLE_o1_str444)
    #print('--')
    #
    #print('biasRLE_o1_str444: ')
    #print(len_biasRLE_o1_str444)
    #print('--')
    #
    #print('pureRLE_o2_str444: ')
    #print(len_pureRLE_o2_str444)
    #print('--')
    
    #print('--------------------------------------------------')
    #print('\n')

     
    #
    # compare
    # return value initialize
    output_compressed_str = ''
    compress_mode = ''
    rle_mode = ''
    offset_mode = ''
    num_char_in_script = ''
    
    #
    size_list = [len_pureRLE_o1_str333, len_biasRLE_o1_str333, len_pureRLE_o2_str333, len_pureRLE_o1_str444, len_biasRLE_o1_str444, len_pureRLE_o2_str444]
    min_size = size_list[0]
    min_case = 0
    for i in range(len(size_list)):
        if(size_list[i]<min_size):
            min_case = i
            min_size = size_list[i]
            
    '''
    test
    '''
    # min_case=0
    

    if min_case == 0:
        output_compressed_str = pureRLE_o1_str333
        compress_mode = 'zlib'
        rle_mode = 'pureRLE'
        offset_mode = 'once'
        num_char_in_script = len_pureRLE_o1_str333
        
    elif min_case ==1:
        output_compressed_str = biasRLE_o1_str333
        compress_mode = 'zlib'
        rle_mode = 'biasRLE'
        offset_mode = 'once'
        num_char_in_script = len_biasRLE_o1_str333
        
    elif min_case ==2:
        output_compressed_str = pureRLE_o2_str333
        compress_mode = 'zlib'
        rle_mode = 'pureRLE'
        offset_mode = 'twice'
        num_char_in_script = len_pureRLE_o2_str333
            
    elif min_case == 3:
        output_compressed_str = pureRLE_o1_str444
        compress_mode = 'bz2'
        rle_mode = 'pureRLE'
        offset_mode = 'once'
        num_char_in_script = len_pureRLE_o1_str444
        
    elif min_case == 4:
        output_compressed_str = biasRLE_o1_str444
        compress_mode = 'bz2'
        rle_mode = 'biasRLE'
        offset_mode = 'once'
        num_char_in_script = len_biasRLE_o1_str444
        
    elif min_case == 5:
        output_compressed_str = pureRLE_o2_str444
        compress_mode = 'bz2'
        rle_mode = 'pureRLE'
        offset_mode = 'twice'
        num_char_in_script = len_pureRLE_o2_str444



    return output_compressed_str, compress_mode, rle_mode, offset_mode, num_char_in_script

#
# end of the evaluator
    




"""
Write File!!

"""

size_complete_align_NaturalSort = 227
size_complete_align_Sort = 111
size_complete_align_NaturalSort_prune = 362
size_complete_align_Sort_prune = 227


# natural sort 
#---227
str_complete_align_NaturalSort ='''import sys,json as j,re
def s(l):
 a=lambda d:int(d)if d.isdigit()else d
 return sorted(l,key=lambda key:[a(c)for c in re.split('([0-9]+)',key)])
k=sys.argv
i=j.load(open(k[1]))
j.dump(dict(zip(s(i[0]),s(i[1]))),open(k[2],'w'))'''


#---111
str_complete_align_Sort ='''import sys,json as j
s=sorted
k=sys.argv
i=j.load(open(k[1]))
j.dump(dict(zip(s(i[0]),s(i[1]))),open(k[2],'w'))'''

#---362
str_complete_align_NaturalSort_prune='''import sys,json as j,re
def s(l):
 a=lambda d:int(d) if d.isdigit() else d.lower() 
 b=lambda key:[a(c) for c in re.split('([0-9]+)', key)] 
 return sorted(l,key=b)
k=sys.argv
i=j.load(open(k[1]))
p={q:0 for q in i[0]}
r={q:q for q in[g for g in i[1] if g in p]if(i[0].remove(q),i[1].remove(q))}
t = p.keys()
j.dump(dict(zip(s(i[0])+t,s(i[1])+t)),open(k[2],'w'))'''


#---227
str_complete_align_Sort_prune='''import sys,json as j
s=sorted
k=sys.argv
i=j.load(open(k[1]))
p={q:0 for q in i[0]}
r={q:q for q in[g for g in i[1] if g in p]if(i[0].remove(q),i[1].remove(q))}
t = p.keys()
j.dump(dict(zip(s(i[0])+t,s(i[1])+t)),open(k[2],'w'))'''




#-------------------------------------------
# for original last3

#--47
str_append_p2_sort_zlib = '''
import sys,json as j,zlib
s=sorted
k=sys.argv
'''

#--47
str_append_p2_sort_bz2 = '''
import sys,json as j,bz2
s=sorted
k=sys.argv
'''

#---185
str_append_p2_natural_sort_zlib = '''
import sys,json as j,re,base64,zlib
def s(l):
 a=lambda d:int(d)if d.isdigit()else d
 return sorted(l,key=lambda key:[a(c)for c in re.split('([0-9]+)',key)])
k=sys.argv
'''


#---185
str_append_p2_natural_sort_bz2 = '''
import sys,json as j,re,base64,bz2
def s(l):
 a=lambda d:int(d)if d.isdigit()else d
 return sorted(l,key=lambda key:[a(c)for c in re.split('([0-9]+)',key)])
k=sys.argv
'''

#---48
str_append_p3_unzip_zlib = 'h=zlib.decompress(base64.b64decode(e)).decode()'
#---47
str_append_p3_unzip_bz2 = 'h=bz2.decompress(base64.b64decode(e)).decode()'


#---103
str_append_p4_pRLE_to_o1_list ='''
m=h.split(",")
e=[]
for t in range(0,len(m),2):
	for r in range(int(m[t+1])):
		e.append(int(m[t]))
'''


#---115
str_append_p4_bRLE_to_o1_list ='''
m=h.split(",")
e=[]
v=0
for t in range(0,len(m),2):
	v+=int(m[t])
	for r in range(int(m[t+1])):
		e.append(v)
'''


#---116
str_append_p4_pRLE_to_o2_list ='''
m=h.split(",")
e=[]
v=0
for t in range(0,len(m),2):
	for r in range(int(m[t+1])):
        v+=int(m[t])
        e.append(v)
'''


#---232
str_append_p5_last = '''
i=j.load(open(k[1]))
j.dumps(i)
a=s(i[0])
b=s(i[1])
f=open(k[2],'w')
f.write('{')
for i in range(len(a)):
	f.write('"')
	f.write(a[i])
	f.write('":"')
	f.write(b[i+e[i]])
	if i==len(a)-1:f.write('"}')
	else:f.write('",')
'''

#---165    
str_append_p5_intact_compact = '''i=j.load(open(k[1]))
j.dumps(i)
a=s(i[0])
b=s(i[1])
f=open(k[2],'w')
w='{'
for i in range(len(a)):
	w+='"'+a[i]+'":"'+b[i+e[i]]+'",'
w=w.strip(',')
w+='}'
f.write(w)'''


#---281
str_append_p5_prune_compact='''i=j.load(open(k[1]))
j.dumps(i)
p={q:0 for q in i[0]}
r={q:q for q in[g for g in i[1] if g in p]if(i[0].remove(q),i[1].remove(q))}
t = p.keys()
a=s(i[0])+t
b=s(i[1])+t
f=open(k[2],'w')
w='{'
for i in range(len(a)):
	w+='"'+a[i]+'":"'+b[i+e[i]]+'",'
w=w.strip(',')
w+='}'
f.write(w)'''



###########################################################################






# compare length


same_index1 = 0
same_index1_prune = 0
same_index2 = 0
same_index2_prune = 0
same_name = 0
write_mode = 0




'''
2018/08/29 HT

'''



set1 = []
set2 = []
set1_copy = []
set2_copy = []

index_table = [] 


# read file
local_data_path = sys.argv[1] # lalalalalala
file = open(local_data_path, 'r')
count = 0
for line in file:
	words = line.split()
	for w in words:
		if w != "{":
			if w != "}":
				w = w.replace('"','')
				w = w.replace(',','')
				w = w.replace(':','')
				if count%2 == 0:
					set1.append(w)
				else:
					set2.append(w)
			count = count + 1
file.close()
with open(local_data_path, 'r') as f:
    json_dict = json.loads(f.read())  #dict
f.close()



'''
set1, set2 copy for prune list
'''


#put ABBC test here

ABBC = False #default
for i in range(len(set1)):
    if set1[i]!=set2[i]:
        if set1[i] in set2:
            ABBC = True
            break # 
    else:
        set1_copy.remove(set1[i])
        set2_copy.remove(set2[i])

passABBCtest = not ABBC


#
complete_align_NaturalSort = False
complete_align_Sort = False
complete_align_NaturalSort_prune = False
complete_align_Sort_prune = False

#num char in str
nc_p2_sort = 47
nc_p2_natural_sort = 185
nc_p5_last_intact = 165
nc_p5_last_prune = 281 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


# 
min_script_size = 0
output_script_str = ''
#
current_script_size = 0
current_script_str = ''





    
# checkpoint: get natural sort ,pruning 
zz_prune=''
if(passABBCtest == True):
    
    # Natural sort of pruning set
    set11 = natural_sort(set1_copy)
    set22 = natural_sort(set2_copy)
    
    for i in range(len(set1_copy)):
    	if i == set22.index(json_dict[set11[i]]):
    		same_index2_prune = same_index2_prune + 1
    		
    if same_index2_prune == len(set1_copy) :
    	complete_align_NaturalSort_prune = True
    	
    	
    for i in range(len(set1_copy)):	
    			index_table.append(set22.index(json_dict[set11[i]]))
    
    #zz_prune=''
    for i in range(len(index_table)):
    	if(i == len(index_table) - 1): 
    		zz_prune+=str(index_table[i]-i)
    	else:
    		zz_prune+=str(index_table[i]-i)
    		zz_prune+=','

index_table.clear()



#checkpoint: complete align , Natural sort , pruned set
if(passABBCtest == True and complete_align_NaturalSort_prune == True):
    
    # write file
    f = open(sys.argv[2], 'w+')
    f.write(str_complete_align_NaturalSort_prune)
    f.close()
    min_script_size = size_complete_align_NaturalSort_prune
    



#checkpoint: partial align, Natural sort, pruned set
if(passABBCtest == True and complete_align_NaturalSort == False ):
    zz_output_compressed_str, zz_compress_mode, zz_rle_mode, zz_offset_mode, part_of_script_size = evaluatorAll(zz_prune)
    
    # size check
    current_script_size = part_of_script_size + 2 + nc_p2_natural_sort + nc_p5_last_prune
    min_script_size = current_script_size

    # write file
    # natural sort, prune file
    f = open(sys.argv[2], 'w+')
    f.write('e=')
    f.write(str(zz_output_compressed_str))
    #
    if(zz_compress_mode == 'zlib'):
        f.write(str_append_p2_natural_sort_zlib)
        f.write(str_append_p3_unzip_zlib)
    elif(zz_compress_mode == 'bz2'):
        f.write(str_append_p2_natural_sort_bz2)
        f.write(str_append_p3_unzip_bz2)

    #
    if(zz_rle_mode == 'pureRLE' and zz_offset_mode == 'once' ):
        f.write(str_append_p4_pRLE_to_o1_list)
    elif(zz_rle_mode == 'biasRLE' and zz_offset_mode == 'once'):
        f.write(str_append_p4_bRLE_to_o1_list)
    elif(zz_rle_mode == 'pureRLE' and zz_offset_mode == 'twice'):
        f.write(str_append_p4_pRLE_to_o2_list)

    f.write(str_append_p5_prune_compact)
    f.close()
        
# end



#
# Natural sort
set11 = natural_sort(set1)
set22 = natural_sort(set2)

for i in range(len(set1)):
	if i == set22.index(json_dict[set11[i]]):
		same_index2 = same_index2 + 1
		
if same_index2 == len(set1) :
	complete_align_NaturalSort = True
	
	
for i in range(len(set1)):	
			index_table.append(set22.index(json_dict[set11[i]]))

zz=''
for i in range(len(index_table)):
	if(i == len(index_table) - 1): 
		zz+=str(index_table[i]-i)
	else:
		zz+=str(index_table[i]-i)
		zz+=','

index_table.clear()
	
#
min_script_size = len(zz) +1000000





# checkpoint: complete align in Natural Sort, full set
# 
if(complete_align_NaturalSort == True):
    
    t_now = time.time()

    if(size_complete_align_NaturalSort < min_script_size and t_now < t_start_plus_29m):
        f = open(sys.argv[2], 'w+')
        f.write(str_complete_align_NaturalSort)
        f.close()
        #
        min_script_size = size_complete_align_NaturalSort 




# checkpoint : partily align ,natural Sort, full set
if(complete_align_NaturalSort == False):
    zz_output_compressed_str, zz_compress_mode, zz_rle_mode, zz_offset_mode, part_of_script_size = evaluatorAll(zz)
    current_script_size = part_of_script_size + 2 + nc_p2_natural_sort + nc_p5_last_intact
    
    
    t_now = time.time()
    
    if(current_script_size < min_script_size and t_now < t_start_plus_29m):
        #
        min_script_size = current_script_size
        #
        #
        # write file
        # natural sort, full
        f = open(sys.argv[2], 'w+')
        f.write('e=')
        f.write(str(zz_output_compressed_str))
        #
        if(zz_compress_mode == 'zlib'):
            f.write(str_append_p2_natural_sort_zlib)
            f.write(str_append_p3_unzip_zlib)
        elif(zz_compress_mode == 'bz2'):
            f.write(str_append_p2_natural_sort_bz2)
            f.write(str_append_p3_unzip_bz2)
    
        #
        if(zz_rle_mode == 'pureRLE' and zz_offset_mode == 'once' ):
            f.write(str_append_p4_pRLE_to_o1_list)
        elif(zz_rle_mode == 'biasRLE' and zz_offset_mode == 'once'):
            f.write(str_append_p4_bRLE_to_o1_list)
        elif(zz_rle_mode == 'pureRLE' and zz_offset_mode == 'twice'):
            f.write(str_append_p4_pRLE_to_o2_list)
    
        
        f.write(str_append_p5_intact_compact)
        f.close()
    


# checkpoint
# sort full set
set11 = sorted(set1)
set22 = sorted(set2)


for i in range(len(set1)):
	if i == set22.index(json_dict[set11[i]]):
		same_index1 = same_index1 + 1
		
if same_index1 == len(set1) :
	complete_align_Sort = True
	
for i in range(len(set1)):	
			index_table.append(set22.index(json_dict[set11[i]]))
			
qq=''
for i in range(len(index_table)):
	if(i == len(index_table) - 1): 
		qq+=str(index_table[i]-i)
	else:
		qq+=str(index_table[i]-i)
		qq+=','
			
index_table.clear()



# checkpoint: complete align, sort, full set
if(complete_align_Sort == True):
    # write
    f = open(sys.argv[2], 'w+')
    f.write(str_complete_align_Sort)
    f.close()
    min_script_size = size_complete_align_Sort

    

# checkpoint: partily align, sort, full set
if(complete_align_Sort == False):
    
    qq_output_compressed_str, qq_compress_mode, qq_rle_mode, qq_offset_mode, part_of_script_size = evaluatorAll(qq)
    
    #size check
    current_script_size = part_of_script_size + 2 + nc_p2_sort + nc_p5_last_intact
    t_now = time.time()
    if(current_script_size < min_script_size and t_now < t_start_plus_29m):
        min_script_size = current_script_size
        #
        #
        # write file
        # natural sort, full
        f = open(sys.argv[2], 'w+')
        f.write('e=')
        f.write(str(qq_output_compressed_str))
        #

        if(qq_compress_mode == 'zlib'):
            f.write(str_append_p2_sort_zlib)
            f.write(str_append_p3_unzip_zlib)
        elif(qq_compress_mode == 'bz2'):
            f.write(str_append_p2_sort_bz2)
            f.write(str_append_p3_unzip_bz2)

        #
        if(qq_rle_mode == 'pureRLE' and qq_offset_mode == 'once' ):
            f.write(str_append_p4_pRLE_to_o1_list)
        elif(qq_rle_mode == 'biasRLE' and qq_offset_mode == 'once'):
            f.write(str_append_p4_bRLE_to_o1_list)
        elif(qq_rle_mode == 'pureRLE' and qq_offset_mode == 'twice'):
            f.write(str_append_p4_pRLE_to_o2_list)

        
        f.write(str_append_p5_intact_compact)
        f.close()
    
    #
    
    
        
    
#############
        
        
# check point: get prune set of qq
qq_prune=''
if(complete_align_Sort == False and passABBCtest == True):
    
    # Natural sort of pruning set
    set11 = sorted(set1_copy)
    set22 = sorted(set2_copy)
    
    for i in range(len(set1_copy)):
    	if i == set22.index(json_dict[set11[i]]):
    		same_index1_prune = same_index1_prune + 1
    		
    if same_index1_prune == len(set1_copy) :
    	complete_align_Sort_prune = True
    	
    	
    for i in range(len(set1_copy)):	
    			index_table.append(set22.index(json_dict[set11[i]]))
    
    #zz_prune=''
    for i in range(len(index_table)):
    	if(i == len(index_table) - 1): 
    		qq_prune+=str(index_table[i]-i)
    	else:
    		qq_prune+=str(index_table[i]-i)
    		qq_prune+=','

index_table.clear()


#################



# checkpoint: complete align, sort, prune set
if(complete_align_Sort == False and complete_align_Sort_prune == True and passABBCtest == True):
    t_now = time.time()
    #'''
    if(size_complete_align_Sort < min_script_size and t_now < t_start_plus_29m):
        # write file
        f = open(sys.argv[2], 'w+')
        f.write(str_complete_align_Sort_prune)
        f.close()
        min_script_size = size_complete_align_Sort_prune
    #'''
    #print('laaaaaaaaaaaaaaaa, lack of str_complete_align_Sort_prune')
    


# checkpoint: partially align, sort, prune set
if(complete_align_Sort == False and passABBCtest == True):
    
    qq_output_compressed_str, qq_compress_mode, qq_rle_mode, qq_offset_mode, part_of_script_size = evaluatorAll(qq)
    
    #size check
    current_script_size = part_of_script_size + 2 + nc_p2_sort + nc_p5_last_prune
    t_now = time.time()
    if(current_script_size < min_script_size and t_now < t_start_plus_29m):
        min_script_size = current_script_size
        #
        #
        # write file
        # natural sort, full
        f = open(sys.argv[2], 'w+')
        f.write('e=')
        f.write(str(qq_output_compressed_str))
        #
        if(qq_compress_mode == 'zlib'):
            f.write(str_append_p2_sort_zlib)
            f.write(str_append_p3_unzip_zlib)
        elif(qq_compress_mode == 'bz2'):
            f.write(str_append_p2_sort_bz2)
            f.write(str_append_p3_unzip_bz2)

        #
        if(qq_rle_mode == 'pureRLE' and qq_offset_mode == 'once' ):
            f.write(str_append_p4_pRLE_to_o1_list)
        elif(qq_rle_mode == 'biasRLE' and qq_offset_mode == 'once'):
            f.write(str_append_p4_bRLE_to_o1_list)
        elif(qq_rle_mode == 'pureRLE' and qq_offset_mode == 'twice'):
            f.write(str_append_p4_pRLE_to_o2_list)

        
        f.write(str_append_p5_prune_compact)
        f.close()
    
    #   

t_now = time.time()
t_execution = t_now-t_start
print('execution time: ' + str(int(t_execution/60)) + ' min ' + str(t_execution%60) + ' sec')
    