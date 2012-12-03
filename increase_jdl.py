#!/usr/bin/python
import sys


if len(sys.argv) < 2:
   print "USAGE: icrease_jdl.py <jdl_start> <N_jdl_to_create>"
   exit(1)

fin_name = sys.argv[1]
N = int(sys.argv[2])
print fin_name, N


fin = open(fin_name,'r')
lines= fin.readlines()

jdl_idx = int(fin_name.split('_')[1].split('.')[0])

for ii in range(1,N):

   new_jdl_idx = jdl_idx + ii
   fout_name = 'lipid_' + str(new_jdl_idx) + '.jdl'
   print "Creating file: " + fout_name
   fout = open(fout_name,'w')

   for line in lines:
      index = line.find('Arguments = "namd2 OPENMPI ')
      if index != -1:
         newline = 'Arguments = "namd2 OPENMPI lipid_' + str(new_jdl_idx) + '.conf";'
         line = newline + '\n'
      index = line.find('/home/cesini/mpi/lipid_segments/lipid_')
      if index != -1:
         newline = line[:index + 38 ] + str(new_jdl_idx) + '.conf"};'
         line = newline + '\n'
      index = line.find('PrologueArguments=')
      if index != -1:
         newline = 'PrologueArguments= "lipid ' + str(new_jdl_idx) + '";'
         line = newline + '\n'
      index = line.find('EpilogueArguments=')
      if index != -1:
         newline = 'EpilogueArguments= "lipid ' + str(new_jdl_idx + 1) + '";'
         line = newline + '\n'
      fout.write(line)
   fout.close()

