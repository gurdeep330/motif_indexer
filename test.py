import os, sys, gzip
import motif_indexer
import pickle

'''
fasta = {}
for line in open('/home/gurdeep/projects/DB/ELM/elm_instances.fasta', 'r'):
    if line[0] == '>':
        acc = line.split('|')[1]
        fasta[acc] = ''
    elif line[0]!='\n':
        fasta[acc] += line.replace('\n', '')

motif = {}
for line in open('/home/gurdeep/projects/DB/ELM/elms_index.tsv', 'r'):
    if line[0] != '#':
        identifier = line.split('\t')[1].replace('"', '')
        regex = line.split('\t')[4].replace('"', '')
        motif[identifier] = regex

for line in open('/home/gurdeep/projects/DB/ELM/elm_instances.tsv', 'r'):
    if line[0] != '#':
        identifier = line.split('\t')[2].replace('"', '')
        acc = line.split('\t')[4].replace('"', '')
        if identifier not in ['LIG_SUMO_SIM_anti_2', 'LIG_SUMO_SIM_par_1']:
            if acc in fasta and identifier in motif:
                start = int(line.split('\t')[6].replace('"', ''))
                end = int(line.split('\t')[7].replace('"', ''))
                match = fasta[acc][start-1:end]
                #print (identifier, motif[identifier], acc, start, end, match)
                l = motif_indexer.main(motif[identifier], match)
                if l == '':
                    print (identifier, motif[identifier], acc, start, end, match, 'NOT FOUND')
                    #sys.exit()
'''

def find_same_patterns(position, outcome, outcomes, dic):
    dic[outcome][position] = []
    for pattern in outcomes:
        if len(pattern) == len(outcome):
            if pattern[position].islower():
                if pattern[:position]+pattern[position+1:] == outcome[:position]+outcome[position+1:]:
                    #print (position, pattern, outcome)
                    dic[outcome][position].append(pattern[position])
    #print (dic[position])
    #sys.exit()

def verify(data, outcomes):
    new_data = []
    dic = {}
    eliminated = []
    for outcome, match in data:
        if (any(char.islower() for char in outcome)):
            #print ('Dealing with', outcome, match)
            for position, char in enumerate(outcome):
                if char.islower():
                    if outcome not in dic:
                        dic[outcome] = {}
                    if position not in dic[outcome]:
                        find_same_patterns(position, outcome, outcomes, dic)

    #print (dic)
    #print (outcomes)
    for outcome, match in data:
        flag = 1
        if outcome in dic:
            for position, char in enumerate(outcome):
                if position in dic[outcome]:
                    for char in dic[outcome][position]:
                        if match[position].lower() == char:
                            flag = 0
                            break
                if flag == 0:
                    break
        if flag == 1:
            new_data.append((outcome, match))
        #if outcome == 'RepSn....F':
        #    print (outcome, match)
        #    print (flag, position, char)

    return new_data, dic

def process(name, motif, match, d):
    data = []
    for outcome in d[name]:
        if len(outcome) == len(match):
            flag = 1
            for i, j in zip(outcome, match):
                if i != '.':
                    if i.islower() == True:
                        if i.upper() == j:
                            flag = 0
                            break
                    elif i != j:
                        flag = 0
                        break
            if flag == 1:
                #print (outcome, match)
                #l += outcome + '\t' + match + '\n'
                data.append((outcome, match))
    data, dic = verify(data, outcomes)
    #for outcome, match in data:
    #    if 'Sn....F' in outcome:
    #        print (outcome, match)
    #sys.exit()
    l = ''
    if len(data) != 0:
        for outcome, match in data:
            l += outcome + '\t' + match + '\n'
            #print (outcome, match)
    if l == '':
        print (line.split('\t')[0], name, motif, match, 'NOT FOUND')
    else:
        if os.path.isdir('output/'+name) == False:
            os.system('mkdir output/'+name)
        gzip.open('output/'+name+'/'+match+'.tx.gz', 'wt').write(l)
        pickle.dump(dic,open('output/'+name+'/'+match + "_dic.p", "wb"))

done = []
all = ''
d = {}
for line in gzip.open('/home/gurdeep/projects/covid19/data/interactions/phosphosite/analysis_elm_motif_domain_kinase.txt.gz', 'rt'):
    if line[0] != '#':
        name = line.split('\t')[2]
        motif = line.split('\t')[4]
        match = line.split('\t')[5]
        if os.path.isdir('output/'+name) == False:
            os.system('mkdir output/'+name)
        if os.path.isfile('output/'+name+'/'+match+'.tx.gz') == False:
            #if name in ['LIG_SUMO_SIM_anti_2']:
            #if name in ['LIG_SUMO_SIM_anti_2', 'LIG_SUMO_SIM_par_1']:
            #if name in ['CLV_PCSK_KEX2_1']:
            #if 'SUMO' not in name:
            if True:
                if name not in done:
                    done.append(name)
                    print (name, motif, match)
                    #continue
                    l, outcomes, dic = motif_indexer.main(motif, match)
                    d[name] = outcomes
                    process(name, motif, match, d)
                    #break
                else:
                    process(name, motif, match, d)
                    '''
                    data = []
                    for outcome in d[name]:
                        if len(outcome) == len(match):
                            flag = 1
                            for i, j in zip(outcome, match):
                                if i != '.':
                                    if i.islower() == True:
                                        if i.upper() == j:
                                            flag = 0
                                            break
                                    elif i != j:
                                        flag = 0
                                        break
                            if flag == 1:
                                #print (outcome, match)
                                #l += outcome + '\t' + match + '\n'
                                data.append((outcome, match))
                    data, dic = verify(data, outcomes)
                    #for outcome, match in data:
                    #    if 'Sn....F' in outcome:
                    #        print (outcome, match)
                    #sys.exit()
                    l = ''
                    if len(data) != 0:
                        for outcome, match in data:
                            l += outcome + '\t' + match + '\n'
                            #print (outcome, match)
                    if l == '':
                        print (line.split('\t')[0], name, motif, match, 'NOT FOUND')
                    else:
                        if os.path.isdir('output/'+name) == False:
                            os.system('mkdir output/'+name)
                        gzip.open('output/'+name+'/'+match+'.tx.gz', 'wt').write(l)
                        pickle.dump(dic,open('output/'+name+'/'+match + "_dic.p", "wb"))
                        #all += l
                    '''
