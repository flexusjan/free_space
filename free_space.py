#!/usr/bin/python
import sys, commands, re, os
from optparse import OptionParser


STATE_OK = 0
STATE_WARNING = 1
STATE_CRITICAL = 2
STATE_UNKNOWN = 3
VERSION = "Version 0.4.3"
parser = OptionParser()


def version(option, opt_str, value, parser):
    print VERSION
    sys.exit(STATE_OK)


parser.add_option( "-w", "--warning", 
                  dest="warning", 
                  default="75", 
                  help="Warning on this percentage. Default=75")

parser.add_option( "-c", "--critical", 
                  dest="critical", 
                  default="90", 
                  help="Critical on this percentage. Default=90")

parser.add_option( "-p", "--path", 
                  dest="path", 
                  default="/", 
                  help="Path to check. Default=/")

parser.add_option( "-V", "--version", 
                  action="callback", 
                  callback=version, 
                  help="Show current version.")

parser.add_option( "-v", "--verbose", 
                  dest="verbose", 
                  default="0", 
                  help="Verbose: 0 is min, 3 is max. Default = 0")

options, args = parser.parse_args()

try:
    dskfr = commands.getstatusoutput("df "+options.path)
    value = float(re.findall(r"[0-9]+%", str(dskfr) )[0][0:-1])
    verbose = int(options.verbose)
    
    if float(options.critical) < float(options.warning):
        options.warning = options.critical

    if verbose >= 2:
        print "Name:", sys.argv[0], "\n", VERSION
        print "Warning-threshold:", options.warning
        print "Critical-threshold:", options.critical
        print "Path:", options.path
        
    if verbose >= 3:
        print "Command:", dskfr
        
except:
    print "State: UNKNOWN!"
    sys.exit(STATE_UNKNOWN)
    
    
if value < float(options.warning):
    print "State: OK! Memory usage:",str(value)+"%",
    if verbose == 1: print "at",options.path
    sys.exit(STATE_OK)
    
elif value < float(options.critical):
    print "State: WARNING! Memory usage:",str(value)+"%",
    if verbose == 1: print "at",options.path
    sys.exit(STATE_WARNING)
    
else:
    print "State: CRITICAL! Memory usage:",str(value)+"%",
    if verbose == 1: print "at",options.path
    sys.exit(STATE_CRITICAL)
