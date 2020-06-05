## Motif_Indexer
For a given pairt of Motif and its match (which you can easily find using *re* module of Python), **motif_indexer** finds all the possible patterns of motif that align with the match.

### How to use?
1. Clone the directory
2. Within the same directory, import **motif_indexer.py**
3. Call its function **motif_indexer.main(*motif*, *match*)** (example: Refer to the **call_motif_indexer.py**)

### To do:
1. Add the *^* clause
2. Mark the best pattern (the one with least # of **.**) in the output
3. Map the indexed of the pattern to that of the match
4. Include the *re.search()/re.findall* from Python so that the function can take a sequence as input

Motif_Indexer has been tested on ELM and 3DID motifs (05/06/2020) with Python3. I can't guarantee other RegEx(s).
