#!/usr/bin/python
import os
import sys

output_name = sys.argv[1]

filename_genome = '%s.genome.exonerate'%output_name
filename_cDNA = '%s.cDNA.exonerate'%output_name

probe2genome = dict()
is_start = 0
f_genome = open(filename_genome,'r')
for line in f_genome:
    if( line.startswith('#') ):
        continue
    if( line.startswith('Hostname:') ):
        is_start = 1
        continue
    if( is_start == 0 ):
        continue

    tokens = line.strip().split()
    probe_id = tokens[0]
    if( not probe2genome.has_key(probe_id) ):
        probe2genome[probe_id] = 0
    probe2genome[probe_id] += 1
f_genome.close()

sys.stderr.write("Total number of probes: %d\n"%(len(probe2genome.keys())))

probeset2target = dict()
probeset2cDNA = dict()
f_cDNA = open(filename_cDNA,'r')
for line in f_cDNA:
    if( line.startswith('#') ):
        continue
    if( line.startswith('Hostname:') ):
        is_start = 1
        continue
    if( is_start == 0 ):
        continue

    tokens = line.strip().split()
    probe_id = tokens[0]
    target_id = tokens[1]

    if( not probe2genome.has_key(probe_id) ):
        continue
    if( probe2genome[probe_id] != 1 ):
        continue

    probeset_id = probe_id.split(':')[0]
    if( not probeset2cDNA.has_key(probeset_id) ):
        probeset2cDNA[probeset_id] = 0
        probeset2target[probeset_id] = []
    probeset2cDNA[probeset_id] += 1
    probeset2target[probeset_id].append(target_id)
f_genome.close()

sys.stderr.write("Total number of probesets: %d\n"%(len(probeset2cDNA.keys())))
probes_per_probeset_list = sorted(probeset2cDNA.values())
probes_per_probeset = probes_per_probeset_list[ int(0.5*len(probes_per_probeset_list)) ]
sys.stderr.write('Number of probes per probeset (median): %d\n'%probes_per_probeset)

count_good_probeset = 0
for probeset_id in sorted(probeset2cDNA.keys()):
    tmp_diff = abs(probeset2cDNA[probeset_id] - probes_per_probeset)

    target_list = sorted(list(set(probeset2target[probeset_id])))
    target_str = ','.join(target_list)
    if( tmp_diff > 1 ):
        print "#%s\t%s\t%d\t%d"%(probeset_id,target_str,probeset2cDNA[probeset_id],tmp_diff)
    elif( len(target_list) > 1 ):
        print "#%s\t%s\t%d\t%d"%(probeset_id,target_str,probeset2cDNA[probeset_id],tmp_diff)
    else:
        count_good_probeset += 1
        print "%s\t%s\t%d\t%d"%(probeset_id,target_str,probeset2cDNA[probeset_id],tmp_diff)
sys.stderr.write('Total number of good probeset: %d\n'%(count_good_probeset))
