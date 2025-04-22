import tkinter as tk
import time

class ShakyBallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shake the Cup!")
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()

        self.ball = self.canvas.create_oval(180, 180, 220, 220, fill="red")
        self.ball_radius = 20
        self.ball_pos = [200, 200]
        self.ball_vel = [0, 0]

        self.gravity = 0.3
        self.friction = 0.99
        self.bounce = -0.7

        self.shake_force = [0, 0]

        self.last_time = time.time()
        self.last_shake_check = time.time()

        self.root.after(200, self.start_tracking)

    def start_tracking(self):
        self.prev_root_x = self.root.winfo_x()
        self.prev_root_y = self.root.winfo_y()
        self.update()

    def update(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # Get window movement delta
        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()
        dx = current_x - self.prev_root_x
        dy = current_y - self.prev_root_y
        self.prev_root_x = current_x
        self.prev_root_y = current_y

        # Window velocity = acceleration applied to ball (reverse direction to simulate inertia)
        self.shake_force[0] = -dx * 0.5
        self.shake_force[1] = -dy * 0.5

        # Apply "inertia" from window movement
        self.ball_vel[0] += self.shake_force[0]
        self.ball_vel[1] += self.shake_force[1]

        # Gravity
        self.ball_vel[1] += self.gravity

        # Update ball position
        self.ball_pos[0] += self.ball_vel[0] * dt * 60
        self.ball_pos[1] += self.ball_vel[1] * dt * 60

        # Bounce off walls
        width = 400
        height = 400
        r = self.ball_radius

        if self.ball_pos[0] - r < 0:
            self.ball_pos[0] = r
            self.ball_vel[0] *= self.bounce
        elif self.ball_pos[0] + r > width:
            self.ball_pos[0] = width - r
            self.ball_vel[0] *= self.bounce

        if self.ball_pos[1] - r < 0:
            self.ball_pos[1] = r
            self.ball_vel[1] *= self.bounce
        elif self.ball_pos[1] + r > height:
            self.ball_pos[1] = height - r
            self.ball_vel[1] *= self.bounce

        # Friction
        self.ball_vel[0] *= self.friction
        self.ball_vel[1] *= self.friction

        # Draw
        x, y = self.ball_pos
        self.canvas.coords(self.ball, x - r, y - r, x + r, y + r)

        self.root.after(16, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = ShakyBallApp(root)
    root.mainloop()
