import requests
import __main__


def call_restendpoint():
    if __main__.debug == 1:
        print("DEBUG: REST url: ", __main__.host)
        
    Restyl = Restly()
    if __main__.host == '' or __main__.host == None:
        print("ERROR: Please specifiy host ")
        return __main__.sys.exit(2)

    else:
        Restyl.getStatus(__main__.host)


class Restly:

    def getStatus(self, URL):
        try:
            HTTPResponse = requests.get(URL)
            print("Status Code for Request: {} ".format(
                HTTPResponse.status_code))

        except requests.exceptions.RequestException as RaisedException:
            print(RaisedException)

    
    def funcname(self):
        """
        docstring
        """
        pass       
   
