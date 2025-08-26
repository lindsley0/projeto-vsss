# test_vision_field_data.py
class BallData:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

class RobotData:
    def __init__(self):
        self.position = BallData()  # reutilizando BallData só pra simplificar
        self.orientation = 0.0

class FieldData:
    def __init__(self):
        self.ball = BallData()
        self.robots_blue = [RobotData() for _ in range(3)]
        self.robots_yellow = [RobotData() for _ in range(3)]

    def update(self, vision_data):
        # Exemplo: vision_data é o objeto retornado do ProtoVision
        try:
            self.ball.x = vision_data.ball.x
            self.ball.y = vision_data.ball.y

            for i, r in enumerate(vision_data.robots_blue):
                self.robots_blue[i].position.x = r.x
                self.robots_blue[i].position.y = r.y
                self.robots_blue[i].orientation = r.orientation

            for i, r in enumerate(vision_data.robots_yellow):
                self.robots_yellow[i].position.x = r.x
                self.robots_yellow[i].position.y = r.y
                self.robots_yellow[i].orientation = r.orientation
        except Exception as e:
            print(f"[FieldData] Erro ao atualizar dados: {e}")
