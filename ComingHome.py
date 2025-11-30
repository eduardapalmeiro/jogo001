##############################################################
###               C O M I N G       H O M E                ###
##############################################################
### Objetivo: Levar o alien até sua casa e sobreviver      ###
### aos obstaculos.                                        ###
##############################################################
### Refatorado: OOP + Assets Reais para Meteoros Rosas     ###
##############################################################

import pygame
import random
import os
import cv2

# Inicializa o PyGame
pygame.init()
pygame.mixer.init()

# ----------------------------------------------------------
# 🔧 CONFIGURAÇÕES GERAIS
# ----------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.display.set_caption("👽 Coming home 👽")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Cores
WHITE = (255, 255, 255)
RED = (255, 60, 60)
BLUE = (60, 100, 255)
GREEN = (50, 239, 106)
DARK_GREEN = (13, 98, 70)

# ----------------------------------------------------------
# 🧩 SEÇÃO DE ASSETS
# ----------------------------------------------------------
ASSETS = {
    "background": "fundo001.png",
    "background2": "fundo002.png",
    "background3": "fundo003.png",
    "player": "alien001.png",
    "player2": "alienamigo001.png",
    "sound_point": "collect-points-190037.mp3",
    "sound_hit": "hit-soundvideo-game-type-230510.mp3",
    "music": "emotional-futuristic-ambient-flying-over-the-universe-322221.mp3",
    "death_sound": "videogame-death-sound-43894.mp3",
    "explosion_sound": "explosaouau.mp3",
    "menubg": "menubg.png",
    "winimg": "teladefinalbom.png",
    "loseimg": "teladefinalruim.png",
    "meteorolifeimg": "coracaometeoro.png",
    "transicaoFase1-2video": "1-2.mp4",
    "transicaoFase2-3video": "2-3.mp4",
    # Animação Normal
    "anim_meteoro": ["meteoro001.png", "meteoro002.png", "meteoro003.png"],
    # Animação Rosa (Novos Arquivos)
    "anim_meteoro_rosa": ["meteororosa001.png", "meteororosa002.png", "meteororosa003.png"],
    # Animação Explosão
    "anim_explosao": [f"explosao{i:03d}.png" for i in range(1, 8)]
}


