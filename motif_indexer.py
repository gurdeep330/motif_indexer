#!/usr/bin/env python

## For a given pair of motif and its mathc, motif_indexer finds all the possible patterns
## of the motif and outputs the one that best aligns with the match.
import re, sys

#match = 'GKRIMA'
#match = 'KKSRRMCP'
#match = 'IP'
#match = 'GKKRSTSTSTSTMPPA'
#match = 'TINCQEPKLGSLVVRCS'
#motif = '^G[KR]{2}R.{0,2}(ST){3,7}[LM]P{1,3}A$'
#motif = '([FVL].C)|(C.[FVL])'
#motif = '([IL][VILY].[^P]A[^P].[VIL][^P].[^P][VLMT][^P][^P][VL][VIL])|(DD[IL][VILY].[^P]A[^P].[VL][^P].[^P][VLM][^P]P[VL][VIL])'
#motif = '(([KR]{1,2})|([KR]{1,2}.[KR]{1,3})).{0,2}C.|[VIL].$'
#motif = '([DEST]|^).{0,4}[LI].C.E.{1,4}[FLMIVAWPHY].{0,8}([DEST]|$)'

##### The script starts here #####
##################################

## A secondary function called by the primry function "make_sorts"
##
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
def pipe(data):
    new_data = []
    row = []
    for value in data:
        if value == '|':
            new_data.append(row)
            row = []
        else:
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


def join_outcome(dic):
    data = []
    for i in range(len(dic)):
        if data == []:
            data = dic[i]
            for i in range(len(data)):
                data[i] = ''.join(data[i])
        else:
            new_data = []
            for val in dic[i]:
                for row in data:
                    new_row = row
                    new_row += ''.join(val)
                    new_data.append(new_row)
            data = new_data
    #print (data)
    #print (len(data))
    return data

# Check and add more possible outcomes if there is a '{'
def check_len(i, pos, mem, val, dic):
    start = -1; end = -1
    if pos+1 < len(val):
        if val[pos+1] == '{':
            pos, start, end = solve_paran(pos+2, val)
            #print (start, end, pos)
            n = len(dic)
            #row += arr
    if start == -1 or end == -1:
        start = 1
        end = 1
    dic[i] = []
    for aa in mem:
        for num in range(start, end+1):
            j = 1
            row = []
            while (j<=num):
                row.append(aa)
                j += 1
            dic[i].append(row)

    return pos

## Generates possible outcomes of a given sub-sort
def generate_outcome(val):
    #print (len(val))
    if len(val) > 0:
        if val[0] == '(' and val[-1] == ')':
            val = val[1:-1]
        if True:
            data =[]
            dic = {}
            i = 0
            #print ('Mod', val)
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
                    # Store the characterS in the list-ed form eg ['S', 'A']
                    mem = list(val[pos+1:].split(']')[0])
                    pos += len(mem)+1
                    # Check and modify (dic) if there is a '{' just after the character
                    pos = check_len(i, pos, mem, val, dic)
                    i += 1
                elif val[pos] == '(':
                    # Store the group of characterS together in the list-ed form eg ['SA']
                    mem = [val[pos+1:].split(')')[0]]
                    #print (mem)
                    #sys.exit()
                    pos += len(mem[0])+1
                    # Check and modify (dic) if there is a '{' just after the character
                    pos = check_len(i, pos, mem, val, dic)
                    i += 1
                pos += 1
                #for num in range(len(dic)):
                #    print (dic[num])
                #sys.exit()
            return(join_outcome(dic))
    else:
        return ['']

## Function to process a given sort
def process_a_sort(val):
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
            #print (''.join(subval))
            x = ''.join(subval)
            #print (x.split())
            data += generate_outcome(''.join(subval))
            #print (data)
        #sys.exit()
        return data

def main(motif, match):
    #print ('The given motif is', motif)
    motif = re.sub("[^A-Z 0-9 \[ \] \. \{ \} \| \, \( \)]", '', motif)
    #print ('The modified motif is', motif)``
    # Make sorts of the given motif
    data = make_sorts(motif)
    # To check and split the sorts (if there is a pipe/OR)
    # Each row will contain a collections of sorts
    # Each row together is an outcome
    data = pipe(data)
    #print ('The list-ed motif is', data)
    #sys.exit()
    #print ('----')
    outcomes = []
    for row in data:
        #print ('-----------')
        dic = {}
        i = 0
        for val in row:
            # Process each sort
            dic[i] = process_a_sort(val)
            i+=1
        outcomes += join_outcome(dic)
    #print (outcomes)

    for outcome in outcomes:
        if len(outcome) == len(match):
            flag = 1
            for i, j in zip(outcome, match):
                if i != '.':
                    if i != j:
                        flag = 0
                        break
            if flag == 1:
                print (outcome, match)

#main(motif, match)
