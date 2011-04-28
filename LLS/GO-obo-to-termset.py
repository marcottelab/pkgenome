#!/usr/bin/python
import re
import sys
import gzip

re_alt_id = re.compile('alt_id: (GO:[0-9]+)')
re_is_a = re.compile('is_a: (GO:[0-9]+)')
re_part_of = re.compile('part_of (GO:[0-9]+)')

## 0: not include, 1: include 
with_alt_id = 1 

filename_GO = sys.argv[1]
filename_base = filename_GO.replace('.obo','')

f_GO = open(filename_GO,'r')
if( filename_GO.endswith('.gz') ):
    f_GO = gzip.open(filename_GO, 'rb')
    filename_base = filename_GO.replace('.gz','')

GO_lines = [line.strip() for line in f_GO.readlines()]
f_GO.close()

line_idx = 0
parents = dict()
alt_id_list = dict()
BP_list = dict()
MF_list = dict()
CC_list = dict()

while( line_idx < len(GO_lines) ):
  if( GO_lines[line_idx] == '[Term]' ):
    id = GO_lines[line_idx+1].lstrip('id: ')
    if( not parents.has_key(id) ):
      parents[id] = []
      alt_id_list[id] = []

    name = GO_lines[line_idx+2].replace('name: ','')
    namespace = GO_lines[line_idx+3].replace('namespace: ','')
    if( namespace == 'molecular_function' ):
      MF_list[id] = name
    if( namespace == 'biological_process' ):
      BP_list[id] = name
    if( namespace == 'cellular_component' ):
      CC_list[id] = name
    line_idx += 3

  for alt_id in re_alt_id.finditer(GO_lines[line_idx]):
    alt_id_list[id].append( alt_id.group(1) )
    
  for is_a in re_is_a.finditer(GO_lines[line_idx]):
    parent_id = is_a.group(1)
    parents[id].append(parent_id)
  
  for part_of in re_part_of.finditer(GO_lines[line_idx]):
    part_parent_id = part_of.group(1)
    parents[id].append(part_parent_id)

  line_idx += 1

def get_parents(i):
  rv = []
  if( parents.has_key(i) ):
    for p_id in parents[i]:
      rv.append(p_id)
      for pp_id in get_parents(p_id):
        rv.append(pp_id)

  return rv

BP_id_list = BP_list.keys()
BP_id_list.sort()

filename_BP = filename_base+'.GOBP_termset'
filename_MF = filename_base+'.GOMF_termset'
filename_CC = filename_base+'.GOCC_termset'

sys.stderr.write("Write %s ... "%filename_BP)
f_BP = open(filename_BP,'w')
f_BP.write("#GO_ID\tDepth\tName\tParents\n")
for id in BP_id_list:
  all_parents_id_list = list(set(get_parents(id)))
  all_parents_id_list.sort()
  if( len(all_parents_id_list) == 0 ):
    continue

  f_BP.write("%s\t%d\t%s\t%s\n"%(id,len(all_parents_id_list),BP_list[id],",".join(all_parents_id_list)))
  if( with_alt_id > 0 ):
    for alt_id in alt_id_list[id]:
      f_BP.write("%s\t%d\t%s\t%s\n"%(alt_id,len(all_parents_id_list),BP_list[id],",".join(all_parents_id_list)))

f_BP.close()
sys.stderr.write("Done\n")

MF_id_list = MF_list.keys()
MF_id_list.sort()

sys.stderr.write("Write %s ... "%filename_MF)
f_MF = open(filename_MF,'w')
f_MF.write("#GO_ID\tDepth\tName\tParents\n")
for id in MF_id_list:
  all_parents_id_list = list(set(get_parents(id)))
  all_parents_id_list.sort()
  if( len(all_parents_id_list) == 0 ):
    continue

  f_MF.write("%s\t%d\t%s\t%s\n"%(id,len(all_parents_id_list),MF_list[id],",".join(all_parents_id_list)))
  if( with_alt_id > 0 ):
    for alt_id in alt_id_list[id]:
      f_MF.write("%s\t%d\t%s\t%s\n"%(alt_id,len(all_parents_id_list),MF_list[id],",".join(all_parents_id_list)))

f_MF.close()
sys.stderr.write("Done\n")

CC_id_list = CC_list.keys()
CC_id_list.sort()

sys.stderr.write("Write %s ... "%filename_CC)
f_CC = open(filename_CC,'w')
f_CC.write("#GO_ID\tDepth\tName\tParents\n")
for id in CC_id_list:
  all_parents_id_list = list(set(get_parents(id)))
  all_parents_id_list.sort()
  if( len(all_parents_id_list) == 0 ):
    continue

  f_CC.write("%s\t%d\t%s\t%s\n"%(id,len(all_parents_id_list),CC_list[id],",".join(all_parents_id_list)))
  if( with_alt_id > 0 ):
    for alt_id in alt_id_list[id]:
      f_CC.write("%s\t%d\t%s\t%s\n"%(alt_id,len(all_parents_id_list),CC_list[id],",".join(all_parents_id_list)))

f_CC.close()
sys.stderr.write("Done\n")
