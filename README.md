# myShellyEM

Get/Set ShellyEM parameters from **Shelly EM device**

The goal of this tool is to retrieve/set information provided by a ShellyEM device at address X.X.X.X

Results are provided as a JSON entity containing various information depending on the command provided on the cmdline:


- Local/Standalone mode: You run the tool locally on the system where the tool is installed. If no commznd is provided on the command line, the full status of the device is provided.  

## Examples:

### Stand-alone mode

    python myShellyEM.py -h
    usage: myShellyEM.py [-h] [-s] [-d] [-v] [-f [LOGFILE]] [-D [DELAY] [-I] [-ip X.X.X.X] [command]

    Get/Set ShellyEM parameters

    positional arguments:
      command               Command to execute. Default is "status"

    optional arguments:
      -h, --help            show this help message and exit
      -s, --server          run in server mode (as a Web Service)
      -d, --debug           print debug messages (to stdout)
      -v, --verbose         provides more information
      -D [DELAY], --delay [DELAY]
                            update interval in minutes (default=1440, e.g. 24H)
      -I, --info            print version and exit
      -ip X.X.X.X	    Shelly EM device IP adress. Default is 192.168.100.100




    python myShellyEM.py -v emeter0 
{
    "power": 130.27,
    "reactive": -154.57,
    "pf": -0.64,
    "voltage": 233.12,
    "is_valid": true,
    "total": 252459.2,
    "total_returned": 0.0
}
