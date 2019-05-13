import subprocess
import time

def run(length,gpu = False):
 if(gpu):
  gpustr = '0'
 else:
  gpustr = '-1'
 result = subprocess.check_output(['th', 'sample.lua', '-checkpoint', 'n1.t7', '-temperature','0.65','-length',str(length),'-gpu',gpustr])
 return result

