# Código para o pgzero rodar e gerar o cenário
import pgzrun

# importar o código para gerar o mapa
from LevelMapGenerator import Level

# configuração da janela
COLS = 40
ROWS = 30
TILE_SIZE = 16
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

# Carregar as informações para geração do cenário na Level
level = Level(COLS, ROWS, TILE_SIZE)
level.generate_map(num_trees = 30)

# função do pgzero para desenhar o cenário
def draw():
    level.draw(screen)

# iniciar o pgzero
pgzrun.go()