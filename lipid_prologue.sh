#!/bin/bash
#namd prologue.sh


#MolName=`echo $1 | awk {'print $1'}`
#Segment=`echo $1 | awk {'print $2'}`

MolName=$1
Segment=$2
MolName_Segment="$MolName"_"$Segment"

echo $1 >> prologue.log
echo $2 >> prologue.log
echo $MolName >> prologue.log
echo $Segment >> prologue.log




# No checking on the close SE is done - should be added
#No error checking is done - to be added

lcg-cp -v --vo gridit --connect-timeout 300 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 lfn:/grid/gridit/cesini/namd_input/namd2 file:./namd2 >> prologue.log 2>>prologue.log 

lcg-cp -v --vo gridit --connect-timeout 300 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 lfn:/grid/gridit/cesini/$MolName/$MolName_Segment.xsc file:./$MolName_Segment.xsc >> prologue.log 2>>prologue.log 

lcg-cp -v --vo gridit --connect-timeout 300 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 lfn:/grid/gridit/cesini/$MolName/$MolName_Segment.vel file:./$MolName_Segment.vel >> prologue.log 2>>prologue.log 

lcg-cp -v --vo gridit --connect-timeout 300 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 lfn:/grid/gridit/cesini/$MolName/$MolName_Segment.coor file:./$MolName_Segment.coor >> prologue.log 2>>prologue.log 

lcg-cp -v --vo gridit --connect-timeout 300 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 lfn:/grid/gridit/cesini/$MolName/$MolName.psf file:./$MolName.psf >> prologue.log  2>>prologue.log 

lcg-cp -v --vo gridit --connect-timeout 300 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 lfn:/grid/gridit/cesini/$MolName/$MolName.pdb file:./$MolName.pdb >> prologue.log  2>>prologue.log 

lcg-cp -v --vo gridit --connect-timeout 300 --sendreceive-timeout 300 --bdii-timeout 300 --srm-timeout 300 lfn:/grid/gridit/cesini/$MolName/$MolName.prm file:./$MolName.prm >> prologue.log 2>>prologue.log 

#sleep 100
