from fastapi import FastAPI, Request
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import time
from metrics import request_counter, request_duration, error_counter, request_latency  # Import metrics
from fastapi import HTTPException

# Initialize FastAPI
app = FastAPI()

# Instrument FastAPI
FastAPIInstrumentor.instrument_app(app)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    # Increment request count
    request_counter.add(1, {"method": request.method, "path": request.url.path, "status_code": str(response.status_code)})

    # Record request duration
    request_duration.record(duration, {"method": request.method, "path": request.url.path})

    # Record latency metric
    request_latency.record(duration, {"method": request.method, "path": request.url.path})

    # Increment error count for 4xx and 5xx responses
    if 400 <= response.status_code < 600:
        error_counter.add(1, {"method": request.method, "path": request.url.path, "status_code": str(response.status_code)})

    return response

@app.get("/")
async def root():
    return {"message": "Hello, OpenTelemetry!"}


@app.get("/error")
async def error_route():
    raise HTTPException(status_code=500, detail="Simulated error")

#The metrics tHat i have designed above in the middleware will only catch error when they occur, if there are no errors
#then in grafana you wont see htt_requests_errors_total metric. So I have created a route that will simulate an error
