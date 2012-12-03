#!/usr/bin/python
import sys
import os
import time

# INITIALIZATION OF VARIABLES AND STDOUT
saveout = sys.stdout
fsock = open('out.log', 'w')
sys.stdout = fsock
VO="gridit"
jobid_file = "pops200_jobid.txt"
segments_info_file = "pops200_info.txt"
JDL_DIR = "/home/cesini/mpi/lipid_segments/popepops200/"
JDL_PREFIX = "pops200_"


if len(sys.argv) < 2:
   print "USAGE: submit_chain_segments.py <segment_start> <segment_end>"
   sys.exit(1)


start_N = int(sys.argv[1])
end_N = int(sys.argv[2])

print "Submitting segments from ", start_N, " to ", end_N
print "Using VO = ", VO

fsock.flush()

if os.access(jobid_file,os.F_OK):
    print "jobidfile: ", jobid_file, " already exists, please specify another one or remove the old one. Exiting."
    sys.exit(1)
if os.access(segments_info_file,os.F_OK):
    print "job_info_file: ", segments_info_file, " already exists, please specify another one or remove the old one. Exiting."
    sys.exit(1)

finfo = open(segments_info_file,'w')

def create_proxy():
   status1 = os.system("myproxy-logon -k cesini_renew -S < logon > /dev/null 2>&1")
   status2 = os.system("voms-proxy-init --voms " + VO + " --noregen -valid 11:58 > /dev/null 2>&1")
   status = status1 + status2
   status = 0 
   return status


def submit_jdl(ii,jobid_file):
   cmd = "glite-wms-job-submit -a -o " + jobid_file + ' ' + JDL_DIR + JDL_PREFIX + str(ii) + ".jdl"
   stream = os.popen(cmd)
   lines = stream.readlines()
   FOUND_JOBID = False
   for line in lines:
       if line.find("Your job identifier is:") != -1:
          index = lines.index(line)
          jobid = lines[index + 2]
          FOUND_JOBID = True
          print "Submit_jdl: Found jobid = ", jobid
   if FOUND_JOBID == True:
       return jobid[:-1]
   else:
       return "ERROR"

def check_job_status(jobid):
   cmd = "glite-wms-job-status " + jobid
   stream = os.popen(cmd)
   lines = stream.readlines()
   job_status = "Unknown"
   for line in lines:
      if line.find("Current Status:") != -1:
         job_status = line.split(':')[1].strip().rstrip()
   return job_status

for ii in range(start_N, end_N + 1 ):
   if ii == start_N:
      print "Creating a new proxy from myproxy"
      fsock.flush()
      status = create_proxy()
      if status != 0:
         print "Error in creating the proxy. Please check manually. Exiting!"
         sys.exit(1)
      print "Submitting segment ", ii, " on ", time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())
      fsock.flush()
      jobid = submit_jdl(ii,jobid_file)
      fsock.flush()
      if jobid != "ERROR":
         line = "Segment " + str(ii) + " in jobdid: " + jobid + "    on  " + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) + '\n'
         finfo.write(line)
         finfo.flush()
      else:
         print "ERROR in submitting segment ", ii, ". Exiting!"
         sys.exit(1)
      fsock.flush()
   else:
      LAST_SEGMENT_STATUS = "Submitted"
      while LAST_SEGMENT_STATUS != "Done(Success)":
          print "sleeping for 2 minutes on " + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())
          fsock.flush()
          os.system("sleep 120")
          last_segment_jobid = os.popen("tail -1 " + jobid_file).readline()[:-1]
          print "Checking last segment status"
          fsock.flush()
          LAST_SEGMENT_STATUS = check_job_status(jobid)
          print "LAST_SEGMENT_STATUS (jobid = " , jobid, " ) = " , LAST_SEGMENT_STATUS
          if LAST_SEGMENT_STATUS == "Aborted" or LAST_SEGMENT_STATUS == "Cleared" or LAST_SEGMENT_STATUS == "Cancelled" :
             print "ERROR: last segment (jobid = ", last_segment_jobid, " was ", LAST_SEGMENT_STATUS, ". Please check manually and restart. Exiting!"
             sys.exit(1)
          fsock.flush()
      
      fsock.flush()
      print "Last segment DONE!!! We can proceed with the new one."
      print "Submitting segment ", ii, " on ", time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime())    
      print "Creating a new proxy from myproxy"
      fsock.flush()
      status = create_proxy()
      if status != 0:
         print "Error in creating the proxy. Please check manually. Exiting!"
         sys.exit(1)
      fsock.flush()
      jobid = submit_jdl(ii,jobid_file)
      if jobid != "ERROR":
         line = "Segment " + str(ii) + " in jobdid: " + jobid + "    on  " + time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime()) + '\n'
         finfo.write(line)
         finfo.flush()
         fsock.flush()
      else:
         print "ERROR in submitting segment ", ii, ". Exiting!"
         sys.exit(1)
      fsock.flush()

print "All segments submitted! Nothing left to do. Remember the status of the last one. Quitting!"
finfo.close()

sys.stdout = saveout
fsock.close()
