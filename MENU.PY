import pygame
import sys

# Inicialização
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pou - Menu")
background_menu = pygame.image.load("/home/gmferreira/Documentos/python/d7hftxdivxxvm.cloudfront.webp")
background_menu = pygame.transform.scale(background_menu, (WIDTH, HEIGHT))

# Cores
WHITE = (255, 255, 255)
LIGHT_BLUE = (230, 240, 255)
BLACK = (0, 0, 0)
BUTTON_BG = (240, 245, 255)
BUTTON_BORDER = (100, 100, 100)

# Fontes
TITLE_FONT = pygame.font.SysFont("comicsansms", 36, bold=True)
BUTTON_FONT = pygame.font.SysFont("comicsansms", 28, bold=True)

clock = pygame.time.Clock()
FPS = 60

# Classe de botão
class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surf):
        pygame.draw.rect(surf, BUTTON_BG, self.rect)
        pygame.draw.rect(surf, BUTTON_BORDER, self.rect, 2)
        txt = BUTTON_FONT.render(self.text, True, BLACK)
        txt_rect = txt.get_rect(center=self.rect.center)
        surf.blit(txt, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Criar botões
buttons = [
    Button((WIDTH//2 - 150, 120, 300, 50), "Create Game"),
    Button((WIDTH//2 - 150, 190, 300, 50), "Join Game"),
]

# Loop do menu
def menu_loop():
    running = True
    while running:
        screen.fill(LIGHT_BLUE)

        # Título
        title = TITLE_FONT.render("Pou", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 40))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if buttons[0].is_clicked(pos):
                    print("Create Game clicked")
                elif buttons[1].is_clicked(pos):
                    print("Join Game clicked")

        # Desenhar botões
        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Iniciar menu
if __name__ == "__main__":
    menu_loop()
