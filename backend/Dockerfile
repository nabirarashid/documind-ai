# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies needed for ChromaDB compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    g++ \
    gcc \
    libc6-dev \
    make \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]