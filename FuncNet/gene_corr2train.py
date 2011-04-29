#!/usr/bin/python
import os
import sys
import random

train_group_size = 10
usage_mesg = 'Usage: gene_corr2train.py <gene_corr file> <linkage file> <output dir>'

if( len(sys.argv) < 4 ):
    print usage_mesg
    sys.exit(1)

filename_gene_corr = sys.argv[1]
filename_linkage = sys.argv[2]
dirname_out = '.'
if( len(sys.argv) == 4 ):
    dirname_out = sys.argv[3]

linkage = dict()
sys.stderr.write("Read %s ... "%filename_linkage)
f_linkage = open(filename_linkage,'r')
for line in f_linkage:
    if(line.startswith('#')):
        continue
  
    tokens = line.strip().split()
    gene1 = tokens[0]
    gene2 = tokens[1]
    link_score = int(tokens[2])

    if( not linkage.has_key(gene1) ):
        linkage[gene1] = dict()
    if( not linkage.has_key(gene2) ):
        linkage[gene2] = dict()
  
    linkage[gene1][gene2] = link_score
    linkage[gene2][gene1] = link_score
f_linkage.close()
sys.stderr.write("Done\n")

gene_corr_list = []
f_gene_corr = open(filename_gene_corr,'r')
h_corr = f_gene_corr.readline().strip()
for line in f_gene_corr:
    if(line.startswith('#')):
        continue
    gene_corr_list.append( line.strip() )
f_gene_corr.close()

random.shuffle( gene_corr_list )

filename_base = "%s.%s"%(filename_gene_corr, os.path.basename(filename_linkage).replace('.linkage','') )
filename_train_all = os.path.join(dirname_out,"%s.train.all"%filename_base)
sys.stderr.write("Write %s ... "%filename_train_all)
f_train_all = open(filename_train_all,'w')
f_train_all.write('#%s\tLinkage\n'%h_corr)

f_train = dict()
f_test = dict()
count_train = dict()
count_test = dict()
count_train_linked = dict()
count_test_linked = dict()
for i in range(0,train_group_size):
    filename_train = os.path.join(dirname_out,"%s.train.%02d"%(filename_base, i))
    f_train[i] = open(filename_train,'w')
    f_train[i].write('#%s\tLinkage\n'%h_corr)
    filename_test = os.path.join(dirname_out,"%s.test.%02d"%(filename_base, i))
    f_test[i] = open(filename_test,'w')
    f_test[i].write('#%s\tLinkage\n'%h_corr)
    count_train[i] = 0
    count_test[i] = 0
    count_train_linked[i] = 0
    count_test_linked[i] = 0

for i in range(0,len(gene_corr_list)):
    tokens = gene_corr_list[i].split()
    gene1 = tokens[0]
    gene2 = tokens[1]
    linkage_score = 0
    if( linkage.has_key(gene1) and linkage[gene1].has_key(gene2) ):
        linkage_score = linkage[gene1][gene2]

    f_train_all.write( gene_corr_list[i]+"\t%d\n"%linkage_score )
    for j in range(0,train_group_size):
        if( i % train_group_size == j ):
            f_test[j].write( gene_corr_list[i]+"\t%d\n"%linkage_score )
            count_test[j] += 1
            if( linkage_score > 0 ):
                count_test_linked[j] += 1
        else:
            f_train[j].write( gene_corr_list[i]+"\t%d\n"%linkage_score )
            count_train[j] += 1
            if( linkage_score > 0 ):
                count_train_linked[j] += 1

for i in range(0,train_group_size):
    f_train_all.write("# Group %d - training %d (%d linked), testing %d (%d linked)\n"%\
                (i,count_train[i],count_train_linked[i],count_test[i],count_test_linked[i]))
    f_train[i].close()
    f_test[i].close()

f_train_all.close()
sys.stderr.write("Done\n")
