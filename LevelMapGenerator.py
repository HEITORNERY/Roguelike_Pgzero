import random
from pygame import Rect

# Esse código vai gerar o cenário, assim como gerenciar as ondas dos inimigos
class Level:
    # construtor da classe para os dados que serão necessários para gerar o level
    def __init__(self, cols, rows, tile_size):

        # o cenário vai ser dividido em linhas e colunas de acordo com o tamanho do tile do chão
        self.cols = cols
        self.rows = rows
        self.tile_size = tile_size

        # terão listas para armazenar as posições que são adicionados os tiles e os outros objetos que compõem o cenário
        self.floor_tiles = []
        self.tree_tiles = []
        self.mushroom_tiles = []
        self.bush_tiles = []

        # informações para as waves
        self.wave_number = 1 
        self.wave_timer = 20
        self.wave_enemies = 5
        self.wave_timer_left = self.wave_timer # tempo para acabar a wave
        self.enemie_counter = 0 # contador de inimigos spawnados
        self.enemies_active = [] # lista dos inimigos ativos 
    
    # função para organizar os tiles no cenário
    def generate_map(self, num_trees, num_mushroom, num_bush):
        
        # primeiro vou definir as posições dos tiles do floor por todo o cenário
        self.floor_tiles = [(x,y) for x in range(self.cols) for y in range(self.rows)]

        # onde foi adicionado um tile de floor pode ser adicionado um tile de tree
        available = list(self.floor_tiles)

        # vou escolher uma posição dentre as que tem o tile do floor para adicionar um tile de tree
        trees = 0
        while trees < num_trees:
            pos = random.choice(available)
            self.tree_tiles.append(pos)
            available.remove(pos)
            trees += 1
        
        mushroom = 0
        while mushroom < num_mushroom:
            pos = random.choice(available)
            self.mushroom_tiles.append(pos)
            available.remove(pos)
            mushroom += 1
        
        bush = 0
        while bush < num_bush:
            pos = random.choice(available)
            self.bush_tiles.append(pos)
            available.remove(pos)
            bush += 1

    def update(self, time_frame, spawn_enemy_callback):

        # iniciar o temporizador a cada frame vai ser diminuido do temporizador
        self.wave_timer_left = max(0.0, self.wave_timer_left - time_frame) 

        # iniciar o spawn dos inimigos
        if self.enemie_counter < self.wave_enemies:
            interval_spawn_enemie = self.wave_timer/self.wave_enemies

            # verifica se já passou o tempo para spawnar um novo inimigo
            if (self.wave_timer -  self.wave_timer_left) >= (interval_spawn_enemie * self.enemie_counter):

                # sortear a posição de spawn dos inimigos
                pos_random_spawn = random.choice(["top", "bottom", "left", "right"])
                x = random.randint(0, self.cols)
                y = random.randint(0, self.rows)
                if pos_random_spawn == "top":
                    spawn_pos = (x, 0)
                elif pos_random_spawn == "bottom":
                    spawn_pos = (x, self.rows)
                elif pos_random_spawn == "left":
                    spawn_pos = (0, y)
                else:
                    spawn_pos = (self.cols, y)
                
                # chamar a função de spawn dos inimigos
                spawn_enemy_callback(spawn_pos)
                self.enemie_counter += 1
        
        # acabou o tempo e não tem inimigos ativos, então deve ser iniciado uma nova onda 
        if self.wave_timer_left <= 0:
            self.enemies_active.clear()
            self.next_wave()

    # função para adicionar os sprites dos tiles no cenário
    def draw(self, screen):

        # adicionar os tiles do chão
        for x,y in self.floor_tiles:
            pos_x = x * self.tile_size
            pos_y = y * self.tile_size
            screen.blit("floor", (pos_x, pos_y))
        
        # adicionar os tiles das árvores
        for x,y in self.tree_tiles:
            pos_x = x * self.tile_size
            pos_y = y * self.tile_size
            screen.blit("tree", (pos_x, pos_y))

        for x,y in self.mushroom_tiles:
            pos_x = x * self.tile_size
            pos_y = y * self.tile_size
            screen.blit("mushroom", (pos_x, pos_y))
        
        for x,y in self.bush_tiles:
            pos_x = x * self.tile_size
            pos_y = y * self.tile_size
            screen.blit("bush", (pos_x, pos_y))

    def next_wave(self):
        self.wave_number += 1 # próxima wave 
        self.wave_enemies += 2 # aumenta 2 inimigos por wave
        self.enemie_counter = 0
        self.wave_timer += 2
        self.wave_timer_left = self.wave_timer

    # função para escrever o timer na tela
    def draw_hud(self, screen, font):
        screen.draw.text(f"Wave: {self.wave_number}", (310, 0), color="white", fontsize=24)
        minutes = int(self.wave_timer_left) // 60
        seconds = int(self.wave_timer_left) % 60
        screen.draw.text(f"Time: {minutes:02d}:{seconds:02d}", (300, 30), color="white", fontsize=24)