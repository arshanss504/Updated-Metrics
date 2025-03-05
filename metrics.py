from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from prometheus_client import start_http_server

# Setup OTLP HTTP Exporter (Ensure insecure=True)
otlp_exporter = OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics")

# Configure Metric Readers (Both Prometheus and OTLP)
otlp_reader = PeriodicExportingMetricReader(otlp_exporter)

# Set Meter Provider
provider = MeterProvider(metric_readers=[otlp_reader])
set_meter_provider(provider)
meter = get_meter_provider().get_meter("fastapi_service")

# Define custom metrics
request_counter = meter.create_counter(
    "http_requests_total",
    description="Total number of HTTP requests",
)

request_duration = meter.create_histogram(
    "http_request_duration_seconds",
    description="Histogram of request duration",
)

error_counter = meter.create_counter(
    "http_requests_errors_total",
    description="Total number of failed HTTP requests",
)

request_latency = meter.create_histogram(
    "http_request_latency_seconds",
    description="Measures latency of HTTP requests",
)

# Start Prometheus metrics server (for local testing)
