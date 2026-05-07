
"""
================================================================================
ARCHITECTURAL DECISION: Why State Management & HITL?
================================================================================

1. CONTEXT:
   In high-stakes environments like Fintech (AzkiVam) or Banking (Behsazan), 
   AI cannot be a "black box" that makes autonomous financial decisions without 
   oversight. We need a way to track the "state" of a conversation over weeks, 
   not just seconds.

2. PROBLEM SOLVED:
   - Statelessness: Standard APIs forget everything after one request. We need 
     "Long-term Memory" for complex loan application flows.
   - Trust Gap: Banks don't trust LLMs to move money. Human-in-the-Loop (HITL) 
     bridges this by allowing a human to verify the AI's reasoning.

3. BUSINESS VALUE:
   - Compliance: Meets regulatory requirements for audit trails in financial 
     transactions.
   - User Retention: Users can leave a chat and return 2 days later, and the 
     AI Agent will remember exactly where they left off.
   - Risk Mitigation: Prevents costly errors by interrupting the process 
     at critical decision points for human approval.

4. TECHNICAL IMPLEMENTATION:
   - Persistent Threading: Each session has a unique ID and state object.
   - Interrupt/Resume Pattern: The workflow can "pause" its execution state 
     until an external signal (Human Approval) is received.
================================================================================
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional

class StateManager:
    def __init__(self):
        # In-memory store simulating a persistent Database (like Redis or Postgres)
        self.threads: Dict[str, Dict[str, Any]] = {}

    def create_thread(self, user_id: str) -> str:
        """Initializes a new conversation or process thread."""
        thread_id = f"thread_{uuid.uuid4().hex[:8]}"
        self.threads[thread_id] = {
            "user_id": user_id,
            "history": [],
            "status": "active",
            "pending_action": None,
            "updated_at": datetime.now().isoformat()
        }
        return thread_id

    def update_state(self, thread_id: str, new_message: str, metadata: Optional[dict] = None):
        """Appends new interaction to the state."""
        if thread_id in self.threads:
            self.threads[thread_id]["history"].append({
                "role": "user",
                "content": new_message,
                "timestamp": datetime.now().isoformat()
            })
            if metadata:
                self.threads[thread_id].update(metadata)

    def request_human_approval(self, thread_id: str, action_details: str):
        """Interrupts the AI flow and waits for human verification."""
        print(f"⚠️ [SYSTEM] AI requested approval for: {action_details}")
        self.threads[thread_id]["status"] = "pending_approval"
        self.threads[thread_id]["pending_action"] = action_details

    def approve_action(self, thread_id: str, approved_by: str):
        """Resumes the flow after human validation."""
        if thread_id in self.threads and self.threads[thread_id]["status"] == "pending_approval":
            print(f"✅ [APPROVAL] Action approved by {approved_by} for thread {thread_id}.")
            self.threads[thread_id]["status"] = "active"
            self.threads[thread_id]["pending_action"] = None
            return True
        return False

# --- Simulation for Interview / Demo ---

def run_hitl_demo():
    manager = StateManager()
    
    # 1. Start a loan application process
    thread_id = manager.create_thread(user_id="sepideh_01")
    manager.update_state(thread_id, "I want to apply for a 50M loan.")
    
    # 2. AI calculates risk but requires a human to sign off
    manager.request_human_approval(
        thread_id, 
        action_details="Approve 50M Tomans loan based on credit score 740"
    )
    
    # 3. Check thread status (It should be blocked/pending)
    print(f"Current Thread Status: {manager.threads[thread_id]['status']}")
    
    # 4. Human (Admin) reviews and approves
    manager.approve_action(thread_id, approved_by="Admin_User_01")
    
    print(f"Final Thread Status: {manager.threads[thread_id]['status']}")

if __name__ == "__main__":
    run_hitl_demo()
