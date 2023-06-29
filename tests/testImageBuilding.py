import unittest

import math
from imagesrv import imageBuilder

LEVEL0_V2 = {
    "@context" : "http://iiif.io/api/image/2/context.json",
    "@id" : "https://iiif-test.github.io/Space/images/JNCE_2021158_34C00002_V01-blue",
    "width" : 1600,
    "height" : 1600,
    "tiles" : [ {
        "scaleFactors" : [ 32, 16, 8, 4, 2, 1 ],
        "width" : 1024,
        "height" : 1024
    } ],
    "protocol" : "http://iiif.io/api/image",
    "sizes" : [ 
        { "width" : 50, "height" : 50 }, 
        { "width" : 100, "height" : 100 }, 
        { "width" : 200, "height" : 200 }, 
        { "width" : 400, "height" : 400 }, 
        { "width" : 800, "height" : 800 },
        { "width" : 1600, "height" : 1600 } 
    ],
    "profile" : "http://iiif.io/api/image/2/level0.json"
}

LEVEL0_V3 = {
    "@context" : "http://iiif.io/api/image/3/context.json",
    "id" : "https://iiif-test.github.io/Places/images/lisbon",
    "type" : "ImageService3",
    "profile" : "level0",
    "width" : 4032,
    "height" : 3024,
    "tiles" : [ {
        "scaleFactors" : [ 32, 16, 8, 4, 2, 1 ],
        "width" : 1024,
        "height" : 1024
    } ],
    "protocol" : "http://iiif.io/api/image",
    "sizes" : [ 
        { "width" : 126, "height" : 95 }, 
        { "width" : 252, "height" : 189 }, 
        { "width" : 504, "height" : 378 }, 
        { "width" : 1008, "height" : 756 }, 
        { "width" : 2016, "height" : 1512 }, 
        { "width" : 4032, "height" : 3024 } 
    ]
}                

