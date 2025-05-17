import math
from pygame import Rect
from pgzero.builtins import Actor


class Enemy:
    def __init__(self, x, y):

        # posição e velocidade
        self.pos_x = x
        self.pos_y = y
        self.speed = 60

        self.state = "run" # animação que vai iniciar
        self.frame_timer = 0 # tempo para trocar de sprite
        self.frame_index = 0 # sprite que vai iniciar
        self.death_timer = 0.5 # tempo para a morte do enemy

        # sprites das animações
        self.sheet_run = Actor("enemy_run_sheet")
        self.sheet_death = Actor("enemy_death_sheet")

        # quantidade de frames por animação
        self.run_frames = 6
        self.death_frames = 6

        # vida do inimigo
        self.hp = 3

    # função para lidar com as animações do inimigo
    def update(self, dt, player, wave_number):

        # se foi morto decrementa o timer de morte
        if self.state == "death":
            self.death_timer -= dt
            return
        
        # calcular o destino 
        dx = player.x - self.pos_x
        dy = player.y - self.pos_y
        dist = math.hypot(dy, dx)
        min_dist = 16

        # calcula a distância mínima para causar dano ao jogador
        if dist <= min_dist:
            player.health = max(0, player.health - 0.1*dt)
            return
        
        # mover o inimigo até a casa
        angle = math.atan2(dy, dx)
        self.pos_x += math.cos(angle) * self.speed * dt
        self.pos_y += math.sin(angle) * self.speed * dt

        # inimigo deve atualizar sua animação a cada frame 
        self.frame_timer += dt

        # vou verificar se passou o tempo para atualizar o frame
        if self.frame_timer >= 0.15:
            self.frame_timer -= 0.15
            self.frame_index += 1

            if self.state == "run":
                max_frames = self.run_frames
            else:
                max_frames = self.death_frames
            
            # se passar do último frame fica em loop em run e pausa no último em idle e death
            if self.frame_index >= max_frames:
                if self.state == "run":
                    self.frame_index = 0
                else:
                    self.frame_index = max_frames - 1

        if wave_number > 1:
            min_dist += wave_number

    # função para colocar a imagem do inimigo na cena
    def draw(self, screen):
         
         # verificar qual animação está parecendo
        if self.state == "run":
            sheet = self.sheet_run
            max_frames = self.run_frames
        else:
            sheet = self.sheet_death
            max_frames = self.death_frames

        # calcular a largura e altura do frame
        width = sheet.width // max_frames
        height = sheet.height

        # cada sheet tem uma quantidade de frames que deve ser movido de um frame para outro usando o tamanho de cada frame
        rect = Rect(self.frame_index * width, 0, width, height)

        # retirar o frame do spritesheet
        frame_surf = sheet._surf.subsurface(rect)

        # desenhar o frame na tela
        screen.blit(frame_surf, (self.pos_x - width/2, self.pos_y - height/2))
    
    # função para o dano sofrido pelo player
    def hit(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.state = "death"
            self.frame_index = 0
            self.frame_timer = 0