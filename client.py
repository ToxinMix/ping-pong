from pygame import *
import socket
import json
import os
from threading import Thread

# =====================================================
# ІНІЦІАЛІЗАЦІЯ
# =====================================================

WIDTH = 800
HEIGHT = 600
FPS = 60

init()
mixer.init()

screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Пінг-Понг Deluxe")
clock = time.Clock()

# =====================================================
# ФОН (ТОЛЬКО background.png)
# =====================================================

background = image.load("images/background.png")
background = transform.scale(background, (WIDTH, HEIGHT))


def draw_background():
    screen.blit(background, (0, 0))

# =====================================================
# КОЛЬОРИ
# =====================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
GRAY = (60, 60, 60)

# =====================================================
# ШРИФТИ
# =====================================================

font_small = font.Font(None, 28)
font_main = font.Font(None, 36)
font_big = font.Font(None, 60)
font_win = font.Font(None, 80)

# =====================================================
# JSON SETTINGS
# =====================================================

SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        data = {
            "player_name": "Player",
            "ball_skin": "default",
            "paddle_skin": "default"
        }
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return data

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

settings = load_settings()

# =====================================================
# ЗОБРАЖЕННЯ СКІНІВ
# =====================================================

ball_skins = {
    "default": transform.scale(image.load("images/ball_default.png"), (26, 26)),
    "fire": transform.scale(image.load("images/ball_fire.png"), (26, 26)),
    "ice": transform.scale(image.load("images/ball_ice.png"), (26, 26))
}

paddle_skins = {
    "default": transform.scale(image.load("images/paddle_default.png"), (20, 100)),
    "gold": transform.scale(image.load("images/paddle_gold.png"), (20, 100))
}

button_img = transform.scale(image.load("images/button.png"), (220, 60))

# =====================================================
# ЗВУКИ
# =====================================================

def load_sound(path):
    try:
        return mixer.Sound(path)
    except:
        return None

click_sound = load_sound("sounds/click.wav")
wall_sound = load_sound("sounds/wall_hit.wav")
platform_sound = load_sound("sounds/platform_hit.wav")

# =====================================================
# КНОПКА
# =====================================================

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = Rect(x, y, w, h)
        self.text = text

    def draw(self):
        screen.blit(transform.scale(button_img, (self.rect.w, self.rect.h)), self.rect)

        txt = font_main.render(self.text, True, WHITE)
        screen.blit(txt, (
            self.rect.centerx - txt.get_width() // 2,
            self.rect.centery - txt.get_height() // 2
        ))

    def is_clicked(self, e):
        return e.type == MOUSEBUTTONDOWN and self.rect.collidepoint(e.pos)

# =====================================================
# ВВЕДЕННЯ ІМЕНІ
# =====================================================

