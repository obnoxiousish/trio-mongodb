import trio

from multiprocessing import Process, Queue
from pymongo import MongoClient

class AsyncMongoProcessProxy:
    def __init__(self, db_operation_queue, db_result_queue, collection_name):
        self.db_operation_queue = db_operation_queue
        self.db_result_queue = db_result_queue
        self.collection_name = collection_name

    async def _enqueue_operation(self, operation, *args, **kwargs):
        task = (self.collection_name, operation, args, kwargs)
        self.db_operation_queue.put(task)
        
        result = await trio.to_thread.run_sync(self.db_result_queue.get)
        return result

    def __getattr__(self, name):
        async def operation(*args, **kwargs):
            return await self._enqueue_operation(name, *args, **kwargs)
        return operation


class AsyncMongoClient:
    def __init__(self, mongo_uri, db_name):
        self.db_operation_queue = Queue()
        self.db_result_queue = Queue()
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.db_process = Process(
            target=self._multiprocessing_processor,
            args=(
                self.db_operation_queue,
                self.db_result_queue,
                self.mongo_uri,
                self.db_name,
            ),
        )
        self.db_process.start()

    def _multiprocessing_processor(self, db_operation_queue, db_result_queue, db_uri, db_name):
        async def db_operations_listener():
            client = MongoClient(db_uri)
            db = client[db_name]

            while True:
                task = db_operation_queue.get()
                if task == "STOP":
                    break

                collection_name, operation_name, args, kwargs = task
                collection = db[collection_name]
                operation_result = await trio.to_thread.run_sync(
                    getattr(collection, operation_name), *args, **kwargs
                )

                db_result_queue.put(operation_result)

        trio.run(db_operations_listener)

    def get_collection(self, collection_name):
        return AsyncMongoProcessProxy(self.db_operation_queue, self.db_result_queue, collection_name)

    def close(self):
        self.db_operation_queue.put("STOP")
        self.db_process.join()

def multiprocessingProcessor(db_operation_queue, db_result_queue, db_uri, db_name):
    async def db_operations_listener():
        client = MongoClient(db_uri)
        db = client[db_name]

        while True:
            task = db_operation_queue.get()
            if task == "STOP":
                break

            collection_name = task['collection_name']
            operation = task['operation']
            args = task['args']
            kwargs = task['kwargs']
            collection = db[collection_name]

            result = await trio.to_thread.run_sync(
                getattr(collection, operation), *args, **kwargs
            )

            # Simplify the result for transport if needed
            simple_result = multiprocessingResult(result)
            db_result_queue.put(simple_result)

    trio.run(db_operations_listener)

def multiprocessingResult(result):
    # Convert MongoDB operation results to a simple dictionary or similar
    # This function needs to be implemented based on specific needs
    return result
