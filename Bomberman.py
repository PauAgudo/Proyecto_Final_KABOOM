import pygame HOLA
import os
import sys
import time
import random
import math  # Para funciones trigonométricas
from pygame.locals import *

# ------------------------------------------------------------------------------------
# Inicialización
# ------------------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()  # Inicializar el mezclador de sonido

# Música de fondo
MUSIC_PATH = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\Banda Sonora\banda_sonora_juego.mp3"
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(0.2)  # Ajusta el volumen de la música
pygame.mixer.music.play(-1)         # Reproduce en bucle

# ------------------------------------------------------------------------------------
# Constantes y configuración
# ------------------------------------------------------------------------------------
TILE_SIZE = 40
GRID_COLS = 21  # 21 columnas (ancho)
GRID_ROWS = 17  # 17 filas (alto)

WIDTH = GRID_COLS * TILE_SIZE  # 840 px
HEIGHT = GRID_ROWS * TILE_SIZE  # 680 px

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomberman - Jugador y habilidades de speed y more_bomb")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# ------------------------------------------------------------------------------------
# Rutas de Assets y carga de imágenes y sonidos
# ------------------------------------------------------------------------------------
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
HABILIDADES_DIR = os.path.join(ASSETS_DIR, "Habilidades")

def load_image(file, size, folder=ASSETS_DIR):
    return pygame.transform.scale(
        pygame.image.load(os.path.join(folder, file)),
        size
    )

GRASS = load_image("grass.png", (TILE_SIZE, TILE_SIZE))
STONE = load_image("stone.png", (TILE_SIZE, TILE_SIZE))
BRICK = load_image("brick.png", (TILE_SIZE, TILE_SIZE))
LIMIT_IMG = load_image("limit.png", (TILE_SIZE, TILE_SIZE))

# Habilidades
SPEED_IMG = load_image("speed.png", (40, 40), folder=HABILIDADES_DIR)
MORE_BOMB_IMG = load_image("more_bomb.png", (40, 40), folder=HABILIDADES_DIR)

# Sonido de explosión
SOUND_BOMB_PATH = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\Banda Sonora\Bombs\bomb.wav"
EXPLOSION_SOUND = pygame.mixer.Sound(SOUND_BOMB_PATH)
EXPLOSION_SOUND.set_volume(0.35)

# Sonido de pasos
FOOTSTEP_SOUND_PATH = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\Banda Sonora\movimiento\pasos.wav"
FOOTSTEP_SOUND = pygame.mixer.Sound(FOOTSTEP_SOUND_PATH)
FOOTSTEP_SOUND.set_volume(1)

# NUEVOS SONIDOS:
# Sonido al colocar bomba
COLOCAR_BOMBA_SOUND_PATH = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\Banda Sonora\Bombs\colocar_bomba.wav"
COLOCAR_BOMBA_SOUND = pygame.mixer.Sound(COLOCAR_BOMBA_SOUND_PATH)
COLOCAR_BOMBA_SOUND.set_volume(0.35)
# Sonido al recoger habilidad
COGER_HABILIDAD_SOUND_PATH = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\Banda Sonora\habilidades\coger_habilidad.wav"
COGER_HABILIDAD_SOUND = pygame.mixer.Sound(COGER_HABILIDAD_SOUND_PATH)
COGER_HABILIDAD_SOUND.set_volume(0.35)

# Animaciones para el jugador rojo (sprites de 120x120)
RED_RIGHT_IMAGES = []
red_right_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\Player1\red\right"
for i in range(1, 10):
    img = load_image("right" + str(i) + ".png", (120, 120), folder=red_right_folder)
    RED_RIGHT_IMAGES.append(img)

RED_LEFT_IMAGES = []
red_left_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\Player1\red\left"
for i in range(1, 10):
    img = load_image("left" + str(i) + ".png", (120, 120), folder=red_left_folder)
    RED_LEFT_IMAGES.append(img)

RED_UP_IMAGES = []
red_up_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\Player1\red\up"
for i in range(1, 10):
    img = load_image("up" + str(i) + ".png", (120, 120), folder=red_up_folder)
    RED_UP_IMAGES.append(img)

