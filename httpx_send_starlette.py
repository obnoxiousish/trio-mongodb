import trio

from httpx import AsyncClient

async def main():
    async with AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8000/insert", json={"name": "Alice", "age": 30})
        print(response.json())
        
        response = await client.post("http://127.0.0.1:8000/update", json={"name": "Alice", "age": 31})
        print(response.json())
        
if __name__ == "__main__":
    trio.run(main)