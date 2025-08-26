# controler.py

import threading
import time
from test_control import TestControl
from tela_partida import Painel

# Bibliotecas FIRASim (ajuste os imports conforme sua instalação)
from lib.comm.control import ProtoControl
from lib.core.data import FieldData
from lib.comm.vision import ProtoVision

def main():
    # Configuração do FIRASim
    control = ProtoControl(team_color_yellow=False, control_ip="127.0.0.1", control_port=20011)
    field_data = FieldData()
    vision = ProtoVision(team_color_yellow=False, field_data=field_data)

    # Cria o controlador dos robôs, agora passando vision
    controller = TestControl(field_data, control, vision)  # Substituído para incluir vision

    # Cria a tela e passa o controlador
    painel = Painel(controller)

    # Thread para atualizar as posições do FIRASim
    def update_field_data():
        while True:
            try:
                # Recebe dados do FIRASim
                new_field_data = vision.receive_field_data()  # Evita sobrescrever field_data da thread principal
                controller.field_data = new_field_data  # Atualiza dados para os robôs
            except Exception as e:
                print(f"Erro lendo posições: {e}")
            time.sleep(0.05)

    threading.Thread(target=update_field_data, daemon=True).start()

    # Inicializa a interface
    painel.root.mainloop()

if __name__ == "__main__":
    main()

