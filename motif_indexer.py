#!/usr/bin/env python3

## For a given pair of motif and its mathc, motif_indexer finds all the possible patterns
## of the motif and outputs the one that best aligns with the match.

## Import built-in libraries
import re, sys, argparse
from itertools import combinations_with_replacement
from itertools import permutations
from itertools import product

## Header
__author__ = "Gurdeep Singh"
__license__ = "GPL"
__email__ = "gurdeep330@gmail.com"

##### The script starts here #####
##################################

## A secondary function called by the primry function "make_sorts"
def var_len(pos, motif):
    arr = []
    while motif[pos] != '}':
        arr.append(motif[pos])
        pos += 1
    arr.append('}')
    return pos, arr

## It make all the possible sorts of the given motif
def make_sorts(motif):
    #row = []
    data = []
    pos = 0 # current position of the motif
    while pos < len(motif):
        row = []
        char = motif[pos]
        #print (char)
        if char not in ['[', ']', '(', ')']:
            row.append(char)
            # Check if just after the end is a "{". If yes, then add it also to the sort
            # and increment the position accoridingly else ignore
            if pos+1 < len(motif):
                if motif[pos+1] == '{':
                    pos, arr = var_len(pos+1, motif)
                    row += arr
        elif char == '(':
            count = 1
            num = 0
            row.append(char)
            pos += 1
            while num != count: # To ensure # '(' and ')' are the same to take into account nested groups
                if motif[pos] == ')':
                    num += 1
                elif motif[pos] == '(':
                    count += 1
                row.append(motif[pos])
                pos += 1
            ## Decrement the position by 1 to adjust
            pos -= 1
            # Check if just after the end is a "{". If yes, then add it also to the sort
            # and increment the position accoridingly else ignore
            if pos+1 < len(motif):
                if motif[pos+1] == '{':
                    pos, arr = var_len(pos+1, motif)
                    row += arr
        elif char == '[':
            while motif[pos] != ']':
                row.append(motif[pos])
                pos += 1
            row.append(']')
            # Check if just after the end is a "{". If yes, then add it also to the sort
            # and increment the position accoridingly else ignore
            if pos+1 < len(motif):
                if motif[pos+1] == '{':
                    pos, arr = var_len(pos+1, motif)
                    row += arr

        data.append(''.join(row))
        #print (''.join(row))
        #row = []
        pos += 1

    #print (data)
    return (data)

## Function to split the sorts into more
## than one array if there is a pipe/OR
## It also removes '^' if it is a solo-sort
def pipe(data):
    new_data = []
    row = []
    for value in data:
        if value == '|':
            new_data.append(row)
            row = []
        elif value != '^':
            row.append(value)
    new_data.append(row)
    return new_data

def solve_paran(pos, motif):
    val = motif[pos:].split('}')[0]
    #print (val)
    if ',' in val:
        start = int(val.split(',')[0])
        end  = int(val.split(',')[1])
        pos += 3
    else:
        start = int(val)
        end = int(val)
        pos += 1
    return pos, start, end

def join_outcome(dic, match):
    data = []
    if len(dic) > 0:
        #print (dic)
        #print (len(dic))
        #x = [['ABCD', 'EFG'], ['xy'], ['12', '3']]
        x = [dic[i] for i in range(len(dic))]
        #print (x)
        for case in product(*x):
            #print (len(list(product(*x))))
            var = ''.join(case)
            var = list(var)
            if len(var) <= len(list(match)):
                #print (len(var), len(list(match)))
                data.append(''.join(case))
        #print (data)
        #sys.exit()
    #print (dic)
    '''
    for i in range(len(dic)):
        if data == []:
            data = dic[i]
            for i in range(len(data)):
                data[i] = ''.join(data[i])
        else:
            new_data = []
            #print (i, dic[i], len(data))
            for val in dic[i]:
                for row in data:
                    new_row = row
                    new_row += ''.join(val)
                    if len(new_row) <= len(match):
                        new_data.append(new_row)
            data = new_data
            #print (len(data))
    #print (data)
    #print (len(data))
    '''
    return data

def all_same(case):
    if case.count(case[0]) == len(case):
        return True
    else:
        return False

# Check and add more possible outcomes if there is a '{'
def check_len(i, pos, mem, val, dic):
    start = -1; end = -1
    if pos+1 < len(val):
        if val[pos+1] == '{':
            pos, start, end = solve_paran(pos+2, val)
            #print (start, end, pos)
            n = len(dic)
            #row += arr
    #if end-start>=8:
    #    end = start+8
        #return pos
    #print ('mem is', mem, end-start, len(mem)*(end-start))
    if start == -1 or end == -1:
        start = 1
        end = 1
    elif len(mem) > 3:
        end = start + 5
    dic[i] = []
    #print (mem, start, end)
    for num in range(start, end+1):
        #print (list(combinations(["hel", "lo", "bye"], 2)))
        #dic[i] += ["".join(case) for case in combinations_with_replacement(mem, num)]
        cases = ["".join(case) for case in combinations_with_replacement(mem, num)]
        #sys.exit()
        add = []
        for case in cases:
            if len(case) > 1 and all_same(case) == False:
                for perm in permutations(case):
                    #print (''.join(list(perm)))
                    #if ''.join(list(perm)) not in dic[i] and ''.join(list(perm)) not in add:
                    add.append(''.join(list(perm)))
                    #print (dic[i])
        dic[i] += cases + add
        dic[i] = list(set(dic[i]))
    #print (dic[i],'++')
    #sys.exit()
    '''
    for aa in mem:
        for num in range(start, end+1):
            j = 1
            row = []
            while (j<=num):
                row.append(aa)
                j += 1
            dic[i].append(row)
    '''
    #print (pos)
    #sys.exit()
    return pos

