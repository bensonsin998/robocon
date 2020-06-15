import math
import os
import pygame

# Variable
print("Message: Environment variables: Initializing...")

# Variable -> Color
black = (0, 0, 0)
red = (255, 0 ,0)
white = (255, 255, 255)

#---------------------------------------------------------------------

# Variable -> Window
process = True
print("Information: process: ", process)

window_height = 1100    # pixel
window_width = 1500     # pixel
print("Information: window_height: ", window_height, " pixel")
print("             window_width: ", window_width, " pixel")

#---------------------------------------------------------------------

# Variable -> Zone
# Original zone height = 10000 mm
# Original zone width = 13300 mm
# Ratio -> 1 : 10
zone_height = 1000
zone_width = 1330
print("Information: Ratio -> 1: 10")
print("             zone_height: ", zone_height, " mm")
print("             zone_width: ", zone_width, " mm")

# Variable -> Grid
grid_size = 10

col_num = int(zone_width / grid_size)  # number of columns
row_num = int(zone_height / grid_size)   # number of rows# number of rows
print("Information: col_num: ", col_num, " number")
print("             row_num: ", row_num, " number")

col_actual_size = zone_width / col_num   # mm
row_actual_size = zone_height / row_num  # mm
print("Information: col_actual_size: ", col_actual_size, " mm")
print("             row_actual_size: ", row_actual_size, " mm")

#---------------------------------------------------------------------

print("Message: Environment variables: Initializing -> Success")

# Class
class car(object):
  def __init__(self):
    self.length = self.width = 670  # mm

#---------------------------------------------------------------------

# Function
def draw_grid_line(sim_window):
  global white
  global window_height, window_width
  global grid_size, col_num, row_num

  # Start position
  # -> x_start = (1500 - (133 * 10)) / 2 = 85 pixel
  # -> y_start = (1050 - (100 * 10)) / 2 = 25 pixel
  x_start = 85
  y_start = 25

  x_end = window_width - 85
  y_end = window_height - 25

  x = x_start
  y = y_start

  # Draw columns
  for i in range(col_num + 1):
    pygame.draw.line(sim_window, white, (x, y_start), (x, y_end))
    x = x + grid_size

  # Draw rows
  for i in range(row_num + 1):
    pygame.draw.line(sim_window, white, (x_start, y), (x_end, y))
    y = y + grid_size

def get_key():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

def redraw_window(sim_window):
  global black, white
  global window_height, window_width
  global zone_height, zone_width

  sim_window.fill(black)
  draw_grid_line(sim_window)

  pygame.display.update()   # Update the screen <- sim_sindow

#---------------------------------------------------------------------

# Main Function
def simulation():
  global window_height, window_width
  global zone_height, zone_width

  pygame.init()
  pygame.display.set_caption("Simulation")
  sim_window = pygame.display.set_mode((window_width, window_height))
  sim_clock = pygame.time.Clock()

  while process:

    sim_clock.tick(10)    # FPS for sim_window

    get_key()

    redraw_window(sim_window)   # Update the screen <- sim_window

#---------------------------------------------------------------------

# Main program
if __name__ == "__main__":
  print("Message: Simulation Algorithm: Start")

  simulation()

  print("Message: Simulation Algorithm: Start -> End")

  print("Message: Program End!!!")

#---------------------------------------------------------------------