import trio

from pymongo import MongoClient
from trio_mongodb.threads import AsyncCollectionWrapper


async def main():
    db_client = MongoClient('mongodb://localhost:27017/')
    db = db_client['your_database']
    raw_collection = db['your_collection']
    collection = AsyncCollectionWrapper(raw_collection)

    # Insert a document asynchronously and print the result
    insert_result = await collection.insert_one({'name': 'Alice', 'age': 30})
    print(f"Insert results: Inserted ID = {insert_result.inserted_id}")

    # Update a document asynchronously and print the result
    update_result = await collection.update_one({'name': 'Alice'}, {'$set': {'age': 31}})
    print(f"Update results: Matched count = {update_result.matched_count}, Modified count = {update_result.modified_count}")


if __name__ == "__main__":
    trio.run(main)
