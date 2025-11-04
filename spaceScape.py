##############################################################
###               S P A C E     E S C A P E                ###
##############################################################
###                  versao Alpha 0.3                      ###
##############################################################
### Objetivo: desviar dos meteoros que caem.               ###
### Cada colisão tira uma vida. Sobreviva o máximo que     ###
### conseguir!                                             ###
##############################################################
### Prof. Filipo Novo Mor - github.com/ProfessorFilipo     ###
##############################################################

import pygame
import random
import os

# Inicializa o PyGame
pygame.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS DO JOGO
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("🚀 Space Escape")

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS (os alunos podem trocar os arquivos aqui)
# ----------------------------------------------------------
# Dica: coloque as imagens e sons na mesma pasta do arquivo .py
# e troque apenas os nomes abaixo.

ASSETS = {
    "background": "fundo001.png",                         # imagem de fundo
    "player": "alien001.png",                                    # imagem da nave
    "player2": "alienamigo001.png",                                    # imagem da nave 2
    "meteor": "meteor002.png",                                 # imagem do meteoro
    "sound_point": "classic-game-action-positive-5-224402.mp3", # som ao desviar com sucesso
    "sound_hit": "explosaouau.mp3",                # som de colisão
    "music": "Monkeys_Spinning_Monkeys.mp3"          # música de fundo. direitos: Music by Maksym Malko from Pixabay
}

# ----------------------------------------------------------
# 🖼️ CARREGAMENTO DE IMAGENS E SONS
# ----------------------------------------------------------
# Cores para fallback (caso os arquivos não existam)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)

# Tela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Função auxiliar para carregar imagens de forma segura
def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        img = pygame.image.load(filename).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    else:
        # Gera uma superfície simples colorida se a imagem não existir
        surf = pygame.Surface(size or (50, 50))
        surf.fill(fallback_color)
        return surf

# Carrega imagens
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (64, 64))
player2_img = load_image(ASSETS["player2"], BLUE, (64, 64))
meteor_img = load_image(ASSETS["meteor"], RED, (40, 40))

# Sons
def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None

sound_point = load_sound(ASSETS["sound_point"])
sound_hit = load_sound(ASSETS["sound_hit"])

# Música de fundo (opcional)
if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)  # loop infinito

# ----------------------------------------------------------
# 🧠 VARIÁVEIS DE JOGO
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player_speed = 7

player2_rect = player2_img.get_rect(center=(WIDTH // 2, HEIGHT - 60))
player2_speed = 7

meteor_list = []
for _ in range(5):
    x = random.randint(0, WIDTH - 40)
    y = random.randint(-500, -40)
    meteor_list.append(pygame.Rect(x, y, 40, 40))
meteor_speed = 5

death = False
death2 = False
score = 0
lives = 3
score2 = 0
lives2 = 3
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True

# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
while running:
    clock.tick(FPS)
    screen.blit(background, (0, 0))

    # --- Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Movimento do jogador ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.y -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        player_rect.x += player_speed
    if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect.y += player_speed

    # --- Movimento do jogador 2 ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player2_rect.left > 0:
        player2_rect.x -= player2_speed
    if keys[pygame.K_w] and player2_rect.top > 0:
        player2_rect.y -= player2_speed
    if keys[pygame.K_d] and player2_rect.right < WIDTH:
        player2_rect.x += player2_speed
    if keys[pygame.K_s] and player2_rect.bottom < HEIGHT:
        player2_rect.y += player2_speed

    # --- Movimento dos meteoros ---
    for meteor in meteor_list:
        meteor.y += meteor_speed

        # Saiu da tela → reposiciona e soma pontos
        if meteor.y > HEIGHT:
            meteor.y = random.randint(-100, -40)
            meteor.x = random.randint(0, WIDTH - meteor.width)
            if not death:
                score += 1
            if not death2:
                score2 += 1
            if sound_point:
                sound_point.play()

        # Colisão
        if meteor.colliderect(player_rect):
            if not death:
                lives -= 1
                meteor.y = random.randint(-100, -40)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                if sound_hit:
                    sound_hit.play()

        # Colisão p2
        if meteor.colliderect(player2_rect):
            if not death2:
                lives2 -= 1
                meteor.y = random.randint(-100, -40)
                meteor.x = random.randint(0, WIDTH - meteor.width)
                if sound_hit:
                    sound_hit.play()

        # Fim de jogo
        if lives2 <= 0 and lives <= 0:
            running = False

    # --- Desenha tudo ---
    if lives > 0:
        screen.blit(player_img, player_rect)
    else:
        death = True
    if lives2 > 0:
        screen.blit(player2_img, player2_rect)
    else:
        death2 = True
    for meteor in meteor_list:
        screen.blit(meteor_img, meteor)

    # --- Exibe pontuação e vidas ---
    text = font.render(f"Pontos: {score}   Vidas: {lives}", True, WHITE)
    screen.blit(text, (10, 10))
    text = font.render(f"Pontos2: {score2}   Vidas2: {lives2}", True, WHITE)
    screen.blit(text, (20, 20))

    pygame.display.flip()

# ----------------------------------------------------------
# 🏁 TELA DE FIM DE JOGO
# ----------------------------------------------------------
pygame.mixer.music.stop()
screen.fill((20, 20, 20))
end_text = font.render("Fim de jogo! Pressione qualquer tecla para sair.", True, WHITE)
final_score = font.render(f"Pontuação final: {score}", True, WHITE)
screen.blit(end_text, (150, 260))
screen.blit(final_score, (300, 300))
pygame.display.flip()

waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
