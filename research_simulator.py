import tkinter as tk
import random
import math
import time

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1000, 800
ROBOT_COUNT = 3
TASK_COUNT = 5
ROBOT_SPEED = 3
COLORS = {
    "background": "#14141e",
    "robot": "#00c8ff",
    "task": "#ff6400",
    "assigned": "#64ff64",
    "text": "#f0f0f0",
    "path": "#323246"
}

class Task:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.assigned_to = None
        self.completed = False
        self.canvas_id = None
        self.text_id = None

class Robot:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.target_task = None
        self.tasks_completed = 0
        self.status = "Idle"
        self.canvas_id = None
        self.text_id = None
        self.line_id = None

    def move_towards(self, tx, ty):
        dx = tx - self.x
        dy = ty - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist > ROBOT_SPEED:
            self.x += (dx / dist) * ROBOT_SPEED
            self.y += (dy / dist) * ROBOT_SPEED
            return False
        else:
            self.x = tx
            self.y = ty
            return True

class ResearchSim:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Multi-Robot Coordination Research Simulator (Zero-Dependency)")
        self.root.configure(bg=COLORS["background"])
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=COLORS["background"], highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        
        self.robots = [Robot(i+1, random.randint(100, 900), random.randint(100, 700)) for i in range(ROBOT_COUNT)]
        self.tasks = [Task(i+1, random.randint(50, 950), random.randint(50, 750)) for i in range(TASK_COUNT)]
        
        self.setup_ui()
        self.update()
        self.root.mainloop()

    def setup_ui(self):
        self.title_label = self.canvas.create_text(20, 30, text="Multi-Robot Coordination System (Auction-Based)", 
                                                 fill="white", font=("Arial", 20, "bold"), anchor="nw")
        self.stats_ids = []
        for i in range(ROBOT_COUNT):
            s_id = self.canvas.create_text(20, 70 + i*25, text="", fill=COLORS["robot"], font=("Arial", 12), anchor="nw")
            self.stats_ids.append(s_id)

    def allocate(self):
        for task in self.tasks:
            if task.assigned_to is None and not task.completed:
                best_bid = float('inf')
                best_robot = None
                
                for robot in self.robots:
                    if robot.target_task is None:
                        dist = math.sqrt((robot.x - task.x)**2 + (robot.y - task.y)**2)
                        if dist < best_bid:
                            best_bid = dist
                            best_robot = robot
                
                if best_robot:
                    task.assigned_to = best_robot.id
                    best_robot.target_task = task
                    best_robot.status = f"Executing Task {task.id}"

    def update(self):
        self.allocate()
        
        # Update Robots
        for robot in self.robots:
            if robot.target_task:
                arrived = robot.move_towards(robot.target_task.x, robot.target_task.y)
                if arrived:
                    robot.target_task.completed = True
                    # Remove task visuals
                    self.canvas.delete(robot.target_task.canvas_id)
                    self.canvas.delete(robot.target_task.text_id)
                    
                    robot.target_task = None
                    robot.tasks_completed += 1
                    robot.status = "Idle"
                    
                    # New Task
                    new_id = len(self.tasks) + 1
                    nt = Task(new_id, random.randint(50, 950), random.randint(50, 750))
                    self.tasks.append(nt)

        # Redraw everything
        self.draw()
        self.root.after(20, self.update)

    def draw(self):
        # Draw Tasks
        for task in self.tasks:
            if not task.completed:
                color = COLORS["assigned"] if task.assigned_to else COLORS["task"]
                if task.canvas_id:
                    self.canvas.coords(task.canvas_id, task.x-6, task.y-6, task.x+6, task.y+6)
                    self.canvas.itemconfig(task.canvas_id, fill=color)
                    self.canvas.coords(task.text_id, task.x+10, task.y-10)
                else:
                    task.canvas_id = self.canvas.create_oval(task.x-6, task.y-6, task.x+6, task.y+6, fill=color, outline="")
                    task.text_id = self.canvas.create_text(task.x+10, task.y-10, text=f"T{task.id}", fill=COLORS["text"], font=("Arial", 10))

        # Draw Robots
        for i, robot in enumerate(self.robots):
            # Path line
            if robot.target_task:
                if robot.line_id:
                    self.canvas.coords(robot.line_id, robot.x, robot.y, robot.target_task.x, robot.target_task.y)
                else:
                    robot.line_id = self.canvas.create_line(robot.x, robot.y, robot.target_task.x, robot.target_task.y, fill=COLORS["path"], dash=(4, 4))
            elif robot.line_id:
                self.canvas.delete(robot.line_id)
                robot.line_id = None

            # Robot body
            if robot.canvas_id:
                self.canvas.coords(robot.canvas_id, robot.x-12, robot.y-12, robot.x+12, robot.y+12)
                self.canvas.coords(robot.text_id, robot.x, robot.y+25)
                self.canvas.itemconfig(robot.text_id, text=f"Robot {robot.id}\n({robot.status})")
            else:
                robot.canvas_id = self.canvas.create_rectangle(robot.x-12, robot.y-12, robot.x+12, robot.y+12, outline=COLORS["robot"], width=2)
                robot.text_id = self.canvas.create_text(robot.x, robot.y+25, text="", fill=COLORS["text"], font=("Arial", 9), justify="center")

            # Update stats
            self.canvas.itemconfig(self.stats_ids[i], text=f"Robot {robot.id}: {robot.tasks_completed} tasks completed")

if __name__ == "__main__":
    ResearchSim()
