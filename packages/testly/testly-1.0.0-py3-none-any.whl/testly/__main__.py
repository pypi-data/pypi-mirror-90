import sys, getopt
import os
from testly import __version__
from testly import rest
from testly import soap
from testly import database
from testly import behaviour

debug = 0

proxies = {
  "http": None,
  "https": None,
}

# Variables - SOAP START
host = ''
# Variables - SOAP END

# Variabes - REST START

# Variables - REST END

def main(argv):
    print("Copyright \N{COPYRIGHT SIGN} 2021 Stewartium, RPhipps ::: testly v{}\n".format(__version__))
    
    action = ''
    global debug
    global host

    try:
        opts, args = getopt.getopt(argv, "c:h:", ["command=", "help=", 
                                                "--host=",
                                                "debug"
                                               ])
        
    except getopt.GetoptError:
        print('Invalid syntax')
        print('To get help, type syntax below: ')
        print('python -m testly --help=')
        return sys.exit(2)
    
    for opt, arg in opts:
        if opt == "--help":
            if arg == "soap":
                print("How to use Testly SOAP module\n")
                print("Usage: python -m testly -c soap [OPTION] ENDPOINT_URL\n")
                print("Mandatory arguments: ")
                print("-h, --host   Nexus host base url e.g https://.<yourcompany>.com/WSDL")
                print("")
                print("Optional arguments i.e Some can be passed in the environment variables")
                print("\n--proxy             Sets Http proxy")
                print("--proxysec          Sets Https proxy")
                return sys.exit(0)
            elif arg == "rest":
                print("How to use Testly REST module\n")
                print("Usage: python -m testly -c rest [OPTION] ENDPOINT_URL\n")
                print("-h, --host   Nexus host base url e.g https://.<yourcompany>.com")
                print("Available OPTIONS: getStatus")
                return sys.exit(0)
            elif arg == "database":
                print("How to use Testly database module")
                return sys.exit(0)  
            elif arg == "bdd":
                print("How to use Testly behaviour testing module")
                return sys.exit(0)
            else:
                print('python -m testly --help soap       Help on how to test SOAP endpoint')
                print('python -m testly --help rest       Help on how to test REST endpoint')
                print('python -m testly --help bdd        Help on how to do BDD test')
                print('python -m testly --help datbase    Help on how to execute database test')
        elif opt == "--debug":
            debug = 1

        elif opt in ("-c", "--command"):
            action = arg
            if action == '':
                print("Invalid command specified")
                return sys.exit(2)
                

        elif opt in ("-h","--host"):
            host = arg
        elif opt == "--proxy":
            proxies['http'] = arg
        
        elif opt == "--proxysec":
            proxies['https'] = arg    
    
    if action == 'soap':
        soap.call_soapendpoint()
    elif action == 'rest':
        rest.call_restendpoint()

    elif action =='http':
        rest.Restly().getStatus(args[0])

    return sys.exit(0) 

    
           

if __name__ == "__main__":
    main(sys.argv[1:])    