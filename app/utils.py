import random

from .constants import Constants

def get_random_pos(tiles = {}):
  row = None
  col = None
  
  while True:
    row = random.randrange(0, Constants.ROWS)
    col = random.randrange(0, Constants.COLS)
    
    if (row, col) not in tiles:
      break
    
  return row, col