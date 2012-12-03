#!/usr/bin/python

import os, sys
#    eqNPT_pops-cuda4.coor  eqNPT_pops-cuda4.dcd  eqNPT_pops-cuda4.vel  eqNPT_pops-cuda4.xsc  eqNPT_pops-cuda4.xst
#N.B - No error checking
# SE names are hardcoded!!


saveout = sys.stdout
fsock = open('epilogue.log', 'w')
sys.stdout = fsock


#MolName=`echo $1 | awk {'print $1'}`
#Segment=`echo $1 | awk {'print $2'}`

MolName = sys.argv[1].split()[0]
Segment = sys.argv[1].split()[1]


#MolName_Segment="$MolName"_"$Segment"

MolName_Segment = MolName + '_' + Segment

SE1="se.scope.unina.it"
SE2="prod-se-02.pd.infn.it"

extension = ['coor', 'dcd', 'vel', 'xsc', 'xst']
#echo $1 >> epilogue.log
#echo $MolName >> epilogue.log
#echo $Segment >> epilogue.log

print MolName, '\n', Segment,'\n'
fsock.flush()



#lcg-cr -v --vo gridit -d $SE1 -l lfn:/grid/gridit/cesini/$MolName/$MolName_Segment.coor file:./$MolName_Segment.coor 2>>epilogue.log
#lcg-rep -v --vo gridit -d $SE2 lfn:/grid/gridit/cesini/$MolName/$MolName_Segment.coor 2>>epilogue.log

for ext in extension:

   cmd1 = "lcg-cr -v --vo gridit --connect-timeout 30 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 -d " + SE1 + " -l lfn:/grid/gridit/cesini/" + MolName + '/' + MolName_Segment +'.' + ext  + ' file:./' + MolName_Segment + '.' + ext + " 2>>epilogue.log"
   cmd2 = "lcg-rep -v --vo gridit --connect-timeout 300 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 -d " + SE2 + " lfn:/grid/gridit/cesini/" + MolName + '/'  + MolName_Segment + '.' + ext + " 2>>epilogue.log"

   for i in range(0,3):
      print "luaching cmd = " + cmd1
      fsock.flush()
      status = os.system(cmd1)
      if status == 0:
         break
      else:
         print "ERROR: cmd status = ", status
         fsock.flush()
   for i in range(0,3):
      print "luaching cmd = " + cmd2
      status = os.system(cmd2)
      if status == 0:
         break
      else:
         print "ERROR: cmd status = ", status
         fsock.flush()

print "END of Epilogue"
fsock.flush()
sys.stdout = saveout
fsock.close()


#sleep 360
