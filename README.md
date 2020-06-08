## Motif_Indexer
For a given pairt of Motif and its match (which you can easily find using *re* module of Python), **motif_indexer** finds all the possible patterns of motif that align with the match.

It return 3 values, namely, "l" (the output), "outcomes" (all possible expansions of the motif) and "dic" (postions in each pattern that have one or more AA(s) prohibited)

### How to use?
1. Clone the directory
2. Within the same directory, import **motif_indexer.py**
3. Call its function **motif_indexer.main(*motif*, *match*)** (example: Refer to the **call_motif_indexer.py**)

### To do:
1. Mark the best pattern (the one with least # of **.**) in the output
2. Include the *re.search()/re.findall* from Python so that the function can take a sequence as input

### Notes:
1. Tested on **[ELM](http://elm.eu.org/)** and **[3DID](https://3did.irbbarcelona.org/)** motifs (05/Jun/2020) with Python3 (I can't guarantee other RegEx)
2. A lowercase character in the pattern represents a ^(Caret) - eg: the pattern Ap.L should imagined as A[^P].L
