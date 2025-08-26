# test_control.py
from atacante import Atacante
from goleiro import Goleiro
from zagueiro import Zagueiro

class TestControl:
    def __init__(self, vision_thread, control):
        self.field_data = vision_thread.field_data
        self.control = control
        self.running = False

        # Criação dos robôs
        self.atacante = Atacante(0, self.field_data, self.control)
        self.zagueiro = Zagueiro(1, self.field_data, self.control)
        self.goleiro  = Goleiro(2, self.field_data, self.control)

        self.robots = [self.goleiro, self.zagueiro, self.atacante]
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
        # Para todos os robôs
        for i in range(len(self.robots)):
            self.control.transmit_robot(i, 0, 0)
        print("Partida parada")

    def _run_loop(self):
        import time
        while True:
            if self.running:
                for robo in self.robots:
                    try:
                        robo.update()
                    except Exception as e:
                        print(f"[Erro no loop dos robôs] {e}")
            time.sleep(0.05)
