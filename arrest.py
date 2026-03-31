import tkinter as tk
import math

root = tk.Tk()
root.title("Test")
root.geometry("900x500")
root.configure(bg="#2b2b2b")
root.resizable(False, False)

WIDTH = 900
HEIGHT = 500

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#2b2b2b", highlightthickness=0)
canvas.pack(fill="both", expand=True)

state = "menu"

# ---------------- MENU ----------------
for i in range(0, HEIGHT, 4):
    shade = 43 + int(i / HEIGHT * 20)
    color = f"#{shade:02x}{shade:02x}{shade:02x}"
    canvas.create_rectangle(0, i, WIDTH, i + 4, fill=color, outline=color)

shadow = canvas.create_text(454, 105, text="Test", font=("Arial Black", 64), fill="#111111")
main_title = canvas.create_text(450, 100, text="Test", font=("Arial Black", 64), fill="#ffffff")

splash = canvas.create_text(650, 85, text="hi", font=("Arial Black", 22), fill="#ffe400")

canvas.create_text(450, 185, text="Select a level", font=("Arial", 18, "bold"), fill="white")

# ---------------- GAME ----------------
ground_y = 380
player_x = 120
player_y = ground_y - 20
vel_y = 0
on_ground = True
rotation = 0

obstacles = [
    [600, "spike"],
    [900, "wall"],
    [1200, "spike"],
    [1450, "wall"],
    [1700, "spike"],
]

player_parts = []
game_objects = []
message_text = None


def start_level():
    global state, player_y, vel_y, on_ground, rotation

    state = "game"
    canvas.delete("all")

    # Background
    canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#4bc0ff", outline="")
    canvas.create_rectangle(0, ground_y, WIDTH, HEIGHT, fill="#3aa63a", outline="")

    player_y = ground_y - 40
    vel_y = 0
    on_ground = True
    rotation = 0

    obstacles.clear()
    obstacles.extend([
        [600, "spike"],
        [900, "wall"],
        [1200, "spike"],
        [1450, "wall"],
        [1700, "spike"],
        [2000, "wall"],
    ])

    update_game()


def draw_player():
    global player_parts

    for p in player_parts:
        canvas.delete(p)
    player_parts.clear()

    cx = player_x
    cy = player_y
    size = 20

    corners = [(-size, -size), (size, -size), (size, size), (-size, size)]
    pts = []

    rad = math.radians(rotation)
    for x, y in corners:
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        pts.extend([cx + rx, cy + ry])

    player_parts.append(canvas.create_polygon(pts, fill="#ff3c3c", outline="white", width=2))


def jump(event=None):
    global vel_y, on_ground
    if state == "game" and on_ground:
        vel_y = -11
        on_ground = False


def game_over():
    global state, message_text
    state = "dead"
    message_text = canvas.create_text(
        WIDTH / 2,
        150,
        text="You Crashed! Press R or ESC",
        font=("Arial Black", 28),
        fill="white"
    )


def restart(event=None):
    if state == "dead":
        start_level()


def update_game():
    global player_y, vel_y, on_ground, rotation

    if state != "game":
        return

    canvas.delete("obstacle")

    vel_y += 0.55
    player_y += vel_y

    if not on_ground:
        rotation += 12

    if player_y >= ground_y - 20:
        player_y = ground_y - 20
        vel_y = 0
        on_ground = True
        rotation = (round(rotation / 90) * 90) % 360

    draw_player()

    player_left = player_x - 20
    player_right = player_x + 20
    player_top = player_y - 20
    player_bottom = player_y + 20

    for obstacle in obstacles:
        obstacle[0] -= 6
        x = obstacle[0]

        if obstacle[1] == "spike":
            canvas.create_polygon(
                x, ground_y,
                x + 20, ground_y - 40,
                x + 40, ground_y,
                fill="#222222",
                outline="white",
                tags="obstacle"
            )

            if player_right > x and player_left < x + 40 and player_bottom > ground_y - 40:
                game_over()
                return

        elif obstacle[1] == "wall":
            canvas.create_rectangle(
                x,
                ground_y - 80,
                x + 35,
                ground_y,
                fill="#444444",
                outline="white",
                tags="obstacle"
            )

            if player_right > x and player_left < x + 35 and player_bottom > ground_y - 80:
                game_over()
                return

    if obstacles and obstacles[-1][0] < WIDTH:
        pass

    root.after(16, update_game)


level_btn = tk.Button(
    root,
    text="Levels",
    font=("Arial", 16, "bold"),
    bg="#7a7a7a",
    fg="white",
    activebackground="#9a9a9a",
    activeforeground="white",
    relief="raised",
    bd=4,
    width=24,
    command=start_level
)

canvas.create_window(450, 250, window=level_btn)

canvas.create_text(450, 310, text="Level 1: Test", font=("Arial", 16, "bold"), fill="white")

angle = 0


def animate_menu():
    global angle
    if state == "menu":
        angle += 0.08
        scale = 1 + math.sin(angle) * 0.12
        size = int(22 * scale)
        offset = math.sin(angle) * 10
        canvas.itemconfig(splash, font=("Arial Black", max(size, 1)))
        canvas.coords(splash, 650, 85 + offset)

    root.after(16, animate_menu)


def back_to_menu(event=None):
    global state
    state = "menu"
    canvas.delete("all")

    for i in range(0, HEIGHT, 4):
        shade = 43 + int(i / HEIGHT * 20)
        color = f"#{shade:02x}{shade:02x}{shade:02x}"
        canvas.create_rectangle(0, i, WIDTH, i + 4, fill=color, outline=color)

    canvas.create_text(454, 105, text="Test", font=("Arial Black", 64), fill="#111111")
    canvas.create_text(450, 100, text="Test", font=("Arial Black", 64), fill="#ffffff")

    global splash
    splash = canvas.create_text(650, 85, text="hi", font=("Arial Black", 22), fill="#ffe400")

    canvas.create_text(450, 185, text="Select a level", font=("Arial", 18, "bold"), fill="white")
    canvas.create_window(450, 250, window=level_btn)
    canvas.create_text(450, 310, text="Level 1: Test", font=("Arial", 16, "bold"), fill="white")

root.bind("<space>", jump)
root.bind("<Button-1>", jump)
root.bind("r", restart)
root.bind("<Escape>", back_to_menu)

animate_menu()
root.mainloop()
