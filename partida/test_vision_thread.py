# test_vision_thread.py
import threading
import time
from test_vision_field_data import FieldData
from lib.comm.vision import ProtoVision

class VisionThread:
    def __init__(self, team_color_yellow=False):
        self.field_data = FieldData()
        self.vision = ProtoVision(team_color_yellow=team_color_yellow)
        self.running = False
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while True:
            if self.running:
                try:
                    data = self.vision.receive_field_data()
                    self.field_data.update(data)
                except Exception as e:
                    print(f"[VisionThread] Erro recebendo dados: {e}")
            time.sleep(0.05)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False
