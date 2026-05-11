from prometheus_client import start_http_server, Summary, Counter
import time

# Create metrics to track
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
TOKEN_COUNT = Counter('llm_tokens_total', 'Total tokens generated')

@REQUEST_TIME.time()
def process_request(tokens):
    """Simulate a request and log metrics."""
    time.sleep(0.5) # Simulate latency
    TOKEN_COUNT.inc(tokens)


if name == "__main__":
    # Start Prometheus exporter on port 8001
    start_http_server(8001)
    print("Prometheus Metrics Exporter running on port 8001...")
    while True:
        process_request(150)