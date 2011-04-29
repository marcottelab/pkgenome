#!/usr/bin/python 
import os
import sys
from operator import itemgetter
import matplotlib.pyplot as plt

#dirname_LLS = 'LLS/'
dirname_LLS = sys.argv[1]

################################################################################
def get_ROC_data(filename_LLS):
    genepair2spearman = dict()
    genepair2LLS = dict()
    genepair2linkage = dict()

    count_true_total = 0
    count_false_total = 0
    sys.stderr.write("Read %s ... "%filename_LLS)
    f_train_LLS = open(os.path.join(dirname_LLS,filename_LLS),'r')
    f_train_LLS.readline()
    for line in f_train_LLS:
        tokens = line.strip().split()
        gene1 = tokens[1].strip('"')
        gene2 = tokens[2].strip('"')
        genepair = "".join(sorted([gene1,gene2]))
        score = float(tokens[3])
        linkage_score = int(tokens[4])
        LLS_score = float(tokens[-1])

        if( genepair2spearman.has_key(genepair) ):
            sys.stderr.write("Duplicate : %s\n"%genepair)

        genepair2spearman[genepair] = score
        genepair2LLS[genepair] = LLS_score
        genepair2linkage[genepair] = linkage_score
        if( linkage_score > 0 ):
            count_true_total += 1
        else:
            count_false_total += 1
    f_train_LLS.close()
    sys.stderr.write("Done\n")

    score_cutoff = 0.0
    genepair2spearman_sorted = sorted(genepair2spearman.items(), key=itemgetter(1), reverse=True)
    for (genepair,score) in genepair2spearman_sorted:
        if( genepair2LLS[genepair] < 0 ):
            break
        else:
            score_cutoff = score
    #print score_cutoff, len(genepair2spearman_sorted)
    #print "Total true : ",count_true_total
    #print "Total false: ",count_false_total

    genepair2LLS_updated = dict()
    for (genepair,LLS) in sorted(genepair2LLS.items(), key=itemgetter(1), reverse=True):
        if( genepair2spearman <= score_cutoff ):
            genepair2LLS_updated[genepair] = 0
        else:
            genepair2LLS_updated[genepair] = genepair2LLS[genepair]
    
    TPR_list = []
    FPR_list = []
    count_positive = 0
    count_negative = 0
    AUC_area = 0.0
    random_area = 0.0
    prev_FPR = 0.0
    for (genepair,LLS) in sorted(genepair2LLS_updated.items(), key=itemgetter(1), reverse=True):
        if( genepair2linkage[genepair] > 0 ):
            count_positive += 1
        else:
            count_negative += 1
        
        true_positive_rate = float(count_positive)/count_true_total
        false_positive_rate = float(count_negative)/count_false_total
        TPR_list.append(true_positive_rate)
        FPR_list.append(false_positive_rate)

        if( false_positive_rate > prev_FPR ):
            AUC_area += (false_positive_rate - prev_FPR)*true_positive_rate
            random_area += (false_positive_rate - prev_FPR)*false_positive_rate
            prev_FPR = false_positive_rate
        
        #print AUC_area,random_area,true_positive_rate,false_positive_rate
        #print true_positive_rate,false_positive_rate,count_negative,count_false_total
        
    return TPR_list, FPR_list, AUC_area
################################################################################
## For train_all
TPR_min = []
FPR_min = []
AUC_min = 0.0
TPR_max = []
FPR_max = []
AUC_max = 0.0

for filename_train_LLS in os.listdir(dirname_LLS):
    if( not filename_train_LLS.endswith('train_LLS.all') ):
        continue
    (TPR_all, FPR_all, AUC_all) = get_ROC_data(filename_train_LLS)

for filename_test_LLS in os.listdir(dirname_LLS):
    if( filename_test_LLS.find("test_LLS") < 0 ):
        continue
    (TPR_test, FPR_test, AUC_test) = get_ROC_data(filename_test_LLS)
    if( AUC_min == 0.0 or AUC_min > AUC_test ):
        TPR_min = TPR_test
        FPR_min = FPR_test
        AUC_min = AUC_test
    if( AUC_max == 0.0 or AUC_max < AUC_test ):
        TPR_max = TPR_test
        FPR_max = FPR_test
        AUC_max = AUC_test

exp_name = filename_train_LLS.split('.')[0]

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
ax.plot(FPR_all,TPR_all,'r-', label="All (AUC=%.3f)"%AUC_all)
ax.plot(FPR_min,TPR_min,'g-', label="Min (AUC=%.3f)"%AUC_min)
ax.plot(FPR_max,TPR_max,'b-', label="Max (AUC=%.3f)"%AUC_max)
ax.plot(FPR_all,FPR_all,'k-')
ax.set_title("ROC curve : %s"%exp_name)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
plt.legend(loc=4)
#plt.show()
plt.savefig("%s.ROC.png"%exp_name, format="png")
