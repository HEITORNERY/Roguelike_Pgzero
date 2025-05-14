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
        self.house_tiles = []
    
    # função para organizar os tiles no cenário
    def generate_map(self, num_trees):
        
        # primeiro vou definir as posições dos tiles do floor por todo o cenário
        self.floor_tiles = [(x,y) for x in range(self.cols) for y in range(self.rows)]

        # onde foi adicionado um tile de floor pode ser adicionado um tile de tree
        available = list(self.floor_tiles)

        # vou escolher uma posição dentre as que tem o tile do floor para adicionar um tile de tree
        trees = 0
        while trees < num_trees:
            pos = random.choice(self.floor_tiles)
            self.tree_tiles.append(pos)
            available.remove(pos)
            trees += 1
        
        # adicionar a casa no centro
        house_pos_x = self.cols//2
        house_pos_y = self.rows//2
        self.house_tiles = [((house_pos_x, house_pos_y), "house_bottom"), ((house_pos_x, house_pos_y - 1), "house_top")]
        
        # remover os tiles da casa dos tiles disponíveis restantes
        for pos in self.house_tiles:
            if pos in available:
                available.remove(pos)

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

        # adicionar os tiles da casa
        for (x,y), image_name in self.house_tiles:
            pos_x = x * self.tile_size
            pos_y = y * self.tile_size
            screen.blit(image_name, (pos_x, pos_y))