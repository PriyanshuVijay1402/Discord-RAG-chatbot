from prometheus_client import Counter, Summary

REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["endpoint"])
REQUEST_LATENCY = Summary("api_request_latency_seconds", "API request latency", ["endpoint"])
