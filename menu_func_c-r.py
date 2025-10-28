import pygame
import sys
import json

class Menu:
    def __init__(self, width=1920, height=1080, background_path=None):
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("My GoodBoy")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BUTTON_BG = (240, 245, 255)
        self.BUTTON_BORDER = (100, 100, 100)
        self.EXIT_BUTTON_BG = (200, 0, 0)
        self.TITLE_COLOR = (50, 50, 50)
        self.TITLE_SHADOW = (100, 100, 100)

        # Fonts
        self.TITLE_FONT = pygame.font.SysFont("bitstreamverasans", 70, bold=True)
        self.BUTTON_FONT = pygame.font.SysFont("bitstreamverasans", 40, bold=True)
        self.NOTIFY_FONT = pygame.font.SysFont("bitstreamverasans", 35, bold=True)

        # Background
        if background_path:
            self.background = pygame.image.load(background_path)
            self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        else:
            self.background = None

        # Clock
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Game state
        self.game_status = {}
        self.notification = ""  # Mensagem para mostrar na tela

        # Buttons
        self.buttons = []
        self.create_buttons()

    class Button:
        def __init__(self, rect, text, bg_color):
            self.rect = pygame.Rect(rect)
            self.text = text
            self.bg_color = bg_color

        def draw(self, surf, font, border_color):
            mouse_pos = pygame.mouse.get_pos()
            is_hover = self.rect.collidepoint(mouse_pos)
            color = tuple(max(0, c - 30) for c in self.bg_color) if is_hover else self.bg_color
            pygame.draw.rect(surf, color, self.rect, border_radius=30)
            pygame.draw.rect(surf, border_color, self.rect, 3, border_radius=30)
            txt = font.render(self.text, True, (0, 0, 0))
            txt_rect = txt.get_rect(center=self.rect.center)
            surf.blit(txt, txt_rect)

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)

    def create_buttons(self):
        button_width = 400
        button_height = 80
        center_x = self.WIDTH // 2 - button_width // 2
        start_y = 500
        spacing = 150

        self.buttons.append(self.Button((center_x, start_y, button_width, button_height), "Create Game", self.BUTTON_BG))
        self.buttons.append(self.Button((center_x, start_y + spacing, button_width, button_height), "Join Game", self.BUTTON_BG))
        self.buttons.append(self.Button((center_x, start_y + 2 * spacing, button_width, button_height), "Exit", self.EXIT_BUTTON_BG))

    def reset_game(self):
        """Reseta todos os estados do jogo com valores default."""
        self.game_status = {
            "hunger": 100,
            "happiness": 100,
            "cleanliness": 100,
            "energy": 100,
            "coins": 0,
            "is_sleeping": False,
            "state": "idle",
            "current_skin": "Toni",
            "owned_skins": ["Toni", "Alex"]
        }
        self.notification = "Game Reset!"
        print("Game reset:", self.game_status)

    def load_game(self, filepath="save_pou.json"):
        """Carrega o estado do jogo de 'save_pou.json'."""
        try:
            with open(filepath, "r") as f:
                self.game_status = json.load(f)
            self.notification = "Game Loaded!"
            print("Game loaded:", self.game_status)
        except FileNotFoundError:
            self.notification = "Save file not found!"
            print(f"File {filepath} not found!")
        except json.JSONDecodeError:
            self.notification = "Error decoding JSON!"
            print("Error decoding JSON file!")

    def draw_notification(self):
        if self.notification:
            txt = self.NOTIFY_FONT.render(self.notification, True, (0, 100, 0))
            txt_rect = txt.get_rect(center=(self.WIDTH // 2, 400))
            self.screen.blit(txt, txt_rect)

    def run(self):
        running = True
        while running:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill(self.WHITE)

            # Title with shadow
            title_text = "My GoodBoy"
            title_render = self.TITLE_FONT.render(title_text, True, self.TITLE_COLOR)
            title_shadow = self.TITLE_FONT.render(title_text, True, self.TITLE_SHADOW)
            x = self.WIDTH // 2 - title_render.get_width() // 2
            y = 200
            self.screen.blit(title_shadow, (x + 4, y + 4))
            self.screen.blit(title_render, (x, y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.buttons[0].is_clicked(pos):
                        self.reset_game()
                    elif self.buttons[1].is_clicked(pos):
                        self.load_game()
                    elif self.buttons[2].is_clicked(pos):
                        running = False

            # Draw buttons
            for btn in self.buttons:
                btn.draw(self.screen, self.BUTTON_FONT, self.BUTTON_BORDER)

            # Draw notification
            self.draw_notification()

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    menu = Menu(background_path=r"/home/gmferreira/Documentos/pou_trb/Pou-Game/plain-blue-background-p99tt1vxhja81wp4.jpg")
    menu.run()
