from ..constants import Constants

class DrawHandler:
  def __init__(self, engine, font):
    self.engine = engine
    self.font = font
  
  def draw_grid(self, window):
    for row in range(1, Constants.ROWS):
      y = row * Constants.RECT_HEIGHT
      self.engine.draw.line(
        window,
        Constants.OUTLINE_COLOR,
        (0, y),
        (Constants.SCREEN_WIDTH, y),
        width=Constants.OUTLINE_THICKNESS
      )
      
    for col in range(1, Constants.COLS):
      x = col * Constants.RECT_WIDTH
      self.engine.draw.line(
        window, 
        Constants.OUTLINE_COLOR, 
        (x, 0),
        (x, Constants.SCREEN_HEIGHT),
        width=Constants.OUTLINE_THICKNESS
      )
    
    self.engine.draw.rect(
      window,
      Constants.OUTLINE_COLOR,
      (0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT),
      width=Constants.OUTLINE_THICKNESS
    )

  def draw(self, window, tiles = {}):
    window.fill(Constants.BACKGROUND_COLOR)
    
    for tile in tiles.values():
      tile.draw(window, self.font)
    
    self.draw_grid(window)

    self.engine.display.update()