def load_image(filename, fallback_color, size=None):
    if os.path.exists(filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            return img
        except Exception as e:
            print(f"Erro imagem {filename}: {e}")

    surf = pygame.Surface(size or (50, 50))
    surf.fill(fallback_color)
    return surf


def load_sound(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    return None


# --- Carregamento Imagens Estáticas ---
background = load_image(ASSETS["background"], WHITE, (WIDTH, HEIGHT))
background2 = load_image(ASSETS["background2"], WHITE, (WIDTH, HEIGHT))
background3 = load_image(ASSETS["background3"], WHITE, (WIDTH, HEIGHT))
player_img = load_image(ASSETS["player"], BLUE, (64, 64))
player2_img = load_image(ASSETS["player2"], BLUE, (64, 64))
meteorosLife_img = load_image(ASSETS["meteorolifeimg"], RED, (40, 40))
menubg = load_image(ASSETS["menubg"], WHITE, (WIDTH, HEIGHT))
winimg = load_image(ASSETS["winimg"], WHITE, (WIDTH, HEIGHT))
loseimg = load_image(ASSETS["loseimg"], WHITE, (WIDTH, HEIGHT))

# --- CARREGAMENTO DE ANIMAÇÕES ---

# 1. Carrega meteoros normais
meteor_frames_normal = []
for frame_file in ASSETS["anim_meteoro"]:
    img = load_image(frame_file, (100, 100, 100), (40, 40))
    meteor_frames_normal.append(img)

# 2. Carrega meteoros ROSAS (Agora usando os arquivos reais)
meteor_frames_pink = []
for frame_file in ASSETS["anim_meteoro_rosa"]:
    # Fallback cor rosa caso a imagem falhe
    img = load_image(frame_file, (255, 105, 180), (40, 40))
    meteor_frames_pink.append(img)

# 3. Carrega Explosão
explosion_frames = []
for frame_file in ASSETS["anim_explosao"]:
    img = load_image(frame_file, (255, 100, 0), (80, 80))
    explosion_frames.append(img)

# --- Carregamento Sons ---
sound_point = load_sound(ASSETS["sound_point"])
if sound_point: sound_point.set_volume(0.2)
sound_hit = load_sound(ASSETS["sound_hit"])
if sound_hit: sound_hit.set_volume(0.2)
sound_explosion = load_sound(ASSETS["explosion_sound"])
if sound_explosion: sound_explosion.set_volume(0.4)

if os.path.exists(ASSETS["music"]):
    pygame.mixer.music.load(ASSETS["music"])
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)


# ----------------------------------------------------------
# 🏛️ CLASSES
# ----------------------------------------------------------

class Meteor(pygame.sprite.Sprite):
    def __init__(self, normal_frames, pink_frames):
        super().__init__()
        self.normal_frames = normal_frames
        self.pink_frames = pink_frames

        self.current_frame = 0
        self.anim_speed = 0.05

        # Começa como normal
        self.is_pink = False
        self.frames = self.normal_frames
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

        # Inicializa
        self.reset_position(phase_level=1)

    def reset_position(self, phase_level=1):
        """Reinicia posição e decide se vira Rosa baseado na fase"""
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(-600, -50)

        # Lógica de Evolução: Só vira rosa na Fase 2 ou 3
        # Chance de 30% de ser rosa nessas fases
        if phase_level >= 2 and random.random() < 0.3:
            self.is_pink = True
            self.frames = self.pink_frames
            self.speed_y = random.randint(10, 14)  # Rosa é rápido
        else:
            self.is_pink = False
            self.frames = self.normal_frames
            self.speed_y = random.randint(4, 8)  # Normal

    def update(self, phase_level=1):
        self.rect.y += self.speed_y

        # Animação
        self.current_frame += self.anim_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # Saiu da tela? Reset passando o nível atual da fase
        if self.rect.y > HEIGHT:
            self.reset_position(phase_level)
            return True
        return False


class LifeBonus(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed_y = 5

    def reset_position(self):
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = random.randint(-1500, -100)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > HEIGHT:
            self.reset_position()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, frames):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.anim_speed = 0.25
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.current_frame += self.anim_speed
        if self.current_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.current_frame)]


