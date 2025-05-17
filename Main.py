# Código para o pgzero rodar e gerar o cenário
import pgzrun

# importar o código para gerar o mapa
from LevelMapGenerator import Level

# importar o código do inimigo
from Enemy import Enemy

# importar o código do Player
from Player import Player

from pygame import Rect

# Estados do jogo
class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

# Configurações globais
current_state = GameState.MENU
sound_enabled = True
music_enabled = True

# variáveis para controle de tempo
elapsed_time = 0
start_time = 0

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

# função para desenhar o menu
def draw_menu():
    screen.clear()
    screen.fill((30, 30, 40))
    
    # Título
    screen.draw.text(
        "Run, Fight and Try don't die!",
        center=(WIDTH//2, HEIGHT//4),
        fontsize=60,
        color="white"
    )
    
    # Botões
    buttons = [
        ("Start Game", (WIDTH//2, HEIGHT//2)),
        ("Music: On" if music_enabled else "Music: Off", (WIDTH//2, HEIGHT//2 + 50)),
        ("Sounds: On" if sound_enabled else "Sounds: Off", (WIDTH//2, HEIGHT//2 + 100)),
        ("Sair", (WIDTH//2, HEIGHT//2 + 150))
    ]
    
    for i, (text, pos) in enumerate(buttons):
        box = Rect(pos[0]-100, pos[1]-15, 200, 30)
        color = (200, 50, 50) if i == 3 else (50, 100, 200)
        screen.draw.filled_rect(box, color)
        screen.draw.text(
            text,
            center=pos,
            fontsize=30,
            color="white"
        )

# função de spawn do inimigo que o level chama
def spawn_enemy(pos):
    pos_x, pos_y = pos

    # centralizar o inimigo na posição que aparecer
    px = pos_x * TILE_SIZE + TILE_SIZE//2
    py = pos_y * TILE_SIZE + TILE_SIZE//2

    # adicionando o inimigo e salvando ele na lista
    enemy = Enemy(px,py, sound_enabled)
    enemies.append(enemy)
    level.enemies_active.append(enemy)

# função para atualizar o temporizador das waves, remover inimigos mortos e atualizar cada inimigo
def update(dt):

    global current_state, enemies_killed, elapsed_time
    
    if current_state == GameState.PLAYING:
        elapsed_time += dt

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

        # Verificar condições de derrota
        if player.health <= 0 or is_out_of_bounds():
            current_state = GameState.GAME_OVER
            if music_enabled:
                music.stop()

# função do pgzero para desenhar os objetos na cena
def draw():
    screen.clear()
    
    if current_state == GameState.MENU:
        draw_menu()
    elif current_state == GameState.PLAYING:
        level.draw(screen)
        level.draw_hud(screen)
        for e in enemies:
            e.draw(screen)
        player.draw(screen)
    elif current_state == GameState.GAME_OVER:
        draw_game_over()

# função da tela de fim de jog0
def draw_game_over():
    screen.fill((40, 30, 30))
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    
    screen.draw.text(
        "Game Over",
        center=(WIDTH//2, HEIGHT//4),
        fontsize=60,
        color="red"
    )
    
    stats = [
        f"Enemies Defeat: {player.enemies_killed}",
        f"Living Time: {minutes:02}:{seconds:02}",
    ]
    
    for i, text in enumerate(stats):
        screen.draw.text(
            text,
            center=(WIDTH//2, HEIGHT//2 + i*40),
            fontsize=40 if i < 2 else 30,
            color="white"
        )

# função que encerra o jogo se sair do mapa 
def is_out_of_bounds():
    return (player.x < 0 or player.x > WIDTH or
            player.y < 0 or player.y > HEIGHT)

# função para iniciar o jogo depois de apertar o botão
def start_game():
    global current_state, level, player, enemies, elapsed_time, enemies_killed
    current_state = GameState.PLAYING
    enemies_killed = 0
    elapsed_time = 0
    
    # Reiniciar todos os objetos do jogo
    level = Level(COLS, ROWS, TILE_SIZE)
    level.generate_map(num_trees=10, num_mushroom=10, num_bush=10)
    player = Player(level)
    enemies.clear()
    
    # Reiniciar música
    if music_enabled:
        music.play('background')
    else:
        music.stop()

def on_mouse_down(pos):
    global current_state, sound_enabled, music_enabled
    
    if current_state == GameState.MENU:
        x, y = pos
        # Verificar clique nos botões com coordenadas relativas
        button_y_positions = [HEIGHT//2, HEIGHT//2 + 50, HEIGHT//2 + 100, HEIGHT//2 + 150]
        
        for index, btn_y in enumerate(button_y_positions):
            btn_area = Rect(
                WIDTH//2 - 100,  # x
                btn_y - 15,       # y
                200,             # width
                30               # height
            )
            if btn_area.collidepoint(x, y):
                handle_menu_click(index)
                break

def handle_menu_click(index):
    global current_state, music_enabled, sound_enabled
    if index == 0:
        start_game()
    elif index == 1:
        music_enabled = not music_enabled
        if music_enabled:
            music.play('background')
        else:
            music.stop()
    elif index == 2:
        sound_enabled = not sound_enabled
        for e in enemies:
            e.sound_enabled = sound_enabled
    elif index == 3:
        exit()

# iniciar o pgzero
pgzrun.go()