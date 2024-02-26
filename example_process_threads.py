import trio

from trio_mongodb.process import AsyncMongoClient

async def main():
    client = AsyncMongoClient("mongodb://localhost:27017/", "your_database")
    collection = client.get_collection('your_collection')

    # Perform operations
    result = await collection.insert_one({"name": "Alice", "age": 30})
    print(f"Inserted ID: {result.inserted_id}")
    
    updateResult = await collection.update_one({"name": "Alice"}, {"$set": {"age": 31}})
    print(f"Updated count: {updateResult.modified_count} | Matched count: {updateResult.matched_count}")

    # Don't forget to close the client
    client.close()

if __name__ == "__main__":
    trio.run(main)