#!/usr/bin/env python
import motif_indexer
import re

## A few examples
motif = '^G[KR]{2}R.{0,2}(ST){3,7}[^LM]P{1,3}A$'
match = 'GKKRSTSTSTSTTPPA'

#motif = '(Y)[^EPILVFYW][^HDEW][PLIV][^DEW]'
#match = 'YAAVA'

motif = '[NQ]{0,1}..[ILMV][ST][DEN][FY][FY].{2,3}[KR]{2,3}[^DE]'
match = 'PLISDFFAKRKRS'

#motif = 'F[EDQS][MILV][ED][MILV]((.{0,1}[ED])|($))'
#match = 'FEMDI'

#motif = '[^PAS].T'
#match = 'MIT'

#motif = '(([KR]{1,2})|([KR]{1,2}.[KR]{1,3})).{0,2}C.|[VIL].$'
#match = 'KKSRRMCP'
#match = 'IP'

#motif = '([DEST]|^).{0,4}[LI].C.E.{1,4}[FLMIVAWPHY].{0,8}([DEST]|$)'
#match = 'TINCQEPKLGSLVVRCS'

#motif = '([FVL].C)|(C.[FVL])'
#match = 'CIV'

motif = '([IL][VILY].[^P]A[^P].[VIL][^P].[^P][VLMT][^P][^P][VL][VIL])|(DD[IL][VILY].[^P]A[^P].[VL][^P].[^P][VLM][^P]P[VL][VIL])'
match = 'LYIYAYGLAGATAAVI'

#motif = '.[^P]A[^P].[VIL][^P].[^P][VLMT][^P][^P][VL][VIL]'
#match = 'AAAAAIAAATAAVI'

#motif = '[LFVAIMW].{3,5}[DE][FY][IL][SAPGK][FL].{3,6}[DE]{3}'
#match = 'LEDNQDFIAFSDSSEDE'

motif = '[DEST]{1,4}.{0,1}[VIL][DESTVILMA][VIL][VILM].[DEST]{0,4}'
match = 'EVILLDSD'

#motif = '([VILA]..N.I[RK])|([VILA].PN.IG.{0,6}[RK])'
#match = 'LNSNAIK'

#motif = '.[DNE][^PG][ST](([FYILMVW]..)|([^PEDGKN][FWYLIVM]).)'
#match = 'PDMSWSS'

#motif = '(([^PEDGKN][FWYLIVM]).)'
#match = 'ALY'

#motif = 'P.I[^DF].[^P].'
#match = 'PAIDMAI'

motif = '[^DE]{0,2}[^DEPG]([ST])(([FWYLMV].)|([^PRIKGN]P)|([^PRIKGN].{2,4}[VILMFWYP]))'
match = 'RVYSTGSNVF'

motif = 'R[^DE]{0,2}[^DEPG]([ST])(([FWYLMV].)|([^PRIKGN]P)|([^PRIKGN].{2,4}[VILMFWYP]))'
match = 'RVYSTGSNVF'

#motif = '[DEST]{1,10}.{0,1}[VIL][DESTVILMA][VIL][VILM].[DEST]{0,5}'
#match = 'SSSSDNIALLV'

#print (re.search(motif, match))
motif = 'P.{0,1}P.{0,2}P'
match = 'PPTEP'
l, outcomes, dic = motif_indexer.main(motif, match)
print (outcomes)
