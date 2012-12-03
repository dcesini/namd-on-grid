#!/usr/bin/python
import sys


if len(sys.argv) < 2:
   print "USAGE: icrease_conf.py <conf_start> <N_conf_to_create>"
   exit(1)

fin_name = sys.argv[1]
N = int(sys.argv[2])
print fin_name, N


fin = open(fin_name,'r')
lines= fin.readlines()

conf_idx = int(fin_name.split('_')[1].split('.')[0])

for ii in range(1,N):

   new_conf_idx = conf_idx + ii
   fout_name = 'lipid_' + str(new_conf_idx) + '.conf'
   print "Creating file: " + fout_name
   fout = open(fout_name,'w')

   for line in lines:
      index = line.find('set firstts [get_first_ts lipid_')
      if index != -1:
         newline = 'set firstts [get_first_ts lipid_' + str(new_conf_idx) + '.xsc]'
         line = newline + '\n'
      index = line.find('bincoordinates          lipid_')
      if index != -1:
         newline = 'bincoordinates          lipid_' + str(new_conf_idx) + '.coor'
         line = newline + '\n'
      index = line.find('binvelocities           lipid_')
      if index != -1:
         newline = 'binvelocities           lipid_' + str(new_conf_idx) + '.vel'
         line = newline + '\n'
      index = line.find('extendedSystem          lipid_')
      if index != -1:
         newline = 'extendedSystem          lipid_' + str(new_conf_idx) + '.xsc'
         line = newline + '\n'
      index = line.find('set output              lipid_')
      if index != -1:
         newline = 'set output              lipid_' + str(new_conf_idx + 1)
         line = newline + '\n'
      index = line.find('restartname             lipid_res_')
      if index != -1:
         newline = 'restartname             lipid_res_' + str(new_conf_idx)
         line = newline + '\n'

      fout.write(line)
   fout.close()
