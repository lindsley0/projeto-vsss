from test_control import TestControl
from tela_partida import Painel
from test_vision_thread import VisionThread
from lib.comm.control import ProtoControl

def main():
    # Inicializa visão em thread
    vision_thread = VisionThread(team_color_yellow=False)
    vision_thread.start()

    # Inicializa FIRASim
    control = ProtoControl(team_color_yellow=False, control_ip="127.0.0.1", control_port=20011)

    # Cria controlador dos robôs
    controller = TestControl(vision_thread, control)

    # Cria a tela
    painel = Painel(controller)
    painel.root.mainloop()
