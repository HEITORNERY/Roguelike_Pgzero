from pgzero.keyboard import keyboard, keys
from pgzero.builtins import Actor
from pygame import Rect
import random
import math

class Player:
    def __init__(self, level):
        
        # player vai começar num tile livre 
        self.level = level
        self.tile_free = level.floor_tiles
        self.tile_size = level.tile_size
        gx, gy = random.choice(self.tile_free)
        self.x = gx * self.tile_size + self.tile_size/2
        self.y = gy * self.tile_size + self.tile_size/2

        # velocidade do player
        self.speed = 100

        # estado de animação e direção do player
        self.state = "idle"
        self.direction = "E"

        # timers e frame da animação
        self.frame_timer = 0
        self.frame_index = 0
        self.cooldown_timer = 0
        self.cooldown_attack = 1

        # vida e dano do player 
        self.health = 10.0
        self.damage = 3

        # sprites das animações do player com suas direções
        self.sprite_sheets = {
            "idle": "idle_side_hero_sheet",
            "run": "hero_run_side-sheet",
            "attack": "side_attack_hero_sheet"
        }

        # quantidade de frames por animação
        self.frames = {
            "idle": 4,
            "run": 6,
            "attack": 8
        }

    # função para movimentar o player
    def update(self, dt, enemies):
        dx = dy = 0

        # lógica de movimentação baseada nas teclas
        if keyboard[keys.LEFT]:
            dx = -1
            self.direction = "W"
        elif keyboard[keys.RIGHT]:
            dx = 1
            self.direction = "E"
        if keyboard[keys.DOWN]:
            dy = 1
        elif keyboard[keys.UP]:
            dy = -1

        # adicionando velocidade ao movimento do player
        if dx != 0 or dy != 0:
            if self.state != "attack":
                self.state = "run"
            else:
                self.state = "attack"
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt

            self.x = new_x
            self.y = new_y

        else:
            if self.state != "attack":
                self.state = "idle"

        # implementar a lógica de ataque
        self.cooldown_timer = max(0, self.cooldown_timer - dt)
        if self.cooldown_timer == 0:
            for e in enemies:
                distance = math.hypot(e.pos_y - self.y, e.pos_x - self.x)
                if distance <= 17:
                    self.state = "attack"
                    self.cooldown_timer = self.cooldown_attack
                    self.frame_index = 0
                    self.frame_timer = 0
                    e.hit(self.damage)
                    break
        
        # atualizar a animação
        self.frame_timer += dt
        if self.frame_timer >= 0.05:
            self.frame_timer -= 0.05
            self.frame_index = (self.frame_index + 1) % self.frames[self.state]

            # volta ao estado de idle após acabar o ataque
            if self.frame_index == 0 and self.state == "attack":
                self.state = "idle"
                self.cooldown_timer = 0
        
    # função para colocar os sprites na cena
    def draw(self, screen, font):
        
        base = self.sprite_sheets[self.state]
        
        # adicionar o nome flip para usar o outro sprite
        name = base + "_flip" if self.direction == "W" else base                        

        total = self.frames[self.state]
        actor = Actor(name)
        fw = actor._surf.get_width() // total
        fh = actor._surf.get_height()

        # Garantir que o frame_index está dentro dos limites
        self.frame_index = min(self.frame_index, total - 1)
        rect = Rect(self.frame_index * fw,0,fw,fh)
        frame = actor._surf.subsurface(rect)
        
        screen.blit(frame, (self.x - fw/2, self.y - fh/2))
        screen.draw.text(f"HP: {self.health}", (560, 0), color="white", fontsize=24)