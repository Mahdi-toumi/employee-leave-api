# 1. Use a lightweight Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first (for caching speed)
COPY requirements.txt .

# 4. Install Python dependencies
# We install 'opentelemetry-distro' to enable auto-tracing later
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install opentelemetry-distro opentelemetry-exporter-otlp

# 5. Run the bootstrap command to install specific OTel libraries
RUN opentelemetry-bootstrap -a install

# 6. Copy the rest of the application code
COPY app/ ./app

# 7. Define the command to run the app
# We use 'opentelemetry-instrument' to automatically wrap the app with tracing
CMD ["opentelemetry-instrument", \
    "--traces_exporter", "otlp", \
    "--metrics_exporter", "none", \
    "--service_name", "employee-leave-api", \
    "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]