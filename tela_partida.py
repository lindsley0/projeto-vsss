from lib.comm.control import ProtoControl
from lib.comm.vision import ProtoVision
from lib.core.data import FieldData
import threading
import time
import math

MAX_SPEED = 100  # velocidade máxima dos robôs

class RoboController:
    def __init__(self):
        self.field_data = FieldData()
        self.vision = ProtoVision(team_color_yellow=False, field_data=self.field_data)
        self.control = ProtoControl(team_color_yellow=False, control_ip="127.0.0.1", control_port=20011)
        self.running = False

    def move_robot_towards(self, robot, target_x, target_y):
        dx = target_x - robot.position.x
        dy = target_y - robot.position.y
        distance = math.hypot(dx, dy)
        if distance == 0:
            return 0, 0
        vx = MAX_SPEED * dx / distance
        vy = MAX_SPEED * dy / distance
        return vx, vy

    def start(self):
        self.running = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def stop(self):
        self.running = False
        # Para todos os robôs azuis
        for i in range(3):
            self.control.transmit_robot(i, 0, 0)

    def update_loop(self):
        while True:
            if self.running:
                # Recebe dados do FIRASim
                self.field_data = self.vision.receive_field_data()

                # Goleiro (robô 0)
                gk = self.field_data.robots_blue[0]
                vx, vy = self.move_robot_towards(gk, gk.position.x, self.field_data.ball.position.y)
                self.control.transmit_robot(0, vx, vy)

                # Zagueiro (robô 1)
                defender = self.field_data.robots_blue[1]
                target_x = max(50, self.field_data.ball.position.x - 100)
                target_y = self.field_data.ball.position.y
                vx, vy = self.move_robot_towards(defender, target_x, target_y)
                self.control.transmit_robot(1, vx, vy)

                # Atacante (robô 2)
                attacker = self.field_data.robots_blue[2]
                vx, vy = self.move_robot_towards(attacker, self.field_data.ball.position.x, self.field_data.ball.position.y)
                self.control.transmit_robot(2, vx, vy)

            time.sleep(0.05)
