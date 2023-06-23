from locust import FastHttpUser, task, events
import json
import os
import random
from enum import Enum

# class syntax

class Version(Enum):
    TWO = "2"
    THREE = "3"

images = []

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--url-list", type=str, env_var="URL_LIST", default="", help="File of URLs to info.jsons")
   
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print ('Loading images')
    try:
        with open(environment.parsed_options.url_list, 'r') as fh:
            for line in fh:
                url = line.replace('\n', '')
                if not url.endswith('/info.json'):
                    print (f"Skipping {url} as it doesn't end with '/info.json'")
                else:    
                    print (f'Adding {url}')
                    images.append(url)
        if len(images) == 0:
            environment.runner.quit()
    except Exception as error:
        print (error)        
        environment.runner.quit()

def identifier(url):
    return url[:-1 * len('/info.json')]

def rndImage():
    return images[random.randint(0, len(images) - 1)]

def rndImageIdentifier():
    return identifier(rndImage())

def getVersion(info):    
    if "type" in info and info['type'] == 'ImageService3':
        return Version.THREE
    else:    
        return Version.TWO

def constructURL(info, region, width=None, height=None, bounded=False, rotation="0", quality="default", format="jpg"):    
    version = getVersion(info)
    if version == version.THREE:
        identifier = info['id']

        if width and not height:
            size = f"{width},"
        elif height and not width:    
            size = f",{height}"
        elif not height and not width:
            size = "max"    
        else:
            size = f"{width},{height}"
    else:
        # assume v2    
        identifier = info['@id']

        if width and not height:
            size = f"{width},"
        elif height and not width:    
            size = f",{height}"
        elif not height and not width:
            size = "full"    
        else:
            if bounded:
                size = f"{width},{height}"
            else:
                # v2 conical URL is to only use the width
                size = f"{width},"

    if bounded:
        size = f"!{size}"

    if identifier.endswith('/'):
        identifier = identifier[:-1]

    return f"{identifier}/{region}/{size}/{rotation}/{quality}.{format}"    

class IIIFURLTester(FastHttpUser):

    @task
    def getMiradorThumbnail(self):
        url = f"{rndImageIdentifier()}/full/,120/0/default.jpg"

        self.client.get(url,name="Mirador thumbnail") 


    @task
    def getUVThumbnail(self):
        url = f"{rndImageIdentifier()}/full/90,/0/default.jpg"

        self.client.get(url,name="UV thumbnail") 

    @task
    def getThumbnailPanel(self):
        with self.client.get(rndImage(), name="info.json") as response:
            response.encoding = "utf-8"
            info = response.json()

            defaultSize = 125 # pixels
            width = defaultSize
            height = defaultSize
            found = False
            if 'sizes' in info:
                for size in info['sizes']:
                    if size['width'] >= defaultSize and size['height'] >= defaultSize:
                        width = size['width']
                        height = size['height']
                        found = True
                        break

                if found:
                    url = constructURL(info, 'full', width=width, height=height)
                else:
                    url = constructURL(info, 'full', width=width, height=height, bounded=True)
            else:
                url = constructURL(info, 'full', width=width, height=height, bounded=True)

            self.client.get(url,name="Thumbnail panel thumbnail") 

