#!/usr/bin/python
import os
import sys

gene_name_map = dict()
f_txt = open('NcbiMrnaXenbaseGene_laevis.txt','r')
for line in f_txt:
    tokens = line.strip().split("\t")
    gi = tokens[0]
    gb_id = tokens[1]
    xb_id = tokens[2]
    gene_name = tokens[3]
    gene_name_map[ '%s|%s'%(gi,gb_id) ] = '%s|%s|%s|%s'%(gene_name,xb_id,gb_id,gi)
f_txt.close()

f_fa = open('xlaevisMRNA.fasta','r')
for line in f_fa:
    if( line.startswith('>') ):
        tokens = line.strip().split('|')
        gene_name = '%s|%s'%(tokens[1],tokens[3])
        if( gene_name_map.has_key(gene_name) ):
            print ">%s"%(gene_name_map[gene_name])
        else:
            print ">unnamed|NA|%s|%s"%(tokens[3],tokens[1])
    else:
        print line.strip().upper()
f_fa.close()
