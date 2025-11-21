# Multi-stage build for optimization
FROM python:3.11-slim as builder

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt gunicorn


# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ ./app/
COPY static/ ./static/

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port (Azure typically uses 8000 or PORT env var)
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=app.main
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Use gunicorn for production (more stable than flask dev server)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 "app.main:app"
