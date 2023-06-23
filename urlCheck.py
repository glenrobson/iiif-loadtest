import os
import sys
from urllib.request import urlopen
from urllib.error import HTTPError
import json
from json import JSONDecodeError

if __name__ == "__main__":
    """
        Useful to test the URls to see they return correctly before running the load test
        This assumes all URLs are to JSON documents either info.jsons, manifests or collections
    """
    if len(sys.argv) != 3:
        print ('Usage:\n\turlCheck.py [host] [file of URLs]')
        exit(-1)

    with open(sys.argv[2]) as f:
        for line in f:
            try:
                response = urlopen(f"{sys.argv[1]}{line}")
                if response.getcode() != 200: 
                    print (f"{connection.getcode()}: {line}")    
                else:
                    try:
                        data = json.loads(response.read())    
                    except JSONDecodeError as error:   
                        print (f"Failed to read {line} due to {error}")

                response.close()
            except HTTPError as e:
                print (f"{e.getcode()}: {line}")