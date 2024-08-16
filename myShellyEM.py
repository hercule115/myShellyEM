#!/usr/bin/env python

# Tool to get/set ShellyEM parameters

# Import or build our configuration. Must be FIRST
try:
    import config	# Shared global config variables (DEBUG,...)
except:
    #print('config.py does not exist. Generating...')
    import initConfig	# Check / Update / Create config.py module
    initConfig.initConfiguration()
    
# Import generated module
try:
    import config
except:
    print('config.py initialization has failed. Exiting')
    sys.exit(1)
    
import argparse
import builtins as __builtin__
import datetime
import inspect
import json
import logging
import os
import sys
import time

import myGlobals as mg
from common.utils import myprint, module_path, get_linenumber, color
import shellyEM as sem

#DEFAULT_IPADDR = '192.168.100.100'
DEFAULT_IPADDR = config.IPADDR #'192.168.100.100'

# Arguments parser
def parse_argv():
    desc = 'Get/Set ShellyEM parameters'

    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-s", "--server",
                        action="store_true",                        
                        dest="server",
                        default=False,
                        help="run in server mode (as a Web Service)")
    parser.add_argument("-d", "--debug",
                        action="count",
                        dest="debug",
                        default=0,
                        help="print debug messages (to stdout)")
    parser.add_argument("-v", "--verbose",
                        action="store_true", dest="verbose", default=False,
                        help="provides more information")
    parser.add_argument('-f', '--file',
                        dest='logFile',
                        const='',
                        default=None,
                        action='store',
                        nargs='?',
                        metavar='LOGFILE',
                        help="write debug messages to FILE")
    parser.add_argument("-ip", '--ipaddr',
                        dest='ipAddr',
                        const='',
                        default=DEFAULT_IPADDR,
                        action='store',
                        nargs='?',
                        metavar='IPADDR',
                        help="adress of ShellyEM device")

    
    parser.add_argument("-k", "--keepResponseFile",
                        action="store_true",
                        dest="keepResponseFile",
                        default=False,
                        help="Keep response file from ShellyEM (.json file, default=False)")
    parser.add_argument('-D', '--delay',
                        dest='updateDelay',
                        default=1440,
                        type=int,
                        action='store',
                        nargs='?',
                        metavar='DELAY',
                        help="update interval in minutes (default=1440, e.g. 24H)")
    parser.add_argument("-H", "--history",
                        action="store_true", dest="history", default=False,
                        help="Dump history")
    parser.add_argument("-I", "--info",
                        action="store_true", dest="version", default=False,
                        help="print version and exit")

    parser.add_argument('command',
                        action='store',
                        nargs='?',
                        help='Command to execute. Default is "status"')

    args = parser.parse_args()
    return args


####
def import_module_by_path(path):

    name = os.path.splitext(os.path.basename(path))[0]
    if sys.version_info[0] == 2:
        import imp
        return imp.load_source(name, path)
    elif sys.version_info[:2] <= (3, 4):
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(name, path).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


#
# Import module. Must be called *after* parsing arguments
#
def importModule(moduleDirPath, moduleName, name):

    modulePath = os.path.join(moduleDirPath, moduleName)
    mod = import_module_by_path(modulePath)
    globals()[name] = mod


####
def main():

    args = parse_argv()

    if args.version:
        print('%s: version %s' % (sys.argv[0], mg.VERSION))
        sys.exit(0)

    config.SERVER   = args.server
    config.VERBOSE  = args.verbose
    config.DEBUG    = args.debug
    
    if config.DEBUG:
        myprint(1,
                'config.DEBUG =', config.DEBUG,
                'config.SERVER =', config.SERVER,
                'config.VERBOSE =', config.VERBOSE)

    if args.keepResponseFile:
        myprint(1, "Will keep response file from server")
        config.KEEPRESPONSEFILE = True
    else:
        config.KEEPRESPONSEFILE = False
        
    if args.history:
        myprint(1, "Dumping history")
        config.HISTORY = True
    else:
        config.HISTORY = False

    if args.logFile == None:
        #print('Using stdout')
        pass
    else:
        if args.logFile == '':
            config.LOGFILE = "myShellyEM-debug.txt"
        else:
            config.LOGFILE = args.logFile
        mg.configFilePath = os.path.join(mg.moduleDirPath, config.LOGFILE)
        print('Using log file: %s' % mg.configFilePath)
        try:
            sys.stdout = open(mg.configFilePath, "w")
            sys.stderr = sys.stdout            
        except:
            print('Cannot create log file')

    if args.updateDelay:
        config.UPDATEDELAY = args.updateDelay
    else:
        config.UPDATEDELAY = 1440 # minutes

    if args.ipAddr:
        config.IPADDR = args.ipAddr
    else:
        config.IPADDR = DEFAULT_IPADDR

    if config.SERVER:
        import server as msas
        if config.DEBUG:
            mg.logger.info('server imported (line #%d)' % get_linenumber())

        myprint(0, 'Running in Server mode. Update interval: %d minutes (%s)' % (config.UPDATEDELAY, str(datetime.timedelta(minutes=config.UPDATEDELAY))))
        res = msas.apiServerMain()	# Never returns
        myprint(1, 'API Server exited with code %d' % res)
        sys.exit(res)

    #
    # Standalone mode
    #

    if args.command:
        cmd = args.command
    else:
        cmd = 'status'
        
    r = sem.shellyEMCommand(cmd)
    
    if r == -1:	# ERROR
        myprint(0, 'Unable to retrieve information')
        sys.exit(1)
        
    # Display information
    if config.VERBOSE:
        oDict = json.loads(r)
        print(json.dumps(oDict, indent=4))

    if args.logFile and args.logFile != '':
        sys.stdout.close()
        sys.stderr.close()

    sys.exit(0)

# Entry point    
if __name__ == "__main__":

    dt_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    logging.basicConfig(filename='myShellyEM-ws.log', level=logging.INFO)
    mg.logger = logging.getLogger(__name__)
    mg.logger.info('Running at %s. Args: %s' % (dt_now, ' '.join(sys.argv)))
    
    # Absolute pathname of directory containing this module
    mg.moduleDirPath = os.path.dirname(module_path(main))

    # Let's go
    main()
