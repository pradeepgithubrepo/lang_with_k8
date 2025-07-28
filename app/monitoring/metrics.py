from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

# FastAPI router to expose /metrics endpoint
router = APIRouter()

@router.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Track number of requests to /ask endpoint
REQUEST_COUNT = Counter(
    "rag_ask_requests_total", "Total number of /ask requests"
)

# Track request latency
REQUEST_LATENCY = Histogram(
    "rag_ask_request_latency_seconds", "Latency for /ask endpoint in seconds"
)

# Graph success/failure
GRAPH_SUCCESS = Counter("langgraph_success_total", "Total successful LangGraph runs")
GRAPH_FAILURE = Counter("langgraph_failure_total", "Total failed LangGraph runs")

# Redis cache metrics
REDIS_HIT = Counter("redis_cache_hit_total", "Total Redis cache hits")
REDIS_MISS = Counter("redis_cache_miss_total", "Total Redis cache misses")
