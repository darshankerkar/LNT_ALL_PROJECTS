# ============================================================================
# MULTI-STAGE DOCKERFILE FOR PRODUCTION-GRADE TO-DO API
# Stage 1: Builder - prepares dependencies and artifacts
# Stage 2: Runtime - minimal production image (~150MB vs 1GB single-stage)
# ============================================================================

# ---- STAGE 1: BUILDER ----
FROM python:3.13-slim as builder

LABEL maintainer="DevOps Team <devops@example.com>"
LABEL description="To-Do API - Multi-stage builder image"

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install packages to /build directory
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# ---- STAGE 2: RUNTIME ----
FROM python:3.13-slim

LABEL maintainer="DevOps Team <devops@example.com>"
LABEL version="1.0.0"
LABEL description="Containerized To-Do REST API"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:$PATH \
    PORT=5000 \
    DEBUG=False \
    API_VERSION=1.0.0

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy only built artifacts from builder stage (minimal footprint)
COPY --from=builder /build/.local /root/.local

# Copy application code
COPY app.py .

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check configuration
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Expose port
EXPOSE 5000

# Run application with gunicorn (production WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
