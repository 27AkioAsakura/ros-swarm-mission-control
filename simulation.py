import math
import random
import time
import asyncio
from typing import List, Dict, Optional

class Task:
    def __init__(self, id: int, x: float, y: float, priority: int = 1):
        self.id = id
        self.x = x
        self.y = y
        self.priority = priority
        self.assigned_to: Optional[int] = None
        self.status = "Pending"  # Pending, Assigned, Executing, Completed
        self.created_at = time.time()

class Robot:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y
        self.target_task: Optional[Task] = None
        self.energy = 100.0
        self.workload = 0
        self.status = "Idle"
        self.speed = 5.0
        self.is_active = True # New: Support for failure simulation

    def calculate_bid(self, task: Task) -> float:
        if not self.is_active or self.energy < 5:
            return float('inf')
            
        distance = math.sqrt((self.x - task.x)**2 + (self.y - task.y)**2)
        energy_factor = (100 - self.energy) * 2
        workload_factor = self.workload * 50
        priority_bonus = (5 - task.priority) * 10
        
        return max(0.1, distance + workload_factor + energy_factor - priority_bonus)

    async def step(self):
        if not self.is_active:
            if self.energy <= 0:
                self.status = "OUT OF ENERGY"
            else:
                self.status = "CRITICAL FAILURE"
            return

        if self.target_task:
            dx = self.target_task.x - self.x
            dy = self.target_task.y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > self.speed:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
                # Strictly clamp energy drain
                self.energy = max(0.0, round(self.energy - 0.1, 2))
                self.status = f"Executing Task {self.target_task.id}"
                
                if self.energy <= 0:
                    self.is_active = False
                    if self.target_task:
                        self.target_task.status = "Pending"
                        self.target_task.assigned_to = None
                        self.target_task = None
            else:
                self.x = self.target_task.x
                self.y = self.target_task.y
                self.target_task.status = "Completed"
                self.workload += 1
                self.target_task = None
                self.status = "Idle"
        
        if self.status == "Idle" and self.energy < 100:
            # Strictly clamp energy gain
            self.energy = min(100.0, round(self.energy + 0.5, 2))

class SwarmManager:
    def __init__(self):
        self.robots: List[Robot] = []
        self.tasks: List[Task] = []
        self.task_counter = 0
        self.is_running = True
        self.auto_task_gen = False
        self.last_event = None
        self.reset()

    def reset(self):
        self.robots = [
            Robot(1, 100, 100),
            Robot(2, 400, 100),
            Robot(3, 700, 100)
        ]
        self.tasks = []
        self.task_counter = 0
        self.auto_task_gen = False
        self.last_event = {"type": "reset", "time": time.time()}
        return True

    def clear_tasks(self):
        self.tasks = []
        # We don't reset task_counter here to keep IDs unique, 
        # but the UI will show 0 active tasks.
        for r in self.robots:
            r.target_task = None
            if r.is_active:
                r.status = "Idle"
        self.last_event = {"type": "clear_tasks", "time": time.time()}
        return True

    def add_task(self, x: float, y: float, priority: int = 1):
        self.task_counter += 1
        new_task = Task(self.task_counter, x, y, priority)
        self.tasks.append(new_task)
        return new_task

    def add_robot(self, x: float, y: float):
        new_id = max([r.id for r in self.robots] + [0]) + 1
        new_robot = Robot(new_id, x, y)
        self.robots.append(new_robot)
        self.last_event = {"type": "deploy", "id": new_id, "x": x, "y": y, "time": time.time()}
        return new_robot

    def trigger_failure(self):
        active_robots = [r for r in self.robots if r.is_active]
        if active_robots:
            robot = random.choice(active_robots)
            robot.is_active = False
            if robot.target_task:
                task = robot.target_task
                task.status = "Pending"
                task.assigned_to = None
                robot.target_task = None
            self.last_event = {"type": "failure", "id": robot.id, "x": robot.x, "y": robot.y, "time": time.time()}
            return {"id": robot.id, "x": robot.x, "y": robot.y}
        return None

    def allocate_tasks(self):
        if not self.is_running: return
        
        pending_tasks = [t for t in self.tasks if t.status == "Pending"]
        pending_tasks.sort(key=lambda x: x.priority, reverse=True)

        for task in pending_tasks:
            best_bid = float('inf')
            best_robot = None
            
            for robot in self.robots:
                if robot.is_active and robot.target_task is None:
                    bid = robot.calculate_bid(task)
                    if bid < best_bid:
                        best_bid = bid
                        best_robot = robot
            
            if best_robot:
                task.assigned_to = best_robot.id
                task.status = "Assigned"
                best_robot.target_task = task

    async def run_loop(self):
        while True:
            if self.is_running:
                if self.auto_task_gen and random.random() < 0.02:
                    self.add_task(random.randint(50, 800), random.randint(50, 500), random.randint(1, 5))
                
                self.allocate_tasks()
                for robot in self.robots:
                    await robot.step()
            
            await asyncio.sleep(0.1)

    def get_state(self):
        avg_energy = sum(r.energy for r in self.robots) / len(self.robots) if self.robots else 0
        return {
            "robots": [
                {
                    "id": r.id, "x": r.x, "y": r.y, 
                    "energy": round(r.energy, 1), 
                    "status": r.status,
                    "workload": r.workload,
                    "is_active": r.is_active
                } for r in self.robots
            ],
            "tasks": [
                {
                    "id": t.id, "x": t.x, "y": t.y, 
                    "status": t.status, "priority": t.priority,
                    "assigned_to": t.assigned_to
                } for t in self.tasks if t.status != "Completed"
            ],
            "stats": {
                "avg_energy": round(avg_energy, 1),
                "completed_count": sum(r.workload for r in self.robots),
                "active_tasks": len([t for t in self.tasks if t.status != "Completed"]),
                "fleet_size": len(self.robots)
            },
            "last_event": self.last_event
        }
