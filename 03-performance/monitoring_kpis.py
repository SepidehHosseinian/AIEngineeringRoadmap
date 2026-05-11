"""
================================================================================
TECHNICAL DECISION: Performance Monitoring & KPI Benchmarking
================================================================================

1. CONTEXT:
   Optimization without measurement is just guessing. To justify the 
   infrastructure costs, we must track precise metrics.

2. PROBLEM SOLVED:
   - Blind Optimization: Helps us see if Quantization actually improved speed.
   - User Experience (UX): Latency p95 ensures that most users have a smooth 
     experience, not just the "average" user.

3. BUSINESS VALUE:
   - Data-Driven Decisions: "Should we buy more GPUs?" - The KPIs will tell us.
   - Cost Visibility: Tracking cost per 1k tokens prevents budget surprises.

4. METRICS DEFINITION:
   - TPS: Throughput measure (Higher is better).
   - p95/p99 Latency: Reliability measure (Lower is better).
   - Cost: Efficiency measure (Lower is better).
================================================================================
"""

import time
import numpy as np

class LLMMonitor:
    def __init__(self, cost_per_1k_tokens=0.002): # Default for a mid-tier model
        self.latencies = []
        self.tps_records = []
        self.cost_per_1k = cost_per_1k_tokens
        self.total_tokens = 0

    def record_inference(self, start_time, end_time, token_count):
        duration = end_time - start_time
        tps = token_count / duration

        self.latencies.append(duration)
        self.tps_records.append(tps)
        self.total_tokens += token_count

    def get_report(self):
        """
        Calculates KPIs including p95 and p99 percentiles.
        Percentiles are crucial because they show the 'worst-case' 
        latency experienced by real users.
        """
        p95 = np.percentile(self.latencies, 95)
        p99 = np.percentile(self.latencies, 99)
        avg_tps = np.mean(self.tps_records)
        total_cost = (self.total_tokens / 1000)  self.cost_per_1k

        return {
            "Average TPS": f"{avg_tps:.2f} tokens/sec",
            "p95 Latency": f"{p95:.3f} sec",
            "p99 Latency": f"{p99:.3f} sec",
            "Total Tokens Processed": self.total_tokens,
            "Estimated Cost": f"${total_cost:.4f}"
        }

# --- Benchmarking Scenario ---

if name == "__main__":
    monitor = LLMMonitor(cost_per_1k_tokens=0.0015) # Example: Llama-3 price

    print("🚀 Simulating 100 API requests...")

    # Simulating some inference data
    for _ in range(100):
        start = time.time()
        # Simulated delay (network + generation)
        time.sleep(np.random.uniform(0.1, 1.2)) 
        end = time.time()

        tokens = np.random.randint(50, 500)
        monitor.record_inference(start, end, tokens)

    # Output the KPI Report
    report = monitor.get_report()
    print("\n📊 --- PERFORMANCE KPI REPORT ---")
    for kpi, value in report.items():
        print(f"{kpi}: {value}")