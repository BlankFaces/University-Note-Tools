#!/usr/bin/env python3

import json
import time
import sys
import getopt

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('getPanoptoCaptions.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('getPanoptoCaptions -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   if len(inputfile) == 0:
      inputfile = input("File name: ")
   else:
      print("File name: " + inputfile)
   print("------\n")

   if len(outputfile) == 0:
      outputfile = inputfile + "-transcript.txt"

   with open(inputfile, 'r') as myfile:
      data=myfile.read()

   # parse file
   obj = json.loads(data)
   captions = [line['Caption'] for line in obj]
   time_stamps = [line['Time'] for line in obj]

   with open(outputfile, 'w') as f:
      for i in range(len(captions)):
         ty_res = time.gmtime(time_stamps[i])
         f.write("%s: %s\n" % (time.strftime("%H:%M:%S",ty_res), captions[i]))

   print("Written to %s" % outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])