RED_DOWN_IMAGES = []
red_down_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\Player1\red\down"
for i in range(1, 10):
    img = load_image("down" + str(i) + ".png", (120, 120), folder=red_down_folder)
    RED_DOWN_IMAGES.append(img)

# Animaciones para el jugador azul (sprites de 120x120)
BLUE_RIGHT_IMAGES = []
blue_right_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\Player1\blue\right"
for i in range(1, 10):
    img = load_image("right" + str(i) + ".png", (120, 120), folder=blue_right_folder)
    BLUE_RIGHT_IMAGES.append(img)

BLUE_LEFT_IMAGES = []
blue_left_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\Player1\blue\left"
for i in range(1, 10):
    img = load_image("left" + str(i) + ".png", (120, 120), folder=blue_left_folder)
    BLUE_LEFT_IMAGES.append(img)

BLUE_UP_IMAGES = []
blue_up_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\Player1\blue\up"
for i in range(1, 10):
    img = load_image("up" + str(i) + ".png", (120, 120), folder=blue_up_folder)
    BLUE_UP_IMAGES.append(img)

BLUE_DOWN_IMAGES = []
blue_down_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\Player1\blue\down"
for i in range(1, 10):
    img = load_image("down" + str(i) + ".png", (120, 120), folder=blue_down_folder)
    BLUE_DOWN_IMAGES.append(img)

# Animación de explosión
EXPLOSION_FRAMES = [load_image(f"explosion_{i}.png", (40, 40)) for i in range(3)]
MAYOR_EXPLOSION_IMG = load_image("mayor_explosion.png", (40, 40), folder=HABILIDADES_DIR)
POWERUP_DESTROY_FRAMES = [pygame.Surface((40, 40)), pygame.Surface((40, 40))]
POWERUP_DESTROY_FRAMES[0].fill((255, 200, 0))
POWERUP_DESTROY_FRAMES[1].fill((255, 100, 0))

# Animación de la bomba (sprites de 40x40)
BOMB_IMAGES = []
bomb_folder = r"D:\Universitat\PRE\Proyecto Final (Bomberman)\assets\bombas"
for i in range(1, 16):
    img = load_image("bomb" + str(i) + ".png", (40, 40), folder=bomb_folder)
    BOMB_IMAGES.append(img)

# ------------------------------------------------------------------------------------
# Clases: PowerUp, Player, Bomb, Explosion
# ------------------------------------------------------------------------------------
class PowerUp:
    def __init__(self, x, y, ptype):
        self.x = x
        self.y = y
        self.type = ptype  # "major_explosion", "speed" o "more_bomb"
        self.visible = False
        self.block_explosion = True
        self.disappearing = False
        self.destroy_frames = POWERUP_DESTROY_FRAMES
        self.destroy_frame_index = 0
        self.destroy_frame_time = 100
        self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.disappearing:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.destroy_frame_time:
                self.destroy_frame_index += 1
                self.last_update = now

    def draw(self, screen):
        if not self.visible:
            return
        # Dibujar la habilidad a un 80% de la casilla (aprox. 32x32)
        ability_size = int(TILE_SIZE * 0.8)
        if not self.disappearing:
            amplitude = 3.0
            freq = 0.4
            offset_y = amplitude * math.sin(2 * math.pi * freq * time.time())
            center_x = self.x * TILE_SIZE + TILE_SIZE // 2
            center_y = self.y * TILE_SIZE + TILE_SIZE // 2 + int(offset_y)
            top_left_x = center_x - ability_size // 2
            top_left_y = center_y - ability_size // 2
            if self.type == "major_explosion":
                scaled_img = pygame.transform.scale(MAYOR_EXPLOSION_IMG, (ability_size, ability_size))
            elif self.type == "speed":
                scaled_img = pygame.transform.scale(SPEED_IMG, (ability_size, ability_size))
            elif self.type == "more_bomb":
                scaled_img = pygame.transform.scale(MORE_BOMB_IMG, (ability_size, ability_size))
            screen.blit(scaled_img, (top_left_x, top_left_y))
        else:
            top_left_x = self.x * TILE_SIZE + (TILE_SIZE - ability_size) // 2
            top_left_y = self.y * TILE_SIZE + (TILE_SIZE - ability_size) // 2
            if self.destroy_frame_index < len(self.destroy_frames):
                frame_img = pygame.transform.scale(self.destroy_frames[self.destroy_frame_index],
                                                   (ability_size, ability_size))
                screen.blit(frame_img, (top_left_x, top_left_y))

    def start_disappear(self):
        self.disappearing = True
        self.destroy_frame_index = 0
        self.last_update = pygame.time.get_ticks()

    def is_destroyed(self):
        return self.disappearing and (self.destroy_frame_index >= len(self.destroy_frames))


