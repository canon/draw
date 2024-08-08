import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

prevx = 0
prevy = 0

def in_range(st, nd, scale, v):
    return (v > st and v < (nd - st) * scale)

def screen_coords(realx, realy, vpx, vpy, scale):
    return ((realx - vpx) / scale, (realy - vpy) / scale)

def real_coords(x, y, vpx, vpy, scale):
    return (vpx + x * scale, vpy + y * scale)

def in_range(x, y):
    return x >= 0 and x < 640 and y >= 0 and y < 480

c = pygame.Color(100,200,250)

def drawdots(dots, vpx, vpy, scale):
  for j,k in dots:
    a,b = screen_coords(j, k, vpx, vpy, scale)
    if in_range(a,b):
      pygame.draw.line(screen, c, (a,b), (a+1,b+1))

def drawlines(lines, vpx, vpy, scale):
  for l in lines:
    prev_pt_scr = screen_coords(l[0][0], l[0][1], vpx, vpy, scale)
    for next_pt in l[1:]:
      next_pt_scr = screen_coords(next_pt[0], next_pt[1], vpx, vpy, scale)
      if in_range(next_pt_scr[0],next_pt_scr[1]) and in_range(prev_pt_scr[0], prev_pt_scr[1]):
        pygame.draw.line(screen, c, prev_pt_scr, next_pt_scr)
      prev_pt_scr = next_pt_scr

def shifted():
  return pygame.key.get_mods() & pygame.KMOD_SHIFT

def main():
   dots = []
   curr_line = []
   lines = []
   scale = 1.0
   vpx = 0.0
   vpy = 0.0
   scale = 1.0
   shift_mode = False
   last_mouse = (0,0)
   drawing = False
   while True:
      for event in pygame.event.get():
        x,y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
          rc = real_coords(x,y,vpx,vpy,scale)
          if drawing:
            curr_line.append(rc)
          else:
            curr_line = [rc]
          dots.append(rc)
          drawing = True
        else:
          if drawing:
            drawing = False
            lines.append(curr_line)
            dots = []
            pygame.draw.rect(screen, Color(0,0,0), (0,0,640,480))
        if shifted():
          if shift_mode:
            vpx = vpx - (x - last_mouse[0]) * scale
            vpy = vpy - (y - last_mouse[1]) * scale
            pygame.draw.rect(screen, Color(0,0,0), (0,0,640,480))
          else:
            shift_mode = True
          last_mouse = (x,y)
        else:
          shift_mode = False

        if event.type == QUIT:
          pygame.quit()
          return
        if event.type == MOUSEWHEEL:
          oldrealx, oldrealy = real_coords(x,y,vpx,vpy,scale)

          scale = scale * ((10.0 - event.y) / 10.0)
          if scale < 0.000001:
            scale = 0.000001
          # real coordinate under mouse before should be under mouse after, so shift viewport
          newrealx, newrealy = real_coords(x,y,vpx,vpy,scale)
          vpx = vpx + (oldrealx - newrealx)
          vpy = vpy + (oldrealy - newrealy)

          pygame.draw.rect(screen, Color(0,0,0), (0,0,640,480))
        drawdots(dots, vpx, vpy, scale)
        drawlines(lines, vpx, vpy, scale)
        pygame.display.flip()
      clock.tick(60)
main()
