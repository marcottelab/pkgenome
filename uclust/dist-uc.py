#!/usr/bin/python
import os
import sys

type_list = []
cluster_freq = dict()

filename_uc = sys.argv[1]


f_uc = open(filename_uc,'r')
for line in f_uc:
    if(line.startswith('#') ):
        continue
    tokens = line.strip().split('\t')
    cluster_id = tokens[1]
    query_id = tokens[8].split('|')[0]
    query_location = query_id.split()[0].split('.')[1]
    type_list.append(tokens[0])
    if( not cluster_freq.has_key(cluster_id) ):
        cluster_freq[cluster_id] = dict()
    if( not cluster_freq[cluster_id].has_key(query_location) ):
        cluster_freq[cluster_id][query_location] = []
    cluster_freq[cluster_id][query_location].append(query_id)

    target_id = tokens[9].split('|')[0]
    if( target_id != '*' ):
        target_location = target_id.split()[0].split('.')[1]
        if( not cluster_freq[cluster_id].has_key(target_location) ):
            cluster_freq[cluster_id][target_location] = []
        cluster_freq[cluster_id][target_location].append(target_id)
f_uc.close()

freq_location = dict()
freq_cloc = dict()
freq_total = dict()
total_count = 0
cluster_size_list = []
small_cluster_count = 0
for cluster_id in cluster_freq.keys():
    tmp_total = 0
    tmp_freq = dict()
    freq_cloc[cluster_id] = dict()
    for tmp_location in cluster_freq[cluster_id].keys():
        if( not freq_location.has_key(tmp_location) ):
            freq_location[tmp_location] = 0
        tmp_count = len(list(set(cluster_freq[cluster_id][tmp_location])))
        tmp_freq[tmp_location] = tmp_count
        freq_location[tmp_location] += tmp_count
        freq_cloc[cluster_id][tmp_location] = tmp_count
        tmp_total += tmp_count
    
    if( tmp_total < 10 ):
        small_cluster_count += 1
    #elif( tmp_total > 200 ):
    #    pas0
    else:
        cluster_size_list.append(tmp_total)
    freq_total[cluster_id] = tmp_total
    total_count += tmp_total

for cluster_id in sorted(freq_total.keys(),key=freq_total.get):
    print freq_total[cluster_id],freq_cloc[cluster_id]    
print "Total count:",total_count,freq_location
print "Small clusters:",small_cluster_count

good_cluster_count = 0
for tmp in cluster_size_list:
    #if( tmp > total_count*0.01 ):
    if( tmp > 200 ):
        good_cluster_count += 1
print "Good clusters(# > 0.01 of total):",good_cluster_count
