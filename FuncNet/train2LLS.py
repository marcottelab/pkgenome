#!/usr/bin/python
import sys
import os
import math

bin_size = 1000
step_size = 100
group_size = 10

usage_mesg = 'Usage: train2LLS.py <LLS directory with *.train.* files>'

if( len(sys.argv) != 2 ):
  print usage_mesg
  sys.exit(1)

dirname_LLS = sys.argv[1]

for filename_train in os.listdir(dirname_LLS):
    if( filename_train.find('.train.') < 0 ):
        continue
    
    count_linked = 0
    count_unlinked = 0
    
    genepair2linkage = dict()
    genepair2corr = dict()

    filename_train = os.path.join(dirname_LLS,filename_train)
    sys.stderr.write("Read %s ... "%filename_train)
    f_train = open(filename_train,'r')
    for line in f_train:
        if( line.startswith('#') ):
            continue
        tokens = line.strip().split()
        genepair = tokens[0]+tokens[1]

        linkage_score = int(tokens[-1])
        corr = float(tokens[2])
        genepair2linkage[genepair] = linkage_score
        genepair2corr[genepair] = corr 

        if( linkage_score > 0 ):
            count_linked += 1
        else:
            count_unlinked += 1
    f_train.close()
    background_ratio = float(count_linked)/float(count_unlinked)
    sys.stderr.write("Done\n")
    
    genepair_list = sorted(genepair2linkage.keys(), key=genepair2corr.get, reverse=True)
    filename_LLS = filename_train.replace('.train.','.LLS.')
    sys.stderr.write("Write %s ... "%filename_LLS)
    f_LLS = open(filename_LLS,'w')
    f_LLS.write("# Training file : %s\n"%filename_train)
    f_LLS.write("# Background ratio : %.4f\n"%background_ratio)
    f_LLS.write("#Score\tLLS\n")
    idx = 0
    while( idx < len(genepair_list) ):
        average_corr = 0.0
        count_bin_linked = 0
        if( idx + bin_size >= len(genepair_list) ):
            break
        
        for i in range(idx,idx+bin_size):
            genepair = genepair_list[i]
            average_corr += genepair2corr[genepair]
            if( genepair2linkage[genepair] > 0 ):
                count_bin_linked += 1

        if( count_bin_linked == 0 ):
            idx += step_size
            continue

        P_linkage = float(count_bin_linked)/bin_size
        average_corr = average_corr/bin_size

        LLS_linkage = math.log( P_linkage/(1.0 - P_linkage) / background_ratio )
        f_LLS.write("%.4f\t%.4f\n"%(average_corr,LLS_linkage))
        idx += step_size
    f_LLS.close()
    sys.stderr.write("Done\n")
