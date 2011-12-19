#!/usr/bin/python
import os
import sys

usage_mesg = 'Usage: eset_rma-to-gene_rma.py <eset_rma> <probeset>'
if( len(sys.argv) != 3 ):
    print usage_mesg
    sys.exit(1)

filename_eset = sys.argv[1]
filename_probeset = sys.argv[2]

probeset2gene = dict()
f_probeset = open(filename_probeset,'r')
for line in f_probeset:
    if( line.startswith('#') ):
        continue
    tokens = line.strip().split("\t")
    probeset2gene[ tokens[0] ] = tokens[1]
f_probeset.close()

f_eset = open(filename_eset,'r')
print "GeneID\t%s"%('\t'.join(f_eset.readline().strip().split()))
for line in f_eset:
    tokens = line.strip().split("\t")
    probeset_id = tokens[0]
    if( not probeset2gene.has_key(probeset_id) ):
        continue
    print "%s\t%s"%(probeset2gene[probeset_id],'\t'.join(['%d'%(2**float(x)) for x in tokens[1:]]))
f_eset.close()
