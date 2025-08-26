# goleiro.py

class Goleiro:
    def __init__(self, robot_index, field_data, control):
        self.robot_index = robot_index
        self.field_data = field_data
        self.control = control
        self.area_x = 0.5  # limite da área do gol azul

    def update(self):
        robo = self.field_data.robots[self.robot_index]
        ball = self.field_data.ball

        # Goleiro acompanha a bola apenas dentro da sua área
        target_x = max(min(ball.position.x, self.area_x), 0)
        target_y = ball.position.y

        dx = target_x - robo.position.x
        dy = target_y - robo.position.y

        robo.position.x += dx * 0.5
        robo.position.y += dy * 0.5

        vx = dx * 4.0
        vy = dy * 4.0
        self.control.transmit_robot(self.robot_index, vx, vy)



