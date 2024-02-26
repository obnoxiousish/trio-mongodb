import trio
import multiprocessing

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from trio_mongodb.process import AsyncMongoClient

from hypercorn.trio import serve
from hypercorn import Config

class starletteExample:
    def __init__(self):
        self.client = AsyncMongoClient("mongodb://localhost:27017/", "your_database")
        self.collection = self.client.get_collection('your_collection')
        
    async def insert_document(self, request):
        data = await request.json()  # Assuming the body contains the document to insert
        result = await self.collection.insert_one(data)
        return JSONResponse({"inserted_id": str(result.inserted_id)})

    async def update_document(self, request):
        data = await request.json()  # Assuming the body contains the update details
        name_to_update = data.get("name")
        new_age = data.get("age")
        if not name_to_update or new_age is None:
            return JSONResponse({"error": "Missing data"}, status_code=400)

        update_result = await self.collection.update_one({"name": name_to_update}, {"$set": {"age": new_age}})
        return JSONResponse({"updated_count": update_result.modified_count, "matched_count": update_result.matched_count})

    async def on_shutdown(self):
        self.client.close()

if __name__ == "__main__":
    #multiprocessing.set_start_method("fork")
    
    instance = starletteExample()
    
    app = Starlette(
        debug=True,
        routes=[
            Route('/insert', instance.insert_document, methods=["POST"]),
            Route('/update', instance.update_document, methods=["POST"]),
        ],
        on_shutdown=[instance.on_shutdown]
    )
    
    config = Config()
    
    trio.run(serve, app, config)