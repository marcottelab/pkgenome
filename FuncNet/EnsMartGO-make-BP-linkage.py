#!/usr/bin/python
import os
import sys
import gzip

skip_evidence_codes = ['ISS','ISO','ISA','ISM','IGC']

usage_mesg = 'Usage: EnsMartGO-make-linkage.py <EnsMartGO file>'

if( len(sys.argv) != 2 ):
    sys.stderr.write(usage_mesg+'(%d)'%(len(sys.argv))+"\n")
    sys.exit(1)

filename_mart = sys.argv[1]
filename_base = filename_mart.replace('.txt','')

gene2GO = dict()
GO2gene = dict()
gene2GO_direct = dict()
GO2gene_direct = dict()

sys.stderr.write("Read %s ... "%filename_mart)
f_mart = open(filename_mart,'r')
if( filename_mart.endswith('.gz') ):
    f_mart = gzip.open(filename_mart, 'rb')

h_mart = f_mart.readline().strip().split("\t")
idx_gene_id = h_mart.index('Ensembl Gene ID')
idx_goterm_id = h_mart.index('GO Term Accession (bp)')
idx_goterm_evidence = h_mart.index('GO Term Evidence Code (bp)')

for line in f_mart:

    tokens = line.strip().split("\t")
    if( len(tokens) != len(h_mart) ):
        continue
    gene_id = tokens[idx_gene_id]
    go_id = tokens[idx_goterm_id]
    go_evidence = tokens[idx_goterm_evidence]

    if( go_evidence in skip_evidence_codes ):
        continue

    if( not gene2GO.has_key(gene_id) ):
        gene2GO[gene_id] = []

    if( not gene2GO_direct.has_key(gene_id) ):
        gene2GO_direct[gene_id] = []

    if( not GO2gene.has_key(go_id) ):
        GO2gene[go_id] = []

    if( not GO2gene_direct.has_key(go_id) ):
        GO2gene_direct[go_id] = []

    gene2GO[gene_id].append(go_id)
    GO2gene[go_id].append(gene_id)

    gene2GO_direct[gene_id].append(go_id)
    GO2gene_direct[go_id].append(gene_id)

f_mart.close()
sys.stderr.write("Done\n")

gene_list = gene2GO.keys()
gene_list.sort()

GO_list = GO2gene.keys()
GO_list.sort()

filename_gene2GO = filename_base+'.gene2GO'

sys.stderr.write("Write %s ... "%filename_gene2GO)
f_gene2GO = open(filename_gene2GO,'w')

f_gene2GO.write("#Gene\tDirectGOTermsCount\tDirectGOTerms\tAllGOTermsCount\tAllGoTerms\n")
for gene_id in gene_list:
    gene2GO_list = list(set(gene2GO[gene_id]))
    gene2GO_direct_list = list(set(gene2GO_direct[gene_id]))
    f_gene2GO.write("%s\t%d\t%s\t%d\t%s\n"%\
        (gene_id,len(gene2GO_direct_list),",".join(gene2GO_direct_list),\
         len(gene2GO_list),",".join(gene2GO_list)))
f_gene2GO.close()
sys.stderr.write("Done\n")

filename_GO2gene = filename_base+'.GO2gene'
sys.stderr.write("Write %s ... "%filename_GO2gene)
f_GO2gene = open(filename_GO2gene,'w')
f_GO2gene.write("#GOTerm\tDirectGenesCount\tDirectGenes\tAllGenesCount\tAllGenes\n")
for go_id in GO_list:
    GO2gene_list = list(set(GO2gene[go_id]))
    GO2gene_direct_list = []
    if( GO2gene_direct.has_key(go_id) ):
        GO2gene_direct_list = list(set(GO2gene_direct[go_id]))
    f_GO2gene.write("%s\t%d\t%s\t%d\t%s\n"%\
        (go_id,len(GO2gene_direct_list),",".join(GO2gene_direct_list),\
         len(GO2gene_list),','.join(GO2gene_list)))
f_GO2gene.close()
sys.stderr.write("Done\n")

filename_linkage = filename_base+'.linkage'
sys.stderr.write("Write %s ... "%filename_linkage)
f_linkage = open(filename_linkage,'w')
f_linkage.write("#Gene1\tGene2\tDirectLinkage\tAllLinkage\n")

for i in range(0,len(gene_list)):
    gene_i = gene_list[i]
    GO_i = list(set(gene2GO[gene_i]))
    GO_direct_i = list(set(gene2GO_direct[gene_i]))

    for j in range(i+1,len(gene_list)):
        gene_j = gene_list[j]
        GO_j = list(set(gene2GO[gene_j]))
        GO_direct_j = list(set(gene2GO_direct[gene_j]))
  
        shared_term = 0
        for tmp_GO_j in GO_j:
            if( tmp_GO_j in GO_i ):
                shared_term += 1
  
        shared_direct_term = 0
        for tmp_GO_j in GO_direct_j:
            if( tmp_GO_j in GO_direct_i ):
                shared_direct_term += 1
  
        if( shared_term > 1 ):
            f_linkage.write("%s\t%s\t%d\t%d\n"%(gene_i, gene_j, shared_direct_term,shared_term))
f_linkage.close()
sys.stderr.write("Done\n")
