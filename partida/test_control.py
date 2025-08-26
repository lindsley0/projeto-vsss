# test_control.py

import threading
import time
from atacante import Atacante
from goleiro import Goleiro
from zagueiro import Zagueiro

class TestControl:
    def __init__(self, field_data, control, vision):
        """
        field_data: objeto com posições da bola e dos robôs
        control: objeto que envia comandos para FIRASim
        vision: objeto que recebe dados do FIRASim em tempo real
        """
        self.field_data = field_data
        self.control = control
        self.vision = vision

        # Controle da partida
        self.running = False

        # Criação dos robôs
        self.atacante = Atacante(0, self.field_data, self.control)
        self.zagueiro = Zagueiro(1, self.field_data, self.control)
        self.goleiro  = Goleiro(2, self.field_data, self.control)

        self.robots = [self.goleiro, self.zagueiro, self.atacante]

        # Thread para o loop contínuo dos robôs
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    # --------------------------
    # Controle da partida
    # --------------------------
    def start(self):
        self.running = True
        print("Partida iniciada")

    def stop(self):
        self.running = False
        # parar todos os robôs
        for i in range(len(self.robots)):
            self.control.transmit_robot(i, 0, 0)
        print("Partida parada")

    def reset(self):
        self.stop()
        # Opcional: reposicionar bola e robôs no FIRASim
        print("Partida resetada")

    # --------------------------
    # Loop interno contínuo
    # --------------------------
    def _run_loop(self):
        """Loop interno que atualiza os robôs continuamente"""
        while True:
            if self.running:
                try:
                    # Atualiza dados do FIRASim em tempo real
                    self.field_data = self.vision.receive_field_data()

                    # Atualiza a lógica de cada robô
                    for robo in self.robots:
                        robo.update()

                except Exception as e:
                    print(f"Erro no loop dos robôs: {e}")
            time.sleep(0.05)  # Atualização a cada 50ms

    def loop(self):
        """Método alternativo para rodar a lógica (não usado se _run_loop estiver ativo)"""
        while True:
            if self.running:
                self.goleiro.update()
                self.zagueiro.update()
                self.atacante.update()
            time.sleep(0.05)


