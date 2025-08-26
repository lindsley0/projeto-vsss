# tela_partida.py

import tkinter as tk
import threading
import time

class Painel:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Informações da Partida")

        # Text box para informações (crie antes da thread)
        self.text_info = tk.Text(self.root, height=25, width=50)
        self.text_info.pack()

        # Frame para botões
        frame = tk.Frame(self.root)
        frame.pack()
        tk.Button(frame, text="Iniciar", command=self.controller.start).grid(row=0, column=0)
        tk.Button(frame, text="Parar", command=self.controller.stop).grid(row=0, column=1)
        ##tk.Button(frame, text="Resetar", command=self.controller.reset).grid(row=0, column=2)

        # Thread para atualizar posições
        threading.Thread(target=self.update_positions, daemon=True).start()

        self.root.mainloop()


    def update_positions(self):
     while True:
        try:
            self.text_info.delete('1.0', tk.END)

            # Bola
            if hasattr(self.controller.field_data, 'ball'):
                bola = self.controller.field_data.ball
                if hasattr(bola, 'position'):
                    self.text_info.insert(tk.END,
                        f"Bola: x={bola.position.x:.2f}, y={bola.position.y:.2f}\n\n"
                    )
                else:
                    self.text_info.insert(tk.END, "Bola: posição não disponível\n\n")
            else:
                self.text_info.insert(tk.END, "Bola: não detectada\n\n")

            # Robôs do time azul (índices 0,1,2)
            if hasattr(self.controller.field_data, 'robots') and len(self.controller.field_data.robots) >= 3:
                for i, robo in enumerate(self.controller.field_data.robots[:3]):
                    tipo = "Atacante" if i == 0 else "Zagueiro" if i == 1 else "Goleiro"
                    if hasattr(robo, 'position'):
                        self.text_info.insert(tk.END,
                            f"{tipo} Team Azul: x={robo.position.x:.2f}, y={robo.position.y:.2f}\n"
                        )
                    else:
                        self.text_info.insert(tk.END,
                            f"{tipo} Team Azul: posição não disponível\n"
                        )
            else:
                self.text_info.insert(tk.END, "Robôs Azuis: não detectados\n")

            # Robôs do time amarelo (índices 3,4,5)
            if hasattr(self.controller.field_data, 'robots') and len(self.controller.field_data.robots) >= 6:
                for i, robo in enumerate(self.controller.field_data.robots[3:6]):
                    tipo = "Atacante" if i == 0 else "Zagueiro" if i == 1 else "Goleiro"
                    if hasattr(robo, 'position'):
                        self.text_info.insert(tk.END,
                            f"{tipo} Team Amarelo: x={robo.position.x:.2f}, y={robo.position.y:.2f}\n"
                        )
                    else:
                        self.text_info.insert(tk.END,
                            f"{tipo} Team Amarelo: posição não disponível\n"
                        )
            else:
                self.text_info.insert(tk.END, "Robôs Amarelos: não detectados\n")

        except Exception as e:
            self.text_info.insert(tk.END, f"Erro lendo posições: {e}\n")

        time.sleep(0.1)

