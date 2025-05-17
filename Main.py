# Código para o pgzero rodar e gerar o cenário
import pgzrun

# importar o código para gerar o mapa
from LevelMapGenerator import Level

# importar o código do inimigo
from Enemy import Enemy

# importar o código do Player
from Player import Player

# configuração da janela
COLS = 40
ROWS = 30
TILE_SIZE = 16
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE

# Carregar as informações para geração do cenário na Level
level = Level(COLS, ROWS, TILE_SIZE)
level.generate_map(num_trees = 10, num_mushroom=10, num_bush= 10)

# lista de inimigos na cena
enemies = []

# instanciar o player
player = Player(level)

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
        e.update(dt, player, level.wave_number)

        # se o inimigo morreu remover ele da cena
        if e.death_timer <= 0 and e.state == "death":
            enemies.remove(e)
            if e in level.enemies_active:
                level.enemies_active.remove(e)
    
    player.update(dt, enemies)

# função do pgzero para desenhar
def draw():
    screen.clear()

    # desenhar o cenário
    level.draw(screen)

    # desenhar o inimigo na cena
    for e in enemies:
        e.draw(screen)

    # desenhar o player
    player.draw(screen, "Arial")

    # desenhar o timer
    level.draw_hud(screen, "Arial")

# iniciar o pgzero
pgzrun.go()