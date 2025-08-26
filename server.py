import asyncio
import websockets
import json

async def control_robots():
    uri = "ws://localhost:8765"  # Substitua pelo endereço do servidor WebSocket do FirA Sim
    async with websockets.connect(uri) as websocket:
        # Enviar comando para mover robô
        command = {
            "robot_id": 0,
            "move": {"x": 1.0, "y": 0.0}  # Mover para a direita
        }
        await websocket.send(json.dumps(command))
        print("Comando enviado:", command)

        # Receber estado da simulação
        response = await websocket.recv()
        state = json.loads(response)
        print("Estado recebido:", state)

# Executar a função de controle
asyncio.run(control_robots())
