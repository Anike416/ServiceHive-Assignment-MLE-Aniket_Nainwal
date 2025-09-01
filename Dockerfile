# --- Stage 1: The Builder ---

# This stage installs dependencies and finds the uvicorn executable
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .

# Copy and install dependencies

RUN pip install -r requirements.txt

# --- Stage 2: The Final Image ---
FROM python:3.11-slim

WORKDIR /app
ENV PATH="/root/.local/bin:${PATH}"
# Set PYTHONPATH
ENV PYTHONPATH=/app/src1

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy the application source code, models, and frontend
COPY src1/ /app/src1/
COPY models/ /app/models/
COPY frontend/ /app/frontend/   

EXPOSE 8000

# The CMD can now reliably find uvicorn in a standard path
CMD ["python", "-m","uvicorn", "src1.api.main:app", "--host", "0.0.0.0", "--port", "8000"]