"""
A Singleton Sprite Manager class
Author: Liz Matthews, 7/21/2023

Provides on-demand loading of images for a pygame program.
Will load entire sprite sheets if given an offset.

"""

from pygame import image, Surface, Rect, SRCALPHA
from os.path import join

class SpriteManager(object):
   """A singleton factory class to create and store sprites on demand."""
   
   # The singleton instance variable
   _INSTANCE = None
   
   @classmethod
   def getInstance(cls):
      """Used to obtain the singleton instance"""
      if cls._INSTANCE == None:
         cls._INSTANCE = cls._SM()
      
      return cls._INSTANCE
   
   # Do not directly instantiate this class!
   class _SM(object):
      """An internal SpriteManager class to contain the actual code. Is a private class."""
      
      # Folder in which images are stored
      _IMAGE_FOLDER = "images"
      
      # Static information about the sprite sizes of particular image sheets.
      _SPRITE_SIZES = {
         "arrow.png" : (8,8),
         "Gunslinger3.png" : (29,40)
      }
      
      # A default sprite size
      _DEFAULT_SPRITE = (16,16)
      
      # A list of images that require to be loaded with transparency
      _TRANSPARENCY = ["Gunslinger3.png"]
      
      # A list of images that require to be loaded with a color key
      _COLOR_KEY = ["waddleDee.png", "kirby.png", "arrow.png", "hat.png"]
      
      def __init__(self):
         # Stores the surfaces indexed based on file name
         # The values in _surfaces can be a single Surface
         #  or a two dimentional grid of surfaces if it is an image sheet
         self._surfaces = {}      
      
      def __getitem__(self, key):
         return self._surfaces[key]
   
      def __setitem__(self, key, item):
         self._surfaces[key] = item
      
      def getSize(self, fileName):
         spriteSize = SpriteManager._SM._SPRITE_SIZES.get(fileName,
                                             SpriteManager._SM._DEFAULT_SPRITE)
         return spriteSize
      
      def getSprite(self, fileName, offset=None):
         # If this sprite has not already been loaded, load the image from memory
         if fileName not in self._surfaces.keys():
            self._loadImage(fileName, offset != None)
         
         # If this is an image sheet, return the correctly offset sub surface
         if offset != None:
            return self[fileName][offset[1]][offset[0]]
         
         # Otherwise, return the sheet created
         return self[fileName]
      
      def _loadImage(self, fileName, sheet=False):
         # Load the full image
         fullImage = image.load(join(SpriteManager._SM._IMAGE_FOLDER, fileName))
         
         # Look up some information about the image to be loaded
         transparent = fileName in SpriteManager._SM._TRANSPARENCY
         colorKey = fileName in SpriteManager._SM._COLOR_KEY
         
         # Detect if a transparency is needed
         if transparent:
            fullImage = fullImage.convert_alpha()
         else:
            fullImage = fullImage.convert()
         
         # If the image to be loaded is an image sheet, split it up based on the sprite size
         if sheet:
               
            self[fileName] = []
            
            # Try to get the sprite size, use the default size if it is not stored
            spriteSize = self.getSize(fileName)
            
            # See how big the sprite sheet is
            sheetDimensions = fullImage.get_size()
            
            # Iterate over the entire sheet, increment by the sprite size
            for y in range(0, sheetDimensions[1], spriteSize[1]):
               self[fileName].append([])
               for x in range(0, sheetDimensions[0], spriteSize[0]):
                  
                  # If we need transparency
                  if transparent:
                     sprite = Surface(spriteSize, SRCALPHA, 32)
                  else:
                     sprite = Surface(spriteSize)
                  
                  sprite.blit(fullImage, (0,0), Rect((x,y), spriteSize))
                  
                  # If we need to set the color key
                  if colorKey:
                     sprite.set_colorkey(sprite.get_at((0,0)))
                  
                  # Add the sprite to the end of the current row
                  self[fileName][-1].append(sprite)
         else:
            # Not a sprite sheet, full image is what we wish to store
            self[fileName] = fullImage
               
            # If we need to set the color key
            if colorKey:
               self[fileName].set_colorkey(self[fileName].get_at((0,0)))
               
            
         