## Generates possible outcomes of a given sub-sort
def generate_outcome(val, match):
    #print (len(val))
    if len(val) > 0:
        if val[0] == '(' and val[-1] == ')':
            val = val[1:-1]
        if True:
            data =[]
            dic = {}
            i = 0
            #print ('Mod', val.split())
            #sys.exit()
            pos = 0
            # To investigate the given sub-sort character by character
            # All the possible subsorts are stored in the variable dic
            while pos < len(val):
                # The case where the character is A-Z
                if val[pos] not in ['{','}','[',']','(',')']:
                    #dic[i] = [val[pos]]
                    # Store the character in the list-ed form eg ['S']
                    mem = list(val[pos])
                    # Check and modify (dic) if there is a '{' just after the character
                    pos = check_len(i, pos, mem, val, dic)
                    #print (dic[i])
                    i += 1
                elif val[pos] == '[':
                    if val[pos+1] == '^':
                        # Store the characterS in the list-ed form eg [^SA] = ['P', 'Q' ....]
                        aa =  list(val[pos+2:].split(']')[0])
                        pos += len(aa)+2
                        mem = []
                        '''
                        for x in list("ACDEFGHIKLMNPQRSTVWY"):
                            if x not in aa:
                                mem.append(x)
                        '''
                        # Convert all [^..] AAs to lowercase
                        # and then match them differently later
                        mem = [char.lower() for char in aa]
                        #print (mem)
                        #sys.exit()
                    else:
                        # Store the characterS in the list-ed form eg ['S', 'A']
                        mem = list(val[pos+1:].split(']')[0])
                        pos += len(mem)+1
                    # Check and modify (dic) if there is a '{' just after the character
                    pos = check_len(i, pos, mem, val, dic)
                    i += 1
                elif val[pos] == '(':
                    if ']' not in val[pos+1:].split(')')[0]:
                        # Store the group of characterS together in the list-ed form eg ['SA']
                        mem = [val[pos+1:].split(')')[0]]
                        #print (mem)
                        #sys.exit()
                        pos += len(mem[0])+1
                        # Check and modify (dic) if there is a '{' just after the character
                        #print (val)
                        #sys.exit()
                        pos = check_len(i, pos, mem, val, dic)
                        i += 1
                    else:
                        #print (val)
                        val = val[:pos] + val[pos+1:].replace(')', '')
                        #print (val)
                        pos -= 1
                pos += 1
                #for num in range(len(dic)):
                #    print (dic[num])
                #print (pos, len(val))
            #sys.exit()
            #print ('here', len(dic))
            if len(val) > 0:
                return(join_outcome(dic, match))
            else:
                return ['']
    else:
        return ['']

## Function to process a given sort
def process_a_sort(val, match):
    #print (val)
    if val[0] == '(' and val[-1] == ')':
        val = val[1:-1]
    if True:
        dic = {}
        # Make sub-sorts of the given sort
        val = make_sorts(val)
        # To check and split the sub-sort (if there is a pipe/OR)
        val = pipe(val)
        #print (val,'---')
        data = []
        for subval in val:
            #print (val, ''.join(subval))
            x = ''.join(subval)
            #print (x.split())
            data += generate_outcome(''.join(subval), match)
            #print (data)
            #sys.exit()
        return data

def main(motif, match):
    #print ('The given motif is', motif)
    motif = re.sub("[^A-Z 0-9 \[ \] \. \{ \} \| \, \( \) \^]", '', motif)
    #print ('The modified motif is', motif)
    # Make sorts of the given motif
    data = make_sorts(motif)
    # To check and split the sorts (if there is a pipe/OR)
    # Each row will contain a collections of sorts
    # Each row together is an outcome
    # Pipe also removes '^' if it is a solo-sort
    data = pipe(data)
    #print ('The list-ed motif is', data)
    #sys.exit()
    #print ('----')
    outcomes = []
    for row in data:
        #print ('-----------')
        dic = {}
        i = 0
        count = 0
        for val in row:
            # Process each sort
            dic[i] = process_a_sort(val, match)
            count += len(dic[i])
            i+=1
        #print (count)
        #sys.exit()
        #outcomes = join_outcome(dic)
        outcomes += join_outcome(dic, match)
    #print (outcomes)
    #print ('#A lowercase character in the pattern means it is ^(Caret)')
    #print ('#Pattern', 'Match')
    #l = '#Motif\tMatch\n'
    l = ''
    data = []
    for outcome in outcomes:
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
    if len(data) != 0:
        for outcome, match in data:
            l += outcome + '\t' + match + '\n'
            #print (outcome, match)
    #else:
    #    l += 'The given pair of Motif and Match do not align'
    return l, outcomes, dic

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

## If running locally
if __name__ == '__main__':
    #print ('hello')
    #print ('hello')
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='To exapnd a Motif and map its indexes to that of a given match',  epilog="contact: gurdeep330[YouKnowWhat]gmail[YouKnowWhat]com")
    parser.add_argument('motif', help='Motif (eg: [NQ]{0,1}..[ILMV][ST][DEN][FY][FY].{2,3}[KR]{2,3}[^DE])')
    parser.add_argument('match', help='Match (eg: PLISDFFAKRKRS)')
    args = parser.parse_args()
    motif = args.motif
    match = args.match
    l, outcomes, dic = main(motif, match)
    print (l)
    sys.exit()