def name_input_screen():
    name = settings["player_name"]
    running = True

    while running:
        draw_background()

        title = font_big.render("Введіть ім'я", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        box = Rect(250, 250, 300, 60)
        draw.rect(screen, WHITE, box, 2)

        txt = font_main.render(name, True, WHITE)
        screen.blit(txt, (box.x + 10, box.y + 15))

        hint = font_small.render("ENTER - продовжити", True, WHITE)
        screen.blit(hint, (260, 340))

        for e in event.get():
            if e.type == QUIT:
                quit()

            if e.type == KEYDOWN:
                if e.key == K_RETURN:
                    settings["player_name"] = name
                    save_settings(settings)
                    running = False

                elif e.key == K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 16:
                        name += e.unicode

        display.update()
        clock.tick(FPS)

# =====================================================
# МАГАЗИН
# =====================================================

def shop_menu():

    fire = Button(250, 170, 300, 50, "М'яч Вогонь")
    ice = Button(250, 240, 300, 50, "М'яч Лід")
    gold = Button(250, 310, 300, 50, "Золота платформа")
    back = Button(250, 420, 300, 50, "Назад")

    running = True

    while running:
        draw_background()

        title = font_big.render("МАГАЗИН", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        fire.draw()
        ice.draw()
        gold.draw()
        back.draw()

        for e in event.get():
            if e.type == QUIT:
                quit()

            if fire.is_clicked(e):
                settings["ball_skin"] = "fire"
                save_settings(settings)
                if click_sound: click_sound.play()

            if ice.is_clicked(e):
                settings["ball_skin"] = "ice"
                save_settings(settings)
                if click_sound: click_sound.play()

            if gold.is_clicked(e):
                settings["paddle_skin"] = "gold"
                save_settings(settings)
                if click_sound: click_sound.play()

            if back.is_clicked(e):
                running = False

        display.update()
        clock.tick(FPS)

# =====================================================
# ГОЛОВНЕ МЕНЮ
# =====================================================

def main_menu():

    play = Button(290, 220, 220, 60, "Грати")
    shop = Button(290, 300, 220, 60, "Магазин")
    exit_btn = Button(290, 380, 220, 60, "Вихід")

    while True:
        draw_background()

        title = font_win.render("PING PONG", True, GOLD)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        name = font_main.render(settings["player_name"], True, WHITE)
        screen.blit(name, (WIDTH//2 - name.get_width()//2, 180))

        play.draw()
        shop.draw()
        exit_btn.draw()

        for e in event.get():
            if e.type == QUIT:
                quit()

            if play.is_clicked(e):
                if click_sound: click_sound.play()
                return

            if shop.is_clicked(e):
                if click_sound: click_sound.play()
                shop_menu()

            if exit_btn.is_clicked(e):
                quit()

        display.update()
        clock.tick(FPS)

# =====================================================
# ПЕРЕД ГРОЮ
# =====================================================

name_input_screen()
main_menu()
# =====================================================
# ПІДКЛЮЧЕННЯ ДО СЕРВЕРА
# =====================================================

def connect_to_server():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 8080))

            buffer = ""
            game_state = {}

            my_id = int(client.recv(64).decode().strip())

            return my_id, game_state, buffer, client

        except:
            draw_background()

            txt = font_big.render("Очікування сервера...", True, WHITE)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

            display.update()

            for e in event.get():
                if e.type == QUIT:
                    quit()

# =====================================================
# ОТРИМАННЯ ДАНИХ
# =====================================================

def receive():
    global buffer, game_state, game_over, client

    while not game_over:
        try:
            data = client.recv(1024).decode()
            buffer += data

            while "\n" in buffer:
                packet, buffer = buffer.split("\n", 1)

                if packet.strip():
                    game_state = json.loads(packet)

        except:
            game_state["winner"] = -1
            break

# =====================================================
# ІНІЦІАЛІЗАЦІЯ ГРИ
# =====================================================

game_over = False
winner = None
you_won = None

my_id, game_state, buffer, client = connect_to_server()

Thread(target=receive, daemon=True).start()

particles = []

# =====================================================
# ГОЛОВНИЙ ІГРОВИЙ ЦИКЛ
# =====================================================

while True:

    for e in event.get():
        if e.type == QUIT:
            quit()

    draw_background()

    # =================================================
    # ВІДЛІК
    # =================================================

    if "countdown" in game_state and game_state["countdown"] > 0:

        txt = font_win.render(str(game_state["countdown"]), True, WHITE)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

        display.update()
        continue

    # =================================================
    # ПЕРЕМОГА
    # =================================================

    if "winner" in game_state and game_state["winner"] is not None:

        if you_won is None:
            you_won = (game_state["winner"] == my_id)

        text = "Ти переміг!" if you_won else "Ти програв!"

        win = font_win.render(text, True, GOLD)
        screen.blit(win, (WIDTH//2 - win.get_width()//2, HEIGHT//2))

        display.update()
        continue

    # =================================================
    # ГРА
    # =================================================

    if game_state:

        # ПЛАТФОРМИ
        left_y = int(game_state["paddles"]["0"])
        right_y = int(game_state["paddles"]["1"])

        screen.blit(
            paddle_skins[settings["paddle_skin"]],
            (20, left_y)
        )

        screen.blit(
            paddle_skins[settings["paddle_skin"]],
            (WIDTH - 40, right_y)
        )

        # М'ЯЧ
        ball_x = int(game_state["ball"]["x"])
        ball_y = int(game_state["ball"]["y"])

        screen.blit(
            ball_skins[settings["ball_skin"]],
            (ball_x - 13, ball_y - 13)
        )

        # =================================================
        # СКОР
        # =================================================

        score = font_big.render(
            f"{game_state['scores'][0]} : {game_state['scores'][1]}",
            True,
            WHITE
        )

        screen.blit(score, (WIDTH//2 - score.get_width()//2, 20))

        # =================================================
        # ЗВУКИ + ЕФЕКТИ
        # =================================================

        if game_state.get("sound_event"):

            if game_state["sound_event"] == "wall_hit":
                if wall_sound:
                    wall_sound.play()

            if game_state["sound_event"] == "platform_hit":
                if platform_sound:
                    platform_sound.play()

                # частинки
                for i in range(8):
                    particles.append([ball_x, ball_y, 4 + i % 3])

        # =================================================
        # ЧАСТИНКИ
        # =================================================

        for p in particles[:]:

            draw.circle(screen, GOLD, (p[0], p[1]), p[2])
            p[2] -= 0.2

            if p[2] <= 0:
                particles.remove(p)

        # =================================================
        # ІМ'Я ГРАВЦЯ
        # =================================================

        name = font_small.render(settings["player_name"], True, WHITE)
        screen.blit(name, (20, 20))

    else:

        txt = font_big.render("Очікування гравців...", True, WHITE)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2))

    display.update()
    clock.tick(FPS)

    # =================================================
    # КЕРУВАННЯ
    # =================================================

    keys = key.get_pressed()

    try:
        if keys[K_w]:
            client.send(b"UP")

        elif keys[K_s]:
            client.send(b"DOWN")

    except:
        pass