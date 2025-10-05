# fredericks 2025
# lerps colors on a circuit playground for use in a halloween decoration
import time
import board
import neopixel
import gc
import supervisor

def lerp(begin, end, t):
   return begin + t * (end - begin)

supervisor.runtime.autoreload = False

OFF = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

ORANGE = (255,113,0)
ORANGE2 = (253,151,2)
HOTPINK = (225,2,255)
PURPLE = (174,3,255)
YELLOW = (255, 255, 0)

cols = [GREEN, RED, ORANGE, ORANGE2, HOTPINK, PURPLE, YELLOW]

NUM_LEDS = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_LEDS, auto_write=False, brightness=0.25)
pixels.fill((0,0,0))
pixels.show()

idx = 0

t = 0.0
tstep = 0.1

def lerp_colors(c1, c2, t):
  r = c1[0] + ((c2[0] - c1[0]) * t)
  g = c1[1] + ((c2[1] - c1[1]) * t)
  b = c1[2] + ((c2[2] - c1[2]) * t)
  
  return (r, g, b)

while True:
   col1 = cols[idx]
   col2 = cols[idx+1]

   col = lerp_colors(col1, col2, t)

   t += tstep
   if t > 1.0: 
       t = 0.0
       idx += 1
       #print(f"STEP {idx}, {len(cols)}")
       if idx > len(cols) - 2: 
           idx = 0
     
   # t += 0.05

   # idx += 1
   # if idx > len(cols)-1: idx = 0

   pixels.fill(col)
   pixels.show()

   time.sleep(0.25)
   gc.collect()
