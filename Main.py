# Código para o pgzero rodar e gerar o cenário
import pgzrun

# importar o código para gerar o mapa
from LevelMapGenerator import Level

# importar o código do inimigo
from Enemy import Enemy

# configuração da janela
COLS = 40
ROWS = 30
TILE_SIZE = 16
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

# Carregar as informações para geração do cenário na Level
level = Level(COLS, ROWS, TILE_SIZE)
level.generate_map(num_trees = 30)

# lista de inimigos na cena
enemies = []

# função de spawn do inimigo que o level chama
def spawn_enemy(pos):
    pos_x, pos_y = pos

    # centralizar o inimigo na posição que aparecer
    px = pos_x * TILE_SIZE + TILE_SIZE//2
    py = pos_y * TILE_SIZE + TILE_SIZE//2

    # adicionando o inimigo e salvando ele na lista
    enemy = Enemy(px,py)
    enemies.append(enemy)
    level.enemies_active.append(enemy)

# função para atualizar o temporizador das waves, remover inimigos mortos e atualizar cada inimigo
def update(dt):

    # atualizar waves 
    level.update(dt, spawn_enemy)

    # atualizar cada inimigo
    for e in enemies:
        e.update(dt, level)

        # se o inimigo morreu remover ele da cena
        if e.death_timer <= 0 and e.state == "death":
            enemies.remove(e)
            if e in level.enemies_active:
                level.enemies_active.remove(e)

# função do pgzero para desenhar
def draw():
    screen.clear

    # desenhar o cenário
    level.draw(screen)

    # desenhar o inimigo na cena
    for e in enemies:
        e.draw(screen)

    # desenhar o timer
    level.draw_hud(screen, "Arial")

# iniciar o pgzero
pgzrun.go()