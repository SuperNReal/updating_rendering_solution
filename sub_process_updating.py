import pygame
import sys

from threading import Thread
from time import sleep


pygame.init()


FPS = 30                                    # max frame rate
scale_per_ms = 0.3                          # scaling speed per millisecond

font = pygame.font.Font(None, 21)           # display font

rect_scale_max = 200                        # max scale value
rect_scale_min = 50                         # min scale value
rect_scale_cur = 100                        # current scale value
is_scale_down = False                       # toggles scaling up and scaling down

rect_x, rect_y = 100,100                    # rectangle's position



class Program():
    def __init__(self):
        self.window = pygame.display.set_mode((500,500))
        pygame.display.set_caption("sub process updating")
        self.clock = pygame.time.Clock()

        self.update_thread = Thread(target=self.update)
        self.update_thread.daemon = True
    
    def kill(self):
        pygame.quit()
        sys.exit()
    
    def run(self):
        self.update_thread.start()
        while True:
            self.render()
    

    def rect_update(self):
        global rect_scale_cur, is_scale_down

        scale_to_add = scale_per_ms
        if is_scale_down:
            scale_to_add = -scale_to_add
        
        rect_scale_cur += scale_to_add

        if rect_scale_cur <= rect_scale_min or rect_scale_cur >= rect_scale_max:
            is_scale_down = not is_scale_down

    def rect_render(self): 
        pygame.draw.rect(self.window, "blue", (rect_x, rect_y, rect_scale_cur, rect_scale_cur))

    def status_render(self):
        dis_fps_max = font.render(f"max FPS: {FPS}", True, "black")
        dis_fps_cur = font.render(f"current FPS: {int(self.clock.get_fps())}", True, "black")
        dis_speed_per_s = font.render(f"scaling speed per second: {scale_per_ms}", True, "black")

        dis_x = 10

        self.window.blit(dis_fps_max, (dis_x, 10))
        self.window.blit(dis_fps_cur, (dis_x, 30))
        self.window.blit(dis_speed_per_s, (dis_x, 50))
    

    def process_event(self):
        global FPS, scale_per_ms
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.kill()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    self.kill()
                
                elif ev.key == pygame.K_UP:
                    FPS += 1
                elif ev.key == pygame.K_DOWN:
                    FPS -= 1
                
                elif ev.key == pygame.K_RIGHT:
                    scale_per_ms += 0.1
                elif ev.key == pygame.K_LEFT:
                    scale_per_ms -= 0.1
    
    def update(self):
        while True:
            self.process_event()
            self.rect_update()

            #add any thing you want here

            sleep(0.001)
    
    def render(self):
        try:
            self.window.fill("green")
            self.rect_render()
            self.status_render()

            pygame.display.update()
            self.clock.tick(FPS)
        except pygame.error: # an error will be raised after you close the update thread
            sys.exit() # close program for good


if __name__ == "__main__":
    program = Program()
    program.run()