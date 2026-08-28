import asyncio

import websockets


async def run_websocket_test():
    async with websockets.connect(
        "ws://127.0.0.1:8000/ws/chat"
    ) as websocket:
        await websocket.send(
            "Explain WebSockets in one sentence."
        )

        response = await websocket.recv()

        print(response)


if __name__ == "__main__":
    asyncio.run(run_websocket_test())