# ----------------------------------------------------------
# 🧠 CONFIGURAÇÃO DE GRUPOS E VARIÁVEIS
# ----------------------------------------------------------
player_rect = player_img.get_rect(center=(WIDTH // 2 - 50, HEIGHT - 60))
player2_rect = player2_img.get_rect(center=(WIDTH // 2 + 50, HEIGHT - 60))
player_speed = 7
player2_speed = 7

meteor_group = pygame.sprite.Group()
life_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# Cria Meteoros passando AMBOS os tipos de frames
for _ in range(6):
    meteor_group.add(Meteor(meteor_frames_normal, meteor_frames_pink))

for _ in range(2):
    life_group.add(LifeBonus(meteorosLife_img))

death = False
death2 = False
video_fase1_2_rodou = False
video_fase2_3_rodou = False
score = 0
lives = 3
score2 = 0
lives2 = 3
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True


# ----------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------
def reproduzir_video(caminho_video):
    if not os.path.exists(caminho_video): return
    cap = cv2.VideoCapture(caminho_video)
    video_rodando = True
    while video_rodando:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame, 0)
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.scale(frame_surface, (WIDTH, HEIGHT))
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release();
                pygame.quit();
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                video_rodando = False
    cap.release()


def menu():
    button_rect = pygame.Rect((WIDTH // 2 - 110, HEIGHT // 2 + 100), (220, 60))
    button_font = pygame.font.Font(None, 50)
    while True:
        screen.blit(menubg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        color = GREEN if button_rect.collidepoint(mouse_pos) else (16, 209, 74)
        if button_rect.collidepoint(mouse_pos) and clicked:
            pygame.time.delay(200);
            return
        pygame.draw.rect(screen, color, button_rect, border_radius=12)
        text = button_font.render("JOGAR", True, DARK_GREEN)
        screen.blit(text, text.get_rect(center=button_rect.center))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()


def game_over_screen(venceu=False):
    global score, score2
    screen.blit(winimg if venceu else loseimg, (0, 0))
    msg = "Você venceu!" if venceu else "Você perdeu!"
    txt_main = font.render(msg, True, WHITE)
    txt_score = font.render(f"Maior pontuação: {max(score, score2)}", True, WHITE)
    screen.blit(txt_main, txt_main.get_rect(center=(WIDTH // 2, 500)))
    screen.blit(txt_score, txt_score.get_rect(center=(WIDTH // 2, 450)))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
        clock.tick(15)


def draw_hud():
    t1 = font.render(f"P1 Pontos: {score}   Vidas: {lives}", True, WHITE)
    t2 = font.render(f"P2 Pontos: {score2}   Vidas: {lives2}", True, WHITE)
    screen.blit(t1, (10, 10))
    screen.blit(t2, (WIDTH - t2.get_width() - 10, 10))


# ----------------------------------------------------------
# 🕹️ LOOP PRINCIPAL
# ----------------------------------------------------------
menu()

current_phase = 1

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # --- LÓGICA DE FIM DE JOGO ---
    if death and death2 and len(explosion_group) == 0:
        game_over_screen(venceu=False)
        break

    # --- CONTROLES ---
    keys = pygame.key.get_pressed()
    if not death:
        if keys[pygame.K_LEFT] and player_rect.left > 0: player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH: player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0: player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT: player_rect.y += player_speed
    if not death2:
        if keys[pygame.K_a] and player2_rect.left > 0: player2_rect.x -= player2_speed
        if keys[pygame.K_d] and player2_rect.right < WIDTH: player2_rect.x += player2_speed
        if keys[pygame.K_w] and player2_rect.top > 0: player2_rect.y -= player2_speed
        if keys[pygame.K_s] and player2_rect.bottom < HEIGHT: player2_rect.y += player2_speed

    # --- DEFINIÇÃO DA FASE ATUAL ---
    current_max = max(score, score2)
    if current_max >= 100:
        current_phase = 3
    elif current_max >= 50:
        current_phase = 2
    else:
        current_phase = 1

    # --- UPDATES (Passando a fase atual) ---
    for meteor in meteor_group:
        if meteor.update(current_phase):
            if not death: score += 1
            if not death2: score2 += 1
            if sound_point: sound_point.play()

    life_group.update()
    explosion_group.update()

    # --- COLISÕES ---
    for meteor in meteor_group:
        # Player 1
        if not death and meteor.rect.colliderect(player_rect):
            lives -= 1
            meteor.reset_position(current_phase)
            if sound_hit: sound_hit.play()
            if lives <= 0:
                death = True
                expl = Explosion(player_rect.center, explosion_frames)
                explosion_group.add(expl)
                if sound_explosion: sound_explosion.play()

        # Player 2
        if not death2 and meteor.rect.colliderect(player2_rect):
            lives2 -= 1
            meteor.reset_position(current_phase)
            if sound_hit: sound_hit.play()
            if lives2 <= 0:
                death2 = True
                expl = Explosion(player2_rect.center, explosion_frames)
                explosion_group.add(expl)
                if sound_explosion: sound_explosion.play()

    for bonus in life_group:
        if not death and bonus.rect.colliderect(player_rect):
            lives += 1;
            score += 5;
            bonus.reset_position()
            if sound_point: sound_point.play()
        if not death2 and bonus.rect.colliderect(player2_rect):
            lives2 += 1;
            score2 += 5;
            bonus.reset_position()
            if sound_point: sound_point.play()

    # --- TRANSIÇÕES DE FASE ---
    current_bg = background
    if current_max >= 150:
        game_over_screen(venceu=True)
        break
    elif current_max >= 100:
        if not video_fase2_3_rodou:
            reproduzir_video(ASSETS["transicaoFase2-3video"])
            video_fase2_3_rodou = True
        current_bg = background3
    elif current_max >= 50:
        if not video_fase1_2_rodou:
            reproduzir_video(ASSETS["transicaoFase1-2video"])
            video_fase1_2_rodou = True
        current_bg = background2

    # --- DESENHO ---
    screen.blit(current_bg, (0, 0))
    if not death: screen.blit(player_img, player_rect)
    if not death2: screen.blit(player2_img, player2_rect)
    meteor_group.draw(screen)
    life_group.draw(screen)
    explosion_group.draw(screen)
    draw_hud()
    pygame.display.flip()

pygame.quit()