"""
SCENARIO: An AI Worker that processes financial documents asynchronously.
This architecture is essential for fintechs like AzkiVam to handle heavy loads.
"""

import asyncio
import uuid
from datetime import datetime

class AsyncAIArchitect:
    def __init__(self):
        # In production, this would be Redis or RabbitMQ
        self.task_queue = asyncio.Queue()
        self.results_db = {} 

    async def submit_document_task(self, document_id: str, analysis_type: str):
        """
        Simulates an API endpoint receiving a document and returning a Task ID immediately.
        """
        task_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # Adding task to the background queue
        await self.task_queue.put({
            "task_id": task_id,
            "doc_id": document_id,
            "type": analysis_type,
            "status": "queued",
            "created_at": timestamp
        })

        print(f"📥 Task {task_id} accepted for Document {document_id}. Status: Queued.")
        return task_id

    async def ai_worker_process(self):
        """
        The background worker that consumes tasks and performs heavy AI inference.
        """
        while True:
            task = await self.task_queue.get()
            task_id = task["task_id"]

            print(f"⚙️ Worker: Starting heavy AI analysis for Task {task_id}...")

            # Simulate heavy RAG or LLM processing time
            await asyncio.sleep(3) 

            # Update internal DB with the result
            self.results_db[task_id] = {
                "status": "completed",
                "result": f"Analysis for {task['type']} completed successfully.",
                "processed_at": datetime.now().isoformat()
            }

            print(f"✅ Worker: Task {task_id} finished.")
            self.task_queue.task_done()

    async def get_status(self, task_id: str):
        """Allows the frontend to poll for results without blocking."""
        return self.results_db.get(task_id, {"status": "processing"})

async def main():
    architect = AsyncAIArchitect()

    # 1. Start the background worker (Simulating a separate service)
    worker_task = asyncio.create_task(architect.ai_worker_process())

    # 2. Simulate incoming API requests
    t1 = await architect.submit_document_task("DOC_9921", "Credit_Scoring")

    t2 = await architect.submit_document_task("DOC_8830", "Fraud_Detection")

    # 3. Check status after a short delay
    await asyncio.sleep(4)
    status = await architect.get_status(t1)
    print(f"\n📊 Current Status of {t1}: {status}")

    # Clean up
    worker_task.cancel()

if name == "__main__":
    asyncio.run(main())