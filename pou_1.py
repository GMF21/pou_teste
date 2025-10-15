import pygame
import sys
import os
import json
import random

# ------------------- Configurações -------------------
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pou Completo em Pygame")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
SKY = (150, 220, 255)
DARK = (50, 50, 50)

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()
FPS = 60

SAVE_FILE = "pou_save.json"

# ------------------- Estado do Pou -------------------
# Valores de status: 0 a 100
status = {
    "hunger": 100,
    "clean": 100,
    "sleep": 100,
    "happy": 100
}

# Visual (trocar cor, chapéu, óculos, etc)
visual = {
    "color": BROWN,
    "hat": None,
    "glasses": None
}

# Estado de animações / transições
anim = {
    "feeding": False,
    "cleaning": False,
    "sleeping": False,
    "sleep_anim_progress": 0,
}

# Diretório de recursos (se quiser depois usar imagens externas)
RESOURCE_DIR = "resources"
if not os.path.exists(RESOURCE_DIR):
    os.makedirs(RESOURCE_DIR)

# ------------------- Funções de salvar / carregar -------------------
def save_game():
    data = {
        "status": status,
        "visual": visual
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    global status, visual
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            status = data.get("status", status)
            visual = data.get("visual", visual)

# ------------------- Botões úteis -------------------
class Button:
    def __init__(self, rect, label, color_bg=LIGHT_GRAY, color_fg=BLACK):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.color_bg = color_bg
        self.color_fg = color_fg

    def draw(self, surf):
        pygame.draw.rect(surf, self.color_bg, self.rect)
        pygame.draw.rect(surf, BLACK, self.rect, 2)
        txt = big_font.render(self.label, True, self.color_fg)
        txt_rect = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Cria botões
btn_feed = Button((50, 500, 150, 50), "Alimentar")
btn_clean = Button((250, 500, 150, 50), "Banho")
btn_sleep = Button((450, 500, 150, 50), "Dormir")
btn_fun = Button((650, 500, 120, 50), "Brincar")
btn_save = Button((650, 20, 120, 40), "Salvar")

# ------------------- Funções de desenho -------------------
def draw_pou(x, y):
    # Corpo oval
    pygame.draw.ellipse(screen, visual["color"], (x - 80, y - 120, 160, 200))
    # Olhos
    eye_y = y - 60
    pygame.draw.circle(screen, WHITE, (x - 30, eye_y), 15)
    pygame.draw.circle(screen, WHITE, (x + 30, eye_y), 15)
    pygame.draw.circle(screen, BLACK, (x - 30, eye_y), 7)
    pygame.draw.circle(screen, BLACK, (x + 30, eye_y), 7)
    # Boca: comportamento conforme felicidade/sleep
    mouth_rect = pygame.Rect(x - 30, y - 10, 60, 30)
    if anim["sleeping"]:
        # boca neutra quando dormindo
        pygame.draw.line(screen, BLACK, (x - 20, y), (x + 20, y), 3)
    else:
        # boca sorrindo ou triste conforme status["happy"]
        if status["happy"] >= 60:
            pygame.draw.arc(screen, BLACK, mouth_rect, 3.14, 0, 3)
        else:
            pygame.draw.arc(screen, BLACK, mouth_rect, 0, 3.14, 3)
    # Itens visuais (chapéu, óculos) – aqui só desenhamos como formas simples
    if visual["hat"]:
        pygame.draw.rect(screen, visual["hat"], (x - 50, y - 140, 100, 30))
    if visual["glasses"]:
        # desenha dois retângulos conectados
        pygame.draw.rect(screen, visual["glasses"], (x - 45, eye_y - 5, 30, 10))
        pygame.draw.rect(screen, visual["glasses"], (x + 15, eye_y - 5, 30, 10))
        pygame.draw.line(screen, visual["glasses"], (x - 15, eye_y), (x + 15, eye_y), 3)

def draw_status_bar(x, y, value, label, color):
    # fundo
    pygame.draw.rect(screen, GRAY, (x, y, 200, 20))
    # valor
    filled = int(200 * (value / 100))
    pygame.draw.rect(screen, color, (x, y, filled, 20))
    # texto
    txt = font.render(f"{label}: {int(value)}%", True, BLACK)
    screen.blit(txt, (x, y - 25))

# ------------------- Minigame simples (cena de “pegar maçã”) -------------------
class MiniGame:
    def __init__(self):
        self.active = False
        self.apples = []
        self.timer = 0
        self.duration = 5 * FPS  # 5 segundos

    def start(self):
        self.active = True
        self.timer = 0
        self.apples.clear()
        # criar algumas maçãs caindo
        for i in range(5):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(-300, -50)
            speed = random.uniform(2, 5)
            self.apples.append({"x": x, "y": y, "speed": speed})

    def update(self):
        if not self.active:
            return
        self.timer += 1
        for apple in self.apples:
            apple["y"] += apple["speed"]
        # remover maçãs que saíram da tela
        self.apples = [a for a in self.apples if a["y"] < HEIGHT + 20]
        if self.timer > self.duration:
            # final do minigame
            self.active = False
            # recompensa: felicidade + alimentação leve
            status["happy"] = min(100, status["happy"] + 20)
            status["hunger"] = min(100, status["hunger"] + 5)

    def draw(self):
        for apple in self.apples:
            pygame.draw.circle(screen, RED, (int(apple["x"]), int(apple["y"])), 15)

    def click(self, pos):
        if not self.active:
            return
        for apple in self.apples:
            dx = pos[0] - apple["x"]
            dy = pos[1] - apple["y"]
            if dx * dx + dy * dy < 15 * 15:
                # “coletou” maçã
                status["happy"] = min(100, status["happy"] + 5)
                status["hunger"] = min(100, status["hunger"] + 2)
                # mover maçã para fora
                apple["y"] = HEIGHT + 100

minigame = MiniGame()

# ------------------- Função principal / loop -------------------
def main_loop():
    load_game()
    pou_x, pou_y = WIDTH // 2, HEIGHT // 2 + 20

    running = True
    while running:
        dt = clock.tick(FPS)
        screen.fill(SKY)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if btn_feed.is_clicked(pos):
                    # alimentar
                    anim["feeding"] = True
                    status["hunger"] = min(100, status["hunger"] + 25)
                elif btn_clean.is_clicked(pos):
                    anim["cleaning"] = True
                    status["clean"] = min(100, status["clean"] + 30)
                elif btn_sleep.is_clicked(pos):
                    anim["sleeping"] = True
                    anim["sleep_anim_progress"] = 0
                elif btn_fun.is_clicked(pos):
                    if not minigame.active:
                        minigame.start()
                elif btn_save.is_clicked(pos):
                    save_game()

                # se estiver no minigame, clique nas maçãs
                if minigame.active:
                    minigame.click(pos)

        # Atualização de status com decaimento
        # Se estiver dormindo, status decaem mais devagar ou pausam
        if anim["sleeping"]:
            # enquanto dorme, recarrega sono
            anim["sleep_anim_progress"] += 1
            status["sleep"] = min(100, status["sleep"] + 0.25)
            if anim["sleep_anim_progress"] >= 4 * FPS:
                # acorda após 4 segundos
                anim["sleeping"] = False
        else:
            status["hunger"] -= 0.02
            status["clean"] -= 0.015
            status["sleep"] -= 0.01
            status["happy"] -= 0.02

        # limitar entre 0 e 100
        for k in status:
            if status[k] < 0:
                status[k] = 0
            if status[k] > 100:
                status[k] = 100

        # Se fome ou limpeza muito baixa, felicidade cai mais
        if status["hunger"] < 20 or status["clean"] < 20:
            status["happy"] -= 0.05

        # Animações temporárias (por exemplo, alimentar / limpar)
        # Podemos exibir algo por tempo curto
        if anim["feeding"]:
            # desenha comida próximo ao Pou
            food_rect = pygame.Rect(pou_x + 60, pou_y + 40, 30, 30)
            pygame.draw.rect(screen, YELLOW, food_rect)
            # pausar animação depois de um tempo
            # podemos usar contador simples: usar anim["feeding"] como tempo restante
            anim["feeding"] = False

        if anim["cleaning"]:
            # efeito de água (círculos transparentes)
            pygame.draw.circle(screen, BLUE, (pou_x, pou_y + 80), 60, 5)
            anim["cleaning"] = False

        # Desenhar Pou
        draw_pou(pou_x, pou_y)
        # Desenhar barras de status
        draw_status_bar(50, 30, status["hunger"], "Fome", GREEN)
        draw_status_bar(50, 80, status["clean"], "Limpeza", BLUE)
        draw_status_bar(50, 130, status["sleep"], "Sono", YELLOW)
        draw_status_bar(50, 180, status["happy"], "Felicidade", RED)

        # Desenhar botões
        btn_feed.draw(screen)
        btn_clean.draw(screen)
        btn_sleep.draw(screen)
        btn_fun.draw(screen)
        btn_save.draw(screen)

        # Se minigame ativo, desenhar
        if minigame.active:
            minigame.update()
            minigame.draw()

        # Aviso se status críticos
        if status["hunger"] <= 0:
            txt = big_font.render("Estou com muita fome!", True, RED)
            screen.blit(txt, (200, 10))
        if status["clean"] <= 0:
            txt = big_font.render("Preciso de um banho!", True, BLUE)
            screen.blit(txt, (200, 50))
        if status["sleep"] <= 0:
            txt = big_font.render("Estou exausto!", True, YELLOW)
            screen.blit(txt, (200, 90))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()
