#!/usr/bin/env python
import motif_indexer

## A few examples
motif = '^G[KR]{2}R.{0,2}(ST){3,7}[^LM]P{1,3}A$'
match = 'GKKRSTSTSTSTTPPA'

#motif = '[^PAS].T'
#match = 'MIT'

#motif = '(([KR]{1,2})|([KR]{1,2}.[KR]{1,3})).{0,2}C.|[VIL].$'
#match = 'KKSRRMCP'
#match = 'IP'

#motif = '([DEST]|^).{0,4}[LI].C.E.{1,4}[FLMIVAWPHY].{0,8}([DEST]|$)'
#match = 'TINCQEPKLGSLVVRCS'

#motif = '([FVL].C)|(C.[FVL])'
#match = 'CIV'

#motif = '([IL][VILY].[^P]A[^P].[VIL][^P].[^P][VLMT][^P][^P][VL][VIL])|(DD[IL][VILY].[^P]A[^P].[VL][^P].[^P][VLM][^P]P[VL][VIL])'
#match = 'LYIYAY.LA.ATAAVI'

#motif = '.[^P]A[^P].[VIL][^P].[^P][VLMT][^P][^P][VL][VIL]'
#match = 'AAAAAIAAATAAVI'

motif_indexer.main(motif, match)
