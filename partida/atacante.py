# atacante.py
import math

class Atacante:
    def __init__(self, robot_index, field_data, control):
        self.robot_index = robot_index
        self.field_data = field_data
        self.control = control

    def update(self):
        try:
            # Pega o robô pelo índice diretamente
            robo = self.field_data.robots[self.robot_index]
            bola = self.field_data.ball

            # Calcula vetor até a bola
            dx = bola.position.x - robo.position.x
            dy = bola.position.y - robo.position.y
            dist = math.sqrt(dx**2 + dy**2)

            # Se já está na bola -> ir para o gol adversário
            if dist < 0.2:
                goal_x, goal_y = 1.5, 0  # posição do gol inimigo
                dx = goal_x - robo.position.x
                dy = goal_y - robo.position.y

            # Normalizar
            norm = math.sqrt(dx**2 + dy**2)
            if norm > 0:
                dx /= norm
                dy /= norm

            # Velocidade
            vx = dx * 1.5  # aumentei para não ficarem lentos
            vy = dy * 1.5

            # Envia comando ao FIRASim
            self.control.transmit_robot(self.robot_index, vx, vy)

        except IndexError:
            print(f"[ERRO] Robô atacante {self.robot_index} não encontrado!")
        except Exception as e:
            print(f"[ERRO Atacante] {e}")

