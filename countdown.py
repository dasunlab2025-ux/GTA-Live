import pygame
import datetime
import sys
import os
import math
import random

# Pygame ආරම්භ කිරීම
pygame.init()

# YouTube Vertical Size (කිසිම වෙනසක් නොකර හරියටම යොදයි)
WIDTH, HEIGHT = 1080, 1920
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# වර්ණ
WHITE = (255, 255, 255)
NEON_PINK = (255, 42, 143)
NEON_CYAN = (0, 255, 255)
DARK_BG = (10, 10, 15)

# අකුරු විලාස
title_font = pygame.font.SysFont("impact", 95)
subtitle_font = pygame.font.SysFont("arial", 45, bold=True)
number_font = pygame.font.SysFont("impact", 190)
label_font = pygame.font.SysFont("arial", 35, bold=True)
percent_font = pygame.font.SysFont("impact", 65)

# දින ගණනය කිරීම්
start_date = datetime.datetime(2026, 1, 1, 0, 0, 0)
release_date = datetime.datetime(2026, 11, 19, 0, 0, 0)
total_duration = (release_date - start_date).total_seconds()

# පසුබිම් ඡායාරූපය Load කිරීම
bg_image = None
if os.path.exists("bg.jpg"):
    try:
        image = pygame.image.load("bg.jpg").convert_alpha()
        bg_image = pygame.transform.smoothscale(image, (WIDTH, HEIGHT))
    except Exception as e:
        pass

overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 190)) 

# පාවෙන අංශු (Particle System)
class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(2, 7)
        self.speed_y = random.uniform(-3, -1)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.color = random.choice([NEON_PINK, NEON_CYAN, WHITE])
        self.alpha = random.randint(50, 200)

    def move(self):
        self.y += self.speed_y
        self.x += self.speed_x
        if self.y < 0:
            self.y = HEIGHT
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        temp_surface = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, (*self.color, self.alpha), (int(self.size), int(self.size)), int(self.size))
        surface.blit(temp_surface, (int(self.x), int(self.y)))

particles = [Particle() for _ in range(70)]

clock = pygame.time.Clock()

def draw_text_advanced(surface, text, font, color, y_pos, float_offset=0, glow=False):
    shadow = font.render(text, True, (0, 0, 0))
    shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 8, y_pos + 8 + float_offset))
    surface.blit(shadow, shadow_rect)

    if glow:
        glow_surf = font.render(text, True, NEON_PINK)
        glow_surf.set_alpha(100)
        surface.blit(glow_surf, glow_surf.get_rect(center=(WIDTH // 2, y_pos + float_offset + 3)))
        surface.blit(glow_surf, glow_surf.get_rect(center=(WIDTH // 2, y_pos + float_offset - 3)))

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y_pos + float_offset))
    surface.blit(text_surface, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    time_ticks = pygame.time.get_ticks()
    
    pulse = (math.sin(time_ticks / 300.0) + 1) / 2 
    float_wave = math.sin(time_ticks / 800.0) * 15 
    
    dynamic_cyan = (0, int(155 + (100 * pulse)), int(155 + (100 * pulse)))
    dynamic_pink = (int(155 + (100 * pulse)), 42, 143)

    if bg_image:
        screen.blit(bg_image, (0, 0))
        screen.blit(overlay, (0, 0))
    else:
        screen.fill(DARK_BG)

    for p in particles:
        p.move()
        p.draw(screen)

    pygame.draw.rect(screen, dynamic_cyan, (15, 15, WIDTH-30, HEIGHT-30), width=8, border_radius=25)
    pygame.draw.rect(screen, dynamic_pink, (30, 30, WIDTH-60, HEIGHT-60), width=3, border_radius=15)

    draw_text_advanced(screen, "GRAND THEFT AUTO VI", title_font, WHITE, 220, float_offset=float_wave, glow=True)
    draw_text_advanced(screen, "OFFICIAL RELEASE COUNTDOWN", subtitle_font, NEON_CYAN, 320, float_offset=float_wave)

    now = datetime.datetime.now()
    time_left = release_date - now

    if time_left.total_seconds() > 0:
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        y_time = 620
        
        draw_text_advanced(screen, f"{days}", number_font, dynamic_pink, y_time, glow=True)
        draw_text_advanced(screen, "DAYS", label_font, WHITE, y_time + 130)

        time_str = f"{hours:02d}  :  {minutes:02d}  :  {seconds:02d}"
        draw_text_advanced(screen, time_str, number_font, WHITE, y_time + 350, glow=True)
        
        labels_str = "HOURS              MINUTES              SECONDS"
        draw_text_advanced(screen, labels_str, label_font, dynamic_cyan, y_time + 480)

        elapsed = (now - start_date).total_seconds()
        percentage = min(max((elapsed / total_duration) * 100, 0), 100)

        bar_width = 900
        bar_height = 70
        bar_x = (WIDTH - bar_width) // 2
        bar_y = 1350

        pygame.draw.rect(screen, (20, 20, 25), (bar_x, bar_y, bar_width, bar_height), border_radius=35)
        
        fill_width = int(bar_width * (percentage / 100))
        if fill_width > 35:
            pygame.draw.rect(screen, NEON_PINK, (bar_x, bar_y, fill_width, bar_height), border_radius=35)
            pygame.draw.rect(screen, (255, 100, 180), (bar_x + 5, bar_y + 5, fill_width - 10, bar_height - 10), border_radius=30)
        
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), width=4, border_radius=35)

        percent_str = f"{percentage:.6f} %  COMPLETED"
        draw_text_advanced(screen, percent_str, percent_font, WHITE, bar_y - 80, glow=True)

    else:
        draw_text_advanced(screen, "AVAILABLE NOW!", title_font, dynamic_cyan, 900, float_offset=float_wave, glow=True)

    pygame.display.update()
    clock.tick(30) # GitHub Server එකට අධික බරක් නොපැටවීමට 30 FPS යොදා ඇත