import pygame
import random

from app.constants import Constants
from app.classes.Tile import Tile
from app.classes.DrawHandler import DrawHandler
from app.utils import get_random_pos

pygame.init()
FONT = pygame.font.SysFont(Constants.FONT_NAME, Constants.FONT_SIZE, bold=Constants.FONT_BOLD)
WINDOW = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
pygame.display.set_caption("2048")
drawHandler = DrawHandler(pygame, FONT)

def move_tiles(window, tiles, clock, direction):
  updated = True
  blocks = set()
  
  is_horizontal = direction == 'right' or direction == 'left'
  is_vertical = direction == 'up' or direction == 'down'
  
  sort_func = lambda x: x.col if is_horizontal else x.row
  
  if direction == 'left':
    reverse = False
    delta = (-Constants.MOVE_VELOCITY, 0)
    boundary_check = lambda tile: tile.col == 0
    get_next_tile = lambda tile: tiles.get((tile.row, tile.col - 1))
    merge_check = lambda tile, next_tile: tile.x > next_tile.x + Constants.MOVE_VELOCITY
    move_check = lambda tile, next_tile: tile.x > next_tile.x + Constants.RECT_WIDTH + Constants.MOVE_VELOCITY
    ceil = True    
  elif direction == 'right':
    reverse = True
    delta = (Constants.MOVE_VELOCITY, 0)
    boundary_check = lambda tile: tile.col == Constants.COLS - 1
    get_next_tile = lambda tile: tiles.get((tile.row, tile.col + 1))
    merge_check = lambda tile, next_tile: tile.x < next_tile.x - Constants.MOVE_VELOCITY
    move_check = lambda tile, next_tile: tile.x + Constants.RECT_WIDTH + Constants.MOVE_VELOCITY < next_tile.x 
    ceil = False    
  elif direction == 'up':
    reverse = False
    delta = (0, -Constants.MOVE_VELOCITY)
    boundary_check = lambda tile: tile.row == 0
    get_next_tile = lambda tile: tiles.get((tile.row - 1, tile.col))
    merge_check = lambda tile, next_tile: tile.y > next_tile.y + Constants.MOVE_VELOCITY
    move_check = lambda tile, next_tile: tile.y > next_tile.y + Constants.RECT_WIDTH + Constants.MOVE_VELOCITY
    ceil = True  
  elif direction == 'down':
    reverse = True
    delta = (0, Constants.MOVE_VELOCITY)
    boundary_check = lambda tile: tile.row == Constants.ROWS - 1
    get_next_tile = lambda tile: tiles.get((tile.row + 1, tile.col))
    merge_check = lambda tile, next_tile: tile.y < next_tile.y - Constants.MOVE_VELOCITY
    move_check = lambda tile, next_tile: tile.y + Constants.RECT_WIDTH + Constants.MOVE_VELOCITY < next_tile.y 
    ceil = False    
  
  while updated:
    clock.tick(Constants.FPS)
    updated = False
    sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)
    for i, tile in enumerate(sorted_tiles):
      if boundary_check(tile):
        continue
      
      next_tile = get_next_tile(tile)
      if not next_tile:
        tile.move(delta)
      elif (
        tile.value == next_tile.value
        and tile not in blocks
        and next_tile not in blocks
      ):
        if merge_check(tile, next_tile):
          tile.move(delta)
        else:
          next_tile.value *= 2
          sorted_tiles.pop(i)
          blocks.add(next_tile)
      elif move_check(tile, next_tile):
        tile.move(delta)
      else:
        continue
      
      tile.set_pos(ceil)
      updated = True
      
    update_tiles(window, tiles, sorted_tiles)
    
  return end_move(tiles)
  
def end_move(tiles):
  if len(tiles) == 16:
    return "lost"
  
  row, col = get_random_pos(tiles)
  tiles[(row, col)] = Tile(random.choice([2, 4]), row, col)
  return "continue"
    
def update_tiles(window, tiles, sorted_tiles):
  tiles.clear()
  
  for tile in sorted_tiles:
    tiles[(tile.row, tile.col)] = tile
    
  drawHandler.draw(window, tiles)
  
def generate_tiles():
  tiles = {}
  
  for _ in range(2):
    row, col = get_random_pos(tiles)
    tiles[(row, col)] = Tile(2, row, col)
    
  return tiles

def handle_input(event, window, tiles, clock):
    if event.type != pygame.KEYDOWN:
      return
    
    if event.key == pygame.K_LEFT:
      move_tiles(window, tiles, clock, 'left')
    if event.key == pygame.K_RIGHT:
      move_tiles(window, tiles, clock, 'right')
    if event.key == pygame.K_DOWN:
      move_tiles(window, tiles, clock, 'down')
    if event.key == pygame.K_UP:
      move_tiles(window, tiles, clock, 'up')

def game_loop(window = WINDOW):
  clock = pygame.time.Clock()
  run = True
  
  tiles = generate_tiles()
  
  while run:
    clock.tick(Constants.FPS)
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        break
      
      handle_input(event, window, tiles, clock)
      
    drawHandler.draw(window, tiles)
      
  pygame.quit()

if __name__ == "__main__":
  game_loop(WINDOW)