class Player:
    def __init__(self, init_tile_x, init_tile_y, color, controls):
        # Para centrar el sprite de 120x120 en la casilla: x = tile_x*40 - 40
        self.x = init_tile_x * TILE_SIZE - 40
        self.y = init_tile_y * TILE_SIZE - 40
        self.color = color
        self.speed = 2
        self.align_speed = 1
        self.controls = controls
        self.health = 3
        self.bomb_range = 1
        self.bomb_limit = 1  # Máximo de bombas simultáneas
        self.sprite_size = 120
        self.hitbox_size = 36
        self.sprite_draw_offset_y = -10
        self.anim_frame = 0
        self.last_anim_update = time.time()
        self.anim_delay = 0.2
        self.current_direction = "right"
        self.prev_x = self.x
        self.prev_y = self.y
        self.last_step_sound = 0
        self.step_delay = 0.3

    def get_hitbox(self):
        center_x = self.x + self.sprite_size // 2
        center_y = self.y + self.sprite_size // 2
        left = center_x - self.hitbox_size // 2
        top = center_y - self.hitbox_size // 2
        return pygame.Rect(left, top, self.hitbox_size, self.hitbox_size)

    def get_center_tile(self):
        cx = self.x + self.sprite_size // 2
        cy = self.y + self.sprite_size // 2
        return int(cx // TILE_SIZE), int(cy // TILE_SIZE)

    def check_collision(self, grid, bombs):
        rect = self.get_hitbox()
        left_cell = rect.left // TILE_SIZE
        right_cell = (rect.right - 1) // TILE_SIZE
        top_cell = rect.top // TILE_SIZE
        bottom_cell = (rect.bottom - 1) // TILE_SIZE

        for cell_x in range(left_cell, right_cell + 1):
            for cell_y in range(top_cell, bottom_cell + 1):
                if cell_x < 0 or cell_x >= GRID_COLS or cell_y < 0 or cell_y >= GRID_ROWS:
                    return True
                if grid[cell_y][cell_x] in (1, 2, 3):
                    return True

        for bomb in bombs:
            bomb_rect = pygame.Rect(bomb.tile_x * TILE_SIZE, bomb.tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if rect.colliderect(bomb_rect):
                if self not in bomb.passable_players:
                    return True

        return False

    def is_compressed_vertically(self, grid):
        cx, cy = self.get_center_tile()
        up_block = (cy - 1 < 0) or (grid[cy - 1][cx] in (1, 2, 3))
        down_block = (cy + 1 >= GRID_ROWS) or (grid[cy + 1][cx] in (1, 2, 3))
        return up_block and down_block

    def is_compressed_horizontally(self, grid):
        cx, cy = self.get_center_tile()
        left_block = (cx - 1 < 0) or (grid[cy][cx - 1] in (1, 2, 3))
        right_block = (cx + 1 >= GRID_COLS) or (grid[cy][cx + 1] in (1, 2, 3))
        return left_block and right_block

    def auto_align_x_once(self, grid, bombs):
        cx, cy = self.get_center_tile()
        desired_x = cx * TILE_SIZE + (TILE_SIZE // 2) - self.sprite_size // 2
        dist = abs(self.x - desired_x)
        if dist == 0:
            return True
        step = min(self.align_speed, dist)
        step = step if (desired_x > self.x) else -step
        old_x = self.x
        self.x += step
        if self.check_collision(grid, bombs):
            self.x = old_x
            return True
        if abs(self.x - desired_x) == 0:
            return True
        return False

    def auto_align_y_once(self, grid, bombs):
        cx, cy = self.get_center_tile()
        desired_y = cy * TILE_SIZE + (TILE_SIZE // 2) - self.sprite_size // 2
        dist = abs(self.y - desired_y)
        if dist == 0:
            return True
        step = min(self.align_speed, dist)
        step = step if (desired_y > self.y) else -step
        old_y = self.y
        self.y += step
        if self.check_collision(grid, bombs):
            self.y = old_y
            return True
        if abs(self.y - desired_y) == 0:
            return True
        return False

    def move_in_small_steps(self, dx, dy, grid, bombs):
        for _ in range(int(self.speed)):
            old_x, old_y = self.x, self.y
            self.x += dx
            self.y += dy
            if self.check_collision(grid, bombs):
                self.x, self.y = old_x, old_y
                break

    def move_up(self, grid, bombs):
        self.current_direction = "up"
        if self.is_compressed_vertically(grid):
            return
        aligned = self.auto_align_x_once(grid, bombs)
        if aligned:
            self.move_in_small_steps(0, -1, grid, bombs)

    def move_down(self, grid, bombs):
        self.current_direction = "down"
        if self.is_compressed_vertically(grid):
            return
        aligned = self.auto_align_x_once(grid, bombs)
        if aligned:
            self.move_in_small_steps(0, 1, grid, bombs)

    def move_left(self, grid, bombs):
        self.current_direction = "left"
        if self.is_compressed_horizontally(grid):
            return
        aligned = self.auto_align_y_once(grid, bombs)
        if aligned:
            self.move_in_small_steps(-1, 0, grid, bombs)

    def move_right(self, grid, bombs):
        self.current_direction = "right"
        if self.is_compressed_horizontally(grid):
            return
        aligned = self.auto_align_y_once(grid, bombs)
        if aligned:
            self.move_in_small_steps(1, 0, grid, bombs)

    def update_passable(self, bombs):
        hitbox = self.get_hitbox()
        for bomb in bombs:
            bomb_rect = pygame.Rect(bomb.tile_x * TILE_SIZE, bomb.tile_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if self in bomb.passable_players:
                intersection = hitbox.clip(bomb_rect)
                intersection_area = intersection.width * intersection.height
                total_area = self.hitbox_size * self.hitbox_size
                if intersection_area < total_area / 2:
                    cx, cy = self.get_center_tile()
                    desired_x = cx * TILE_SIZE - 40
                    desired_y = cy * TILE_SIZE - 40
                    correction_factor = 0.15 * self.align_speed
                    self.x += (desired_x - self.x) * correction_factor
                    self.y += (desired_y - self.y) * correction_factor
                    if abs(desired_x - self.x) < 0.5 and abs(desired_y - self.y) < 0.5:
                        self.x = desired_x
                        self.y = desired_y
                        bomb.passable_players.remove(self)

    def update_animation(self, keys):
        moving = (keys[self.controls['right']] or keys[self.controls['left']] or
                  keys[self.controls['up']] or keys[self.controls['down']])
        if moving:
            current_time = time.time()
            if (self.x != self.prev_x or self.y != self.prev_y) and (current_time - self.last_step_sound >= self.step_delay):
                FOOTSTEP_SOUND.play()
                self.last_step_sound = current_time
            if (self.x, self.y) != (self.prev_x, self.prev_y):
                if time.time() - self.last_anim_update >= self.anim_delay:
                    self.anim_frame = (self.anim_frame + 1) % 9
                    self.last_anim_update = time.time()
            else:
                self.anim_frame = 0
        else:
            self.anim_frame = 0

        self.prev_x = self.x
        self.prev_y = self.y

    def draw(self, screen):
        if self.color == RED:
            if self.current_direction == "right":
                image = RED_RIGHT_IMAGES[self.anim_frame]
            elif self.current_direction == "left":
                image = RED_LEFT_IMAGES[self.anim_frame]
            elif self.current_direction == "up":
                image = RED_UP_IMAGES[self.anim_frame]
            elif self.current_direction == "down":
                image = RED_DOWN_IMAGES[self.anim_frame]
            else:
                image = RED_RIGHT_IMAGES[0]
            screen.blit(image, (self.x, self.y + self.sprite_draw_offset_y))
        elif self.color == BLUE:
            if self.current_direction == "right":
                image = BLUE_RIGHT_IMAGES[self.anim_frame]
            elif self.current_direction == "left":
                image = BLUE_LEFT_IMAGES[self.anim_frame]
            elif self.current_direction == "up":
                image = BLUE_UP_IMAGES[self.anim_frame]
            elif self.current_direction == "down":
                image = BLUE_DOWN_IMAGES[self.anim_frame]
            else:
                image = BLUE_RIGHT_IMAGES[0]
            screen.blit(image, (self.x, self.y + self.sprite_draw_offset_y))

    def place_bomb(self, bombs):
        current_bombs = [b for b in bombs if b.owner == self and not b.exploded]
        if len(current_bombs) >= self.bomb_limit:
            return
        cx = self.x + self.sprite_size // 2
        cy = self.y + self.sprite_size // 2
        bomb_tile_x = int(cx // TILE_SIZE)
        bomb_tile_y = int(cy // TILE_SIZE)
        for b in bombs:
            if b.tile_x == bomb_tile_x and b.tile_y == bomb_tile_y:
                return
        new_bomb = Bomb(bomb_tile_x, bomb_tile_y, self.bomb_range)
        new_bomb.owner = self
        new_bomb.passable_players.add(self)
        bombs.append(new_bomb)
        # Reproducir sonido al colocar bomba
        COLOCAR_BOMBA_SOUND.play()


class Bomb:
    def __init__(self, tile_x, tile_y, blast_range):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.blast_range = blast_range
        self.timer = 3  # Detonación a 3 segundos
        self.plant_time = time.time()
        self.exploded = False
        self.passable_players = set()
        self.chain_triggered = False
        self.chain_trigger_time = None
        self.owner = None

    def explode(self, grid, players, bombs, powerups):
        if self.exploded:
            return []
        self.exploded = True
        if self in bombs:
            bombs.remove(self)
        EXPLOSION_SOUND.play()
        explosions = [(self.tile_x, self.tile_y)]
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            for i in range(1, self.blast_range + 1):
                nx = self.tile_x + dx * i
                ny = self.tile_y + dy * i
                if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                    if grid[ny][nx] == 1:
                        grid[ny][nx] = 0
                        explosions.append((nx, ny))
                        reveal_powerup_if_any(powerups, nx, ny)
                        break
                    elif grid[ny][nx] in (2, 3):
                        break
                    # Si hay una habilidad en la celda, la hace desaparecer y detiene la propagación
                    found_powerup = False
                    for p in powerups:
                        if p.x == nx and p.y == ny and p.visible and not p.disappearing:
                            p.start_disappear()
                            explosions.append((nx, ny))
                            found_powerup = True
                            break
                    if found_powerup:
                        break
                    # Explosión en cadena
                    for b in bombs:
                        if (b.tile_x, b.tile_y) == (nx, ny) and not b.exploded and not b.chain_triggered:
                            b.chain_triggered = True
                            b.chain_trigger_time = time.time()
                    explosions.append((nx, ny))
        for (ex, ey) in explosions:
            for player in players:
                if player.get_center_tile() == (ex, ey):
                    player.health -= 1
        return explosions

    def draw(self, screen):
        if self.chain_triggered:
            total_time = 0.75  # Delay para explosión en cadena
            elapsed = time.time() - self.chain_trigger_time
        else:
            total_time = 3.0
            elapsed = time.time() - self.plant_time
        frame_time = total_time / 15.0
        frame_index = min(int(elapsed / frame_time), 14)
        bomb_image = BOMB_IMAGES[frame_index]
        base_scale = 1.4
        oscillation = 0.15 * math.sin(2 * math.pi * (elapsed / total_time))
        scale_factor = base_scale + oscillation
        bomb_image_scaled = pygame.transform.scale(
            bomb_image,
            (int(bomb_image.get_width() * scale_factor),
             int(bomb_image.get_height() * scale_factor))
        )
        px = self.tile_x * TILE_SIZE + (TILE_SIZE - bomb_image_scaled.get_width()) // 2
        py = self.tile_y * TILE_SIZE + (TILE_SIZE - bomb_image_scaled.get_height()) // 2
        screen.blit(bomb_image_scaled, (px, py))


class Explosion:
    def __init__(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.frames = EXPLOSION_FRAMES
        self.current_frame = 0
        self.frame_duration = 0.1
        self.last_update = pygame.time.get_ticks()
        self.finished = False

    def update(self):
        now = pygame.time.get_ticks()
        if not self.finished and (now - self.last_update > self.frame_duration * 1000):
            self.current_frame += 1
            self.last_update = now
            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            px = self.tile_x * TILE_SIZE
            py = self.tile_y * TILE_SIZE
            screen.blit(self.frames[self.current_frame], (px, py))


# ------------------------------------------------------------------------------------
# Funciones de powerups y generación del mapa
# ------------------------------------------------------------------------------------
def get_powerup_at(powerups, x, y):
    for p in powerups:
        if p.x == x and p.y == y and p.visible:
            return p
    return None

def reveal_powerup_if_any(powerups, x, y):
    for p in powerups:
        if p.x == x and p.y == y and not p.visible:
            p.visible = True

def update_powerups(powerups):
    to_remove = []
    for p in powerups:
        p.update()
        if p.is_destroyed():
            to_remove.append(p)
    for r in to_remove:
        powerups.remove(r)

def draw_powerups(screen, powerups):
    for p in powerups:
        p.draw(screen)

def check_pickup(players, powerups):
    to_remove = []
    for p in powerups:
        if p.visible and not p.disappearing:
            for player in players:
                if player.get_center_tile() == (p.x, p.y):
                    if p.type == "major_explosion":
                        player.bomb_range += 1
                    elif p.type == "speed":
                        player.speed += 0.5
                        player.align_speed += 0.5
                    elif p.type == "more_bomb":
                        player.bomb_limit += 1
                    # Reproducir sonido al recoger la habilidad
                    COGER_HABILIDAD_SOUND.play()
                    to_remove.append(p)
                    break
    for r in to_remove:
        powerups.remove(r)

def generate_grid_and_powerups():
    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    powerups = []
    # Bordes
    for x in range(GRID_COLS):
        grid[0][x] = 3
        grid[GRID_ROWS - 1][x] = 3
    for y in range(GRID_ROWS):
        grid[y][0] = 3
        grid[y][GRID_COLS - 1] = 3
    # Rellenar interior
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            grid[y][x] = 0
    # Paredes de piedra (2) en subregión
    for y in range(2, 15):
        for x in range(2, 19):
            if (x % 2 == 0) and (y % 2 == 0):
                grid[y][x] = 2
    # Ladrillos (1) con probabilidad
    for y in range(1, GRID_ROWS - 1):
        for x in range(1, GRID_COLS - 1):
            if grid[y][x] == 0:
                if random.random() < 0.7:
                    grid[y][x] = 1
                    r = random.random()
                    if r < 0.1:
                        powerups.append(PowerUp(x, y, "speed"))
                    elif r < 0.3:
                        powerups.append(PowerUp(x, y, "major_explosion"))
                    elif r < 0.4:
                        powerups.append(PowerUp(x, y, "more_bomb"))
    def create_L_of_free_tiles(grid, corner_x, corner_y, hd, vd):
        if grid[corner_y][corner_x] == 1:
            grid[corner_y][corner_x] = 0
        H = random.choice([2, 3])
        V = random.choice([2, 3])
        for i in range(1, H + 1):
            xx = corner_x + i * hd
            yy = corner_y
            if 1 <= xx < GRID_COLS - 1 and 1 <= yy < GRID_ROWS - 1:
                if grid[yy][xx] in (0, 1):
                    grid[yy][xx] = 0
                elif grid[yy][xx] in (2, 3):
                    break
        for j in range(1, V + 1):
            xx = corner_x
            yy = corner_y + j * vd
            if 1 <= xx < GRID_COLS - 1 and 1 <= yy < GRID_ROWS - 1:
                if grid[yy][xx] in (0, 1):
                    grid[yy][xx] = 0
                elif grid[yy][xx] in (2, 3):
                    break

    create_L_of_free_tiles(grid, 1, 1, +1, +1)
    create_L_of_free_tiles(grid, GRID_COLS - 2, 1, -1, +1)
    create_L_of_free_tiles(grid, 1, GRID_ROWS - 2, +1, -1)
    create_L_of_free_tiles(grid, GRID_COLS - 2, GRID_ROWS - 2, -1, -1)

    return grid, powerups

def draw_grid(screen, grid):
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[y][x] == 0:
                screen.blit(GRASS, rect)
            elif grid[y][x] == 1:
                screen.blit(BRICK, rect)
            elif grid[y][x] == 2:
                screen.blit(STONE, rect)
            elif grid[y][x] == 3:
                screen.blit(LIMIT_IMG, rect)

def draw_grid_lines(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    line_color = (0, 0, 0, 80)
    for row in range(GRID_ROWS + 1):
        start = (0, row * TILE_SIZE)
        end = (WIDTH, row * TILE_SIZE)
        pygame.draw.line(overlay, line_color, start, end, 1)
    for col in range(GRID_COLS + 1):
        start = (col * TILE_SIZE, 0)
        end = (col * TILE_SIZE, HEIGHT)
        pygame.draw.line(overlay, line_color, start, end, 1)
    screen.blit(overlay, (0, 0))

def main():
    clock = pygame.time.Clock()
    grid, powerups = generate_grid_and_powerups()

    players = [
        Player(1, 1, RED, {
            'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d, 'bomb': pygame.K_SPACE
        }),
        Player(19, 15, BLUE, {
            'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'bomb': pygame.K_RETURN
        }),
    ]
    bombs = []
    explosions = []

    running = True
    while running:
        screen.fill(BLACK)
        draw_grid(screen, grid)
        draw_grid_lines(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for player in players:
                    if event.key == player.controls['bomb']:
                        player.place_bomb(bombs)

        keys = pygame.key.get_pressed()
        for player in players:
            if keys[player.controls['up']]:
                player.move_up(grid, bombs)
            elif keys[player.controls['down']]:
                player.move_down(grid, bombs)
            elif keys[player.controls['left']]:
                player.move_left(grid, bombs)
            elif keys[player.controls['right']]:
                player.move_right(grid, bombs)

            player.update_animation(keys)
            player.update_passable(bombs)

        # Explosión de bombas
        for bomb in bombs[:]:
            if bomb.chain_triggered:
                if time.time() - bomb.chain_trigger_time >= 0.75:
                    exp_positions = bomb.explode(grid, players, bombs, powerups)
                    for (tx, ty) in exp_positions:
                        explosions.append(Explosion(tx, ty))
            elif time.time() - bomb.plant_time >= bomb.timer:
                exp_positions = bomb.explode(grid, players, bombs, powerups)
                for (tx, ty) in exp_positions:
                    explosions.append(Explosion(tx, ty))

        update_powerups(powerups)
        draw_powerups(screen, powerups)
        check_pickup(players, powerups)

        # Dibujar bombas
        for bomb in bombs:
            bomb.draw(screen)

        # Dibujar jugadores
        for player in players:
            player.draw(screen)

        # Dibujar explosiones
        for explosion in explosions[:]:
            explosion.update()
            if explosion.finished:
                explosions.remove(explosion)
            else:
                explosion.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
