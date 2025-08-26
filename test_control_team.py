from lib.comm.control import ProtoControl
from lib.comm.vision import ProtoVision
from lib.core.command import TeamCommand
import time
import math


# Função para calcular velocidade proporcional até um alvo (x, y)
def move_to(robot, target_x, target_y, max_speed=10):
    dx = target_x - robot.x
    dy = target_y - robot.y
    dist = math.hypot(dx, dy)

    if dist < 0.01:  # já está no alvo
        return 0, 0

    # Normaliza direção e aplica velocidade
    vx = max_speed * dx / dist
    vy = max_speed * dy / dist

    # Simplificação: usamos vx e vy como left/right
    left = vx
    right = vy
    return left, right


def main():
    # Comandos para cada time
    team_command_blue = TeamCommand()
    team_command_yellow = TeamCommand()

    # Controle para enviar comandos
    blue_control = ProtoControl(team_color_yellow=False, team_command=team_command_blue, control_port=20011)
    yellow_control = ProtoControl(team_color_yellow=True, team_command=team_command_yellow, control_port=20011)

    # Visão: recebe estados de bola e robôs
    vision = ProtoVision(team_color_yellow=False, vision_port=23333)

    print("🏁 Iniciando partida entre Azul (ataque) e Amarelo (defesa)...")

    start_time = time.time()
    match_time = 60  # duração da partida em segundos

    while time.time() - start_time < match_time:
    # Atualiza estado do jogo
        state = vision.update()

    # Verifica se o estado é válido
        if state is None or state.ball is None:
            print("Aguardando dados da visão...")
            time.sleep(0.05)  # aguarda um pouco e tenta novamente
            continue
        print(f"Bola: x={state.ball.x:.2f}, y={state.ball.y:.2f}")
    ball = state.ball
       
    # Lista de robôs de cada time
    robots_blue = [r for r in state.robots if r.team_color_yellow == False]
    robots_yellow = [r for r in state.robots if r.team_color_yellow == True]

    # --- Estratégia Azul (ataque) ---
    if robots_blue:
        # Robô 0 = atacante → segue a bola
        left, right = move_to(robots_blue[0], ball.x, ball.y, max_speed=8)
        team_command_blue.commands[0].left_speed = left
        team_command_blue.commands[0].right_speed = right

        # Robô 1 = apoio → vai para meio caminho da bola
        if len(robots_blue) > 1:
            left, right = move_to(robots_blue[1], ball.x * 0.5, ball.y * 0.5, max_speed=6)
            team_command_blue.commands[1].left_speed = left
            team_command_blue.commands[1].right_speed = right

        # Robô 2 = cobertura → meio do campo
        if len(robots_blue) > 2:
            left, right = move_to(robots_blue[2], 0.0, 0.0, max_speed=4)
            team_command_blue.commands[2].left_speed = left
            team_command_blue.commands[2].right_speed = right

    # --- Estratégia Amarela (defesa) ---
    if robots_yellow:
        # Robô 0 = goleiro → segue a bola no eixo Y
        goal_x = -0.7
        left, right = move_to(robots_yellow[0], goal_x, ball.y, max_speed=7)
        team_command_yellow.commands[0].left_speed = left
        team_command_yellow.commands[0].right_speed = right

        # Robô 1 = marcador → vai até a bola devagar
        if len(robots_yellow) > 1:
            left, right = move_to(robots_yellow[1], ball.x, ball.y, max_speed=5)
            team_command_yellow.commands[1].left_speed = left
            team_command_yellow.commands[1].right_speed = right

        # Robô 2 = defensor fixo no meio do campo
        if len(robots_yellow) > 2:
            left, right = move_to(robots_yellow[2], -0.3, 0.0, max_speed=4)
            team_command_yellow.commands[2].left_speed = left
            team_command_yellow.commands[2].right_speed = right

    # Envia comandos para os dois times
    blue_control.update()
    yellow_control.update()

    # Pequeno delay para sincronizar (~20Hz)
    time.sleep(0.05)
