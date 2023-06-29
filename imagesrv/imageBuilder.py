import math
from enum import Enum

class Version(Enum):
    TWO = "2"
    THREE = "3"

def getVersion(info):    
    if "type" in info and info['type'] == 'ImageService3':
        return Version.THREE
    else:    
        return Version.TWO
    
def levelsWithTiles(info):    
    levels = []
    if 'tiles' in info and type(info['tiles']) == list:
        # zoom into max level / 2
        tiles = info['tiles'][0]
        if 'scaleFactors' in tiles:
            for level in tiles['scaleFactors']:
                if info['width'] / level >= tiles['width']:
                    levels.append(level)

    return levels

def constructURL(info, region, width=None, height=None, bounded=False, size="",rotation="0", quality="default", format="jpg"):    
    version = getVersion(info)
    if size:
        if version == version.THREE and size == "full":
            size = "max"
        elif version == version.TWO and size == "max":
            size = "full"    
    else:
        if version == version.THREE:

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

    if version == version.THREE:
        identifier = info['id']
    else:
        identifier = info['@id']

    if identifier.endswith('/'):
        identifier = identifier[:-1]

    return f"{identifier}/{region}/{size}/{rotation}/{quality}.{format}"

def tiles(info, level):
    images = []
    if 'tiles' in info and type(info['tiles']) == list:
        # zoom into max level / 2
        tiles = info['tiles'][0]
        if 'scaleFactors' in tiles and level in tiles['scaleFactors']:
            if 'width' in tiles and not 'height' in tiles:
                tileWidth = tiles['width']
                tileHeight = tiles['width']
            else:
                tileWidth = tiles['width']
                tileHeight = tiles['height']        

            # at risk of round errors so only use if sizes not present
            levelWidth = math.ceil(info['width'] / level)
            levelHeight = math.ceil(info['height'] / level)
            # ideally replace with actual sizes advertised
            if 'sizes' in info:
                widthLow = math.floor(info['width'] / level)
                widthHigh = math.ceil(info['width'] / level)
                for size in info['sizes']:
                    if size['width'] == widthLow or size['width'] == widthHigh:
                        levelWidth = size['width']
                        levelHeight = size['height']
                        break

            
            xTiles = math.ceil(levelWidth / tileWidth)
            yTiles = math.ceil(levelHeight / tileHeight)
            #print (f"Tiles no {xTiles + 1},{yTiles + 1} size: {tileWidth},{tileHeight} level:{levelWidth}, {levelHeight} image:{info['width']},{info['height']}")

            for x in range(0, xTiles):
                images.append([])
                for y in range(0, yTiles):
                    tileX = x * tileWidth
                    tileY = y * tileHeight
                    if tileX + tileWidth > levelWidth:
                        curTileWidth = levelWidth - tileX
                    else:
                        curTileWidth = tileWidth     

                    if tileY + tileHeight > levelHeight:
                        curTileHeight = levelHeight - tileY
                    else:
                        curTileHeight = tileHeight  

                    region = f"{tileX * level},{tileY * level},{curTileWidth * level},{curTileHeight * level}"
                    if getVersion(info) == Version.THREE:
                        size = f"{curTileWidth},{curTileHeight}" # need to think about this!
                    else:    
                        size = f"{curTileWidth}," # need to think about this!

                    # print (f"x:{x} y:{y} width:{info['width']} height:{info['height']} lw:{levelWidth}-{tileX} lh:{levelHeight}-{tileY} tileHeight:{curTileHeight}  - {region}/{size}")
                    images[x].append((region, size)) 


            # print (f"{level} from {tiles['scaleFactors']}")
        else:
            raise KeyError(f"scaleFactor {level} not in scaleFactors {tiles}")    
    else:
        raise NotImplementedError(f"Tiles not present in info.json {info}")        

    return images

def zoomToPoint(info, posx, posy):
    """
        Returns the image requests as if you were zooming into a point
        x,y the point you want to zoom to
        info the info json
        returns a list of regions and sizes to request
    """
    images = []
    # Skip to the levels that have tiles
    levels = levelsWithTiles(info)
    if levels:
        # sort so smaller sizes first 
        levels.sort(reverse=True)

        tilesInfo = info['tiles'][0]
        (tileWidth, tileHeight) = (tilesInfo['width'], tilesInfo['height'])

        for level in levels:
            # Get the tile that contains the 
            (tileX,tileY) = (math.floor(posx/(level*tileWidth)), math.floor(posy/(level*tileHeight)))

            tilesData = tiles(info,level)
            #print (f'x:{posx},y:{posy} level:{level} tileX:{tileX} tileY:{tileY} totalX:{len(tilesData)} totalY:{len(tilesData[0])}')

            images.append(tilesData[tileX][tileY])

            # Now add surrounding ones if there are any
            for x in range(tileX - 1, tileX + 2):
                for y in range(tileY - 1, tileY + 2):
                    #print (f'X:{x} < {len(tilesData)} Y:{y} < {len(tilesData[x])}' )
                    if x >= 0 and x < len(tilesData) and y >= 0 and y < len(tilesData[x]) and not (x == tileX and y == tileY):
                        #print ('added')
                        images.append(tilesData[x][y])   

    return images    

