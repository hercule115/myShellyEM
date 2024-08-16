from datetime import datetime, date
import json
#from openpyxl import load_workbook
import os
import requests
import time
import shutil
import sys

import myGlobals as mg
import httpHeaders as hh
import config

from common.utils import myprint, color, dumpToFile, dumpJsonToFile, dumpListToFile, dumpListOfListToFile, bubbleSort, isFileOlderThanXMinutes

class color:
    PURPLE    = '\033[95m'
    CYAN      = '\033[96m'
    DARKCYAN  = '\033[36m'
    BLUE      = '\033[94m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    BOLD      = '\033[1m'
    GREYED    = '\033[2m'
    ITALIC    = '\033[3m'
    UNDERLINE = '\033[4m'
    STRIKETHRu = '\033[9m'
    END       = '\033[0m'


# Dictionary containing the HTTP requests to send to the device

SHELLYEM_HTTP_REQUESTS = {
    
    "status" : {
        "name" : "status",
        "info" : "Connect to ShellyEM and get full status (JSON)",
        "rqst" : {
            "type" : 'GET',
            "url"  : 'SET-AT-RUN TIME',
            "urltail" : '/status',
            "headers" : {
                "User-Agent"	  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/115.0',
                "Accept"          : '*/*',
                "Accept-Encoding" : 'gzip, deflate, br',
                "Accept-Language" : 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                "Referer"         : 'SET-AT-RUN TIME', # 'http://192.168.100.100/',
                "Host"            : 'SET-AT-RUN TIME', # '192.168.100.100',
                "Cache-Control"   : 'no-cache',
                "Connection"      : 'keep-alive',
                "Pragma"          : 'no-cache',
                "X-Requested-With": 'XMLHttpRequest',
                "DNT" 		  : '1',
            },
        },
        "resp" : {
            "code" : 200,
            "dumpResponse" : 'status.json',
            "updateCookies" : False,
        },
        "returnText" : True,
    },

    "settings" : {
        "name" : "settings",
        "info" : "Connect to ShellyEM and get full settings (JSON)",
        "rqst" : {
            "type" : 'GET',
            "url"  : 'SET-AT-RUN TIME',
            "urltail" : '/settings',
            "headers" : {
                "User-Agent"	  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/115.0',
                "Accept"          : '*/*',
                "Accept-Encoding" : 'gzip, deflate, br',
                "Accept-Language" : 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                "Referer"         : 'SET-AT-RUN TIME', # 'http://192.168.100.100/',
                "Host"            : 'SET-AT-RUN TIME', # '192.168.100.100',
                "Cache-Control"   : 'no-cache',
                "Connection"      : 'keep-alive',
                "Pragma"          : 'no-cache',
                #"X-Requested-With": 'XMLHttpRequest',
                #"DNT" 		  : '1',
            },
        },
        "resp" : {
            "code" : 200,
            "dumpResponse" : 'settings.json',
            "updateCookies" : False,
        },
        "returnText" : True,
    },

    "shelly" : {
        "name" : "shelly",
        "info" : "Connect to ShellyEM and provide basic information (JSON)",
        "rqst" : {
            "type" : 'GET',
            "url"  : 'SET-AT-RUN TIME',
            "urltail" : '/shelly',
            "headers" : {
                "User-Agent"	  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/115.0',
                "Accept"          : '*/*',
                "Accept-Encoding" : 'gzip, deflate, br',
                "Accept-Language" : 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                "Referer"         : 'SET-AT-RUN TIME', # 'http://192.168.100.100/',
                "Host"            : 'SET-AT-RUN TIME', # '192.168.100.100',
                "Cache-Control"   : 'no-cache',
                "Connection"      : 'keep-alive',
                "Pragma"          : 'no-cache',
            },
        },
        "resp" : {
            "code" : 200,
            "dumpResponse" : 'shelly.json',
            "updateCookies" : False,
        },
        "returnText" : True,
    },

    "emeter0" : {
        "name" : "emeter0",
        "info" : "Connect to ShellyEM and get emeter data for channel 0 (JSON)",
        "rqst" : {
            "type" : 'GET',
            "url"  : 'SET-AT-RUN TIME',
            "urltail" : '/emeter/0',
            "headers" : {
                "User-Agent"	  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/115.0',
                "Accept"          : '*/*',
                "Accept-Encoding" : 'gzip, deflate, br',
                "Accept-Language" : 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                "Referer"         : 'SET-AT-RUN TIME', # 'http://192.168.100.100/',
                "Host"            : 'SET-AT-RUN TIME', # '192.168.100.100',
                "Cache-Control"   : 'no-cache',
                "Connection"      : 'keep-alive',
                "Pragma"          : 'no-cache',
                "X-Requested-With": 'XMLHttpRequest',
                "DNT" 		  : '1',
            },
        },
        "resp" : {
            "code" : 200,
            "dumpResponse" : 'emeter0.json',
            "updateCookies" : False,
        },
        "returnText" : True,
    },

    "emeter1" : {
        "name" : "emeter1",
        "info" : "Connect to ShellyEM and get emeter data for channel 1 (JSON)",
        "rqst" : {
            "type" : 'GET',
            "url"  : 'SET-AT-RUN TIME',
            "urltail" : '/emeter/1',
            "headers" : {
                "User-Agent"	  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/115.0',
                "Accept"          : '*/*',
                "Accept-Encoding" : 'gzip, deflate, br',
                "Accept-Language" : 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                "Referer"         : 'SET-AT-RUN TIME', # 'http://192.168.100.100/',
                "Host"            : 'SET-AT-RUN TIME', # '192.168.100.100',
                "Cache-Control"   : 'no-cache',
                "Connection"      : 'keep-alive',
                "Pragma"          : 'no-cache',
                "X-Requested-With": 'XMLHttpRequest',
                "DNT" 		  : '1',
            },
        },
        "resp" : {
            "code" : 200,
            "dumpResponse" : 'emeter1.json',
            "updateCookies" : False,
        },
        "returnText" : True,
    },

    #/emeter/{index}?reset_totals

    "reset_totals0" : {
        "name" : "reset_totals0",
        "info" : "Connect to ShellyEM and reset emeter totals for channel 0",
        "rqst" : {
            "type" : 'GET',
            "url"  : 'SET-AT-RUN TIME',
            "urltail" : '/emeter/0?reset_totals=1',
            "headers" : {
                "User-Agent"	  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/115.0',
                "Accept"          : '*/*',
                "Accept-Encoding" : 'gzip, deflate, br',
                "Accept-Language" : 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                "Referer"         : 'SET-AT-RUN TIME', # 'http://192.168.100.100/',
                "Host"            : 'SET-AT-RUN TIME', # '192.168.100.100',
                "Cache-Control"   : 'no-cache',
                "Connection"      : 'keep-alive',
                "Pragma"          : 'no-cache',
                "X-Requested-With": 'XMLHttpRequest',
                "DNT" 		  : '1',
            },
        },
        "resp" : {
            "code" : 200,
            "dumpResponse" : '',
            "updateCookies" : False,
        },
        "returnText" : True,
    },

    "reset_totals1" : {
        "name" : "reset_totals1",
        "info" : "Connect to ShellyEM and reset emeter totals for channel 1",
        "rqst" : {
            "type" : 'GET',
            "url"  : 'SET-AT-RUN TIME',
            "urltail" : '/emeter/1?reset_totals=1',
            "headers" : {
                "User-Agent"	  : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/115.0',
                "Accept"          : '*/*',
                "Accept-Encoding" : 'gzip, deflate, br',
                "Accept-Language" : 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                "Referer"         : 'SET-AT-RUN TIME', # 'http://192.168.100.100/',
                "Host"            : 'SET-AT-RUN TIME', # '192.168.100.100',
                "Cache-Control"   : 'no-cache',
                "Connection"      : 'keep-alive',
                "Pragma"          : 'no-cache',
                "X-Requested-With": 'XMLHttpRequest',
                "DNT" 		  : '1',
            },
        },
        "resp" : {
            "code" : 200,
            "dumpResponse" : '',
            "updateCookies" : False,
        },
        "returnText" : True,
    },
}
    

class ShellyEM:

    def __init__(self, session):
        self._session  = session
        # Dict to save cookies from server
        self._cookies = dict()
        self._ipaddr = config.IPADDR
        
    def runShellyCmd(self, cmd):
        myprint(2, '*** Launching HTTP Request: %s' % cmd)
        
        httpRqst = SHELLYEM_HTTP_REQUESTS[cmd]

        # Set request parameters containing IP Addr of device
        httpRqst['rqst']['url'] = 'http://' + self._ipaddr + httpRqst['rqst']['urltail']
        httpRqst['rqst']['headers']['Referer'] = 'http://' + self._ipaddr + '/'
        httpRqst['rqst']['headers']['Host'] = self._ipaddr

        respText = self._executeRequest(httpRqst)
        if 'ErRoR' in respText:
            myprint(1, 'Error retrieving information from server')
            return -1

        if httpRqst["returnText"]:
            return respText

        return ''

        
    # Build a string containing all cookies passed as parameter in a list 
    def _buildCookieString(self, cookieList):
        cookieAsString = ''
        for c in cookieList:
            # Check if cookie exists in our dict
            if c in self._cookies:
                cookieAsString += '%s=%s; ' % (c, self._cookies[c])
            else:
                myprint(1,'Warning: Cookie %s not found.' % (c))
        return(cookieAsString)

    # Update our cookie dict
    def _updateCookies(self, cookies):
        for cookie in self._session.cookies:
            if cookie.value == 'undefined' or cookie.value == '':
                myprint(2,'Skipping cookie with undefined value %s' % (cookie.name))
                continue
            if cookie.name in self._cookies and self._cookies[cookie.name] != cookie.value:
                myprint(1,'Updating cookie:', cookie.name)
                self._cookies[cookie.name] = cookie.value
            elif not cookie.name in self._cookies:
                myprint(1,'Adding cookie:', cookie.name)
                self._cookies[cookie.name] = cookie.value
            else:
                myprint(2,'Cookie not modified:', cookie.name)                

    def _executeRequest(self, rqst):
        dt_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        myprint(1, '%s: Executing request "%s": %s' % (dt_now, rqst["name"], rqst["info"]))
        myprint(2, json.dumps(rqst, indent=4))

        hdrs = hh.HttpHeaders()

        for k,v in rqst["rqst"]["headers"].items():
            if k == "Cookie":
                if 'str' in str(type(v)):	# Cookie is a string
                    cookieAsString = v
                else:				# Cookie is a list of cookies
                    assert('list' in str(type(v)))
                    cookieAsString = self._buildCookieString(v)

                # Add extra Cookie if requested
                if "extraCookie" in rqst["rqst"]:
                    cookieAsString += rqst["rqst"]["extraCookie"]
                hdrs.setHeader('Cookie', cookieAsString)
            else:
                hdrs.setHeader(k, v)

        rqstType = rqst["rqst"]["type"]
        rqstURL  = rqst["rqst"]["url"]
        try:
            rqstStream = rqst["rqst"]["stream"]
        except:
            rqstStream = False

        try:
            csvStream = rqst["rqst"]["csv"]
        except:
            csvStream = False
            
        myprint(1,'Request type: %s, Request URL: %s' % (rqstType, rqstURL))
        myprint(2,'Request Headers:', json.dumps(hdrs.headers, indent=2))

        errFlag = False
        
        if rqstType == 'GET':
            try:
                myprint(2,'Request Stream:', rqstStream, 'CSV Stream:', csvStream)
                r = self._session.get(rqstURL, headers=hdrs.headers, stream=rqstStream)
            except requests.exceptions.RequestException as e:
                print(e)
                errFlag = True
                
        elif rqstType == 'POST':
            rqstPayloadData = rqst["rqst"]["payload_data"]
            rqstPayloadType = rqst["rqst"]["headers"]["Content-Type"]

            #if rqst["rqst"]["payload_type"] == 'MULTIPART_FORM_DATA':
            if rqstPayloadType == 'MULTIPART_FORM_DATA':
                try:
                    r = self._session.post(rqstURL,
                                           headers=hdrs.headers,
                                           files=rqstPayloadData)
                except requests.exceptions.RequestException as e:
                    errFlag = True
            else:  # Assume 'application/json'
                # Convert rqstPayloadData to a string
                rqstPayloadData = str(rqstPayloadData).replace(" ", "")
                myprint(2, rqstPayloadData)
                myprint(2, len(rqstPayloadData))

                try:
                    r = self._session.post(rqstURL,
                                           headers=hdrs.headers,
                                           data=rqstPayloadData)
                except requests.exceptions.RequestException as e:
                    errFlag = True
                    myprint(2, e)
                
        else:	# OPTIONS
            assert(rqstType == 'OPTIONS')
            try:
                r = self._session.options(rqstURL, headers=hdrs.headers)
            except requests.exceptions.RequestException as e:
                errFlag = True

        if errFlag:
            errorMsg = 'ErRoR while retrieving information' # Dont't change the cast for ErRoR  !!!!
            myprint(0, errorMsg)
            return errorMsg

        myprint(1,'Response Code:',r.status_code)

        if r.status_code != rqst["resp"]["code"]:
            myprint(1,'Invalid Status Code: %d (expected %d). Reason: %s' % (r.status_code, rqst["resp"]["code"], r.reason))
            if rqst["returnText"]:
                return ''
            else:
                return

        myprint(2,'Response Headers:', json.dumps(dict(r.headers), indent=2))
        
        # Optional parameter "useContentDisposition" and "dumpResponse"
        fname = None	# Build output filename from response header

        try:
            useContentEncoding = r.headers['Content-Encoding']
        except:
            myprint(2, 'Content-Encoding header not found in response')
        else:
            myprint(2, 'Content-Encoding header found in response:', useContentEncoding)
            fname = 'out' + '.' + useContentEncoding
            
        try:
            useContentDisposition = r.headers['Content-Disposition']
        except:
            myprint(2, 'Content-Disposition header not found in response')
            # Manually build output filename
            fname = datetime.now().strftime("%d%m%Y") + '.json'
        else:
            if useContentDisposition:
                # Example: "Content-Disposition": "attachment;filename=20221221.xlsx",
                try:
                    cd = r.headers['Content-Disposition']
                except:
                    myprint(2, 'Content-Disposition not found in response header')
                    #fname = datetime.now().strftime("%d%m%Y") + '.xlsx'
                    fname = 'out.txt'
                    #myprint(1, 'Using output filename:', fname)
                else:
                    for item in cd.split(';'):
                        if item.startswith('filename='):
                            fname = item.split('=')[1]
                            #myprint(1, 'Using output filename:', fname)
                            break
                    
                    if not fname:
                        myprint(1, 'ERROR while parsing Content-Disposition response header')
                        # Manually build output filename
                        fname = datetime.now().strftime("%d%m%Y") + '.xlsx'

        try:
            dumpResponse = rqst["resp"]["dumpResponse"]
        except:
            myprint(2, 'No "dumpResponse" requested')
            pass
        else:
            myprint(1, 'Using output filename:', fname)
            outputFile = os.path.join(mg.moduleDirPath, fname)
            myprint(1, 'Using output file path:', outputFile)

            # Update the HTTP request with new output file path
            rqst['resp']['dumpResponse'] = outputFile
                    
            if rqstStream:
                if csvStream:
                    with open(outputFile, 'wb') as f:
                        for line in r.iter_lines():
                            f.write(line+'\n'.encode())
                else:
                    r.raw.decode_content = True
                    myprint(1, "Saving raw text to %s" % outputFile)
                    with open(outputFile, 'wb') as f:
                        shutil.copyfileobj(r.raw, f)
            else:
                myprint(2, "dumpToFile(%s, r.content)" % outputFile)
                dumpToFile(outputFile, r.content)
        
        # Update cookies
        if rqst["resp"]["updateCookies"]:
            self._updateCookies(r.cookies)
            
        if rqst["returnText"]:
            return r.text

        return ''
    
####

def shellyEMCommand(cmd):

    # Create session
    with requests.session() as session:

        # Create connection with ShellyEM
        shelly = ShellyEM(session)
        
        # Get information from server
        res = shelly.runShellyCmd(cmd)
        return res
