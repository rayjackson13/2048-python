import pygame
import math
from ..constants import Constants

class Tile:  
  def __init__(self, value, row, col):
    self.value = value
    self.row = row
    self.col = col
    self.x = col * Constants.RECT_WIDTH
    self.y = row * Constants.RECT_HEIGHT
    
  def get_color(self):
    color_index = int(math.log2(self.value)) - 1
    color = Constants.COLORS[color_index]
    return color
    
  def draw(self, window, font):
    color = self.get_color()
    pygame.draw.rect(window, color, (self.x, self.y, Constants.RECT_WIDTH, Constants.RECT_HEIGHT))
    text = font.render(str(self.value), 1, Constants.FONT_COLOR)
    window.blit(
      text, 
      (
        self.x + (Constants.RECT_WIDTH / 2 - text.get_width() / 2),
        self.y + (Constants.RECT_HEIGHT / 2 - text.get_height() / 2),
      ),
    )
  
  def set_pos(self, ceil = False):
    if ceil:
      self.row = math.ceil(self.y / Constants.RECT_HEIGHT)
      self.col = math.ceil(self.x / Constants.RECT_WIDTH)
    else:
      self.row = math.floor(self.y / Constants.RECT_HEIGHT)
      self.col = math.floor(self.x / Constants.RECT_WIDTH)
  
  def move(self, delta):
    self.x += delta[0]
    self.y += delta[1]