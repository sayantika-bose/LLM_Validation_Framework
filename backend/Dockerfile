# Use Python 3.12 as base image
FROM python:3.12-slim-bullseye

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy application code
COPY ./app ./app
COPY main.py .

# Expose port
EXPOSE 8000

# Set PYTHONPATH so 'from app.routers import prompt' works
ENV PYTHONPATH=/app

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