class ImageBuilder(unittest.TestCase):

    def testImageURLs(self):
        url = imageBuilder.constructURL(LEVEL0_V2, 'full', width=1024, height=1024)
        self.assertEqual(url, 'https://iiif-test.github.io/Space/images/JNCE_2021158_34C00002_V01-blue/full/1024,/0/default.jpg', "Expected different URL")
        url = imageBuilder.constructURL(LEVEL0_V3, 'full', width=1024, height=1024)
        self.assertEqual(url, 'https://iiif-test.github.io/Places/images/lisbon/full/1024,1024/0/default.jpg', "Expected different URL")


        url = imageBuilder.constructURL(LEVEL0_V2, 'full', width=1024, height=1024, bounded=True)
        self.assertEqual(url, 'https://iiif-test.github.io/Space/images/JNCE_2021158_34C00002_V01-blue/full/!1024,1024/0/default.jpg', "Expected different URL")
        url = imageBuilder.constructURL(LEVEL0_V3, 'full', width=1024, height=1024, bounded=True)
        self.assertEqual(url, 'https://iiif-test.github.io/Places/images/lisbon/full/!1024,1024/0/default.jpg', "Expected different URL")
        
        url = imageBuilder.constructURL(LEVEL0_V2, 'full', width=90)
        self.assertEqual(url, 'https://iiif-test.github.io/Space/images/JNCE_2021158_34C00002_V01-blue/full/90,/0/default.jpg', "Expected different URL")
        url = imageBuilder.constructURL(LEVEL0_V3, 'full', width=90)
        self.assertEqual(url, 'https://iiif-test.github.io/Places/images/lisbon/full/90,/0/default.jpg', "Expected different URL")

        url = imageBuilder.constructURL(LEVEL0_V2, '0,0,1024,1024', size="1024,1024")
        self.assertEqual(url, 'https://iiif-test.github.io/Space/images/JNCE_2021158_34C00002_V01-blue/0,0,1024,1024/1024,1024/0/default.jpg', "Expected different URL")
        url = imageBuilder.constructURL(LEVEL0_V3, '0,0,1024,1024', size="1024,1024")
        self.assertEqual(url, 'https://iiif-test.github.io/Places/images/lisbon/0,0,1024,1024/1024,1024/0/default.jpg', "Expected different URL")

        url = imageBuilder.constructURL(LEVEL0_V2, 'full', size="full")
        self.assertEqual(url, 'https://iiif-test.github.io/Space/images/JNCE_2021158_34C00002_V01-blue/full/full/0/default.jpg', "Expected different URL")
        url = imageBuilder.constructURL(LEVEL0_V3, 'full', size="full")
        self.assertEqual(url, 'https://iiif-test.github.io/Places/images/lisbon/full/max/0/default.jpg', "Expected different URL")

    def test_tiles_full(self):
        images = imageBuilder.tiles(LEVEL0_V2, 1)

        self.assertTrue(('0,0,1024,1024','1024,') == images[0][0], "Tile 0,0 missing")
        self.assertTrue(('0,1024,1024,576','1024,') == images[0][1], "Tile 0,1 missing")
        self.assertTrue(('1024,0,576,1024','576,') == images[1][0], "Tile 1,0 missing")
        self.assertTrue(('1024,1024,576,576','576,') == images[1][1], "Tile 1,1 missing")

    def test_tiles_all(self):
        info = LEVEL0_V2

        for level in info['tiles'][0]['scaleFactors']:
            if level != 1:
                images = imageBuilder.tiles(info,level)
                self.assertTrue(('0,0,1600,1600',f"{math.ceil(info['width'] / level)},") == images[0][0], f"Tile 0,0 missing. found: {images} expected: {math.ceil(info['width'] / level)},")
                self.assertEqual(len(images), 1, "Expected only 1 URL")


    def test_v3(self):
        info = LEVEL0_V3

        images = imageBuilder.tiles(info, 1)
        self.assertTrue(('0,0,1024,1024','1024,1024') == images[0][0], "Tile 0,0 missing")
        self.assertTrue(('0,1024,1024,1024','1024,1024') == images[0][1], "Tile 0,1 missing")
        self.assertTrue(('0,2048,1024,976','1024,976') == images[0][2], "Tile 0,2 missing")
        self.assertTrue(('1024,0,1024,1024','1024,1024') == images[1][0], "Tile 1,0 missing")
        self.assertTrue(('1024,1024,1024,1024','1024,1024') == images[1][1], "Tile 1,1 missing")
        self.assertTrue(('1024,2048,1024,976','1024,976') == images[1][2], "Tile 1,2 missing")
        self.assertTrue(('2048,0,1024,1024','1024,1024') == images[2][0], "Tile 2,0 missing")
        self.assertTrue(('2048,1024,1024,1024','1024,1024') == images[2][1], "Tile 2,1 missing")
        self.assertTrue(('2048,2048,1024,976','1024,976') == images[2][2], "Tile 2,2 missing")
        self.assertTrue(('3072,0,960,1024','960,1024') == images[3][0], "Tile 3,0 missing")
        self.assertTrue(('3072,1024,960,1024','960,1024') == images[3][1], "Tile 3,1 missing")
        self.assertTrue(('3072,2048,960,976','960,976') == images[3][2], "Tile 3,2 missing")

        images = imageBuilder.tiles(info, 2)
        self.assertTrue(('0,0,2048,2048','1024,1024') == images[0][0], "Tile 0,0 missing")
        self.assertTrue(('0,2048,2048,976','1024,488') == images[0][1], "Tile 0,1 missing")
        self.assertTrue(('2048,0,1984,2048','992,1024') == images[1][0], "Tile 1,0 missing")
        self.assertTrue(('2048,2048,1984,976','992,488') == images[1][1], "Tile 1,1 missing")


    def test_levels(self):
        levels = imageBuilder.levelsWithTiles(LEVEL0_V2)
        self.assertEqual(levels, [1], f"Found levels {levels}")

        levels = imageBuilder.levelsWithTiles(LEVEL0_V3)
        self.assertEqual(levels, [2, 1], f"Found levels {levels}")

    def test_zoomToPoint(self):
        # This image is in tile 1,1
        images = imageBuilder.zoomToPoint(LEVEL0_V2, 1312, 1312)
        self.assertTrue(('1024,1024,576,576','576,') == images[0], "Tile 1,1 missing")
        self.assertTrue(('0,0,1024,1024','1024,') == images[1], "Tile 0,0 missing")
        self.assertTrue(('0,1024,1024,576','1024,') == images[2], "Tile 0,1 missing")
        self.assertTrue(('1024,0,576,1024','576,') == images[3], "Tile 1,0 missing")


        # Centre point of the image
        images = imageBuilder.zoomToPoint(LEVEL0_V3, 2016, 1512)
        self.assertTrue(('0,0,2048,2048','1024,1024') == images[1], "Tile 0,0 missing")
        self.assertTrue(('0,2048,2048,976','1024,488') == images[1], "Tile 0,1 missing")
        self.assertTrue(('2048,0,1984,2048','992,1024') == images[2], "Tile 1,0 missing")
        self.assertTrue(('2048,2048,1984,976','992,488') == images[3], "Tile 1,1 missing")
        self.assertTrue(('1024,1024,1024,1024','1024,1024') == images[4], "Tile 1,1 missing")
        self.assertTrue(('0,0,1024,1024','1024,1024') == images[5], "Tile 0,0 missing")
        self.assertTrue(('0,1024,1024,1024','1024,1024') == images[6], "Tile 0,1 missing")
        self.assertTrue(('0,2048,1024,976','1024,976') == images[7], "Tile 0,2 missing")
        self.assertTrue(('1024,0,1024,1024','1024,1024') == images[8], "Tile 1,0 missing")
        self.assertTrue(('1024,2048,1024,976','1024,976') == images[9], "Tile 1,2 missing")
        self.assertTrue(('2048,0,1024,1024','1024,1024') == images[10], "Tile 2,0 missing")
        self.assertTrue(('2048,1024,1024,1024','1024,1024') == images[11], "Tile 2,1 missing")
        self.assertTrue(('2048,2048,1024,976','1024,976') == images[12], "Tile 2,2 missing")

        self.assertEqual(len(images), 13, f"Expected 13 images")

if __name__ == '__main__':
    unittest.main()        