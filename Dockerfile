# Miniflux Exporter Dockerfile
# Simplified single-stage build

FROM python:3.11-slim

# Set labels
LABEL maintainer="Miniflux Exporter Contributors"
LABEL description="Export Miniflux articles to Markdown format"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash exporter

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY miniflux_exporter/ ./miniflux_exporter/
COPY setup.py README.md ./

# Install the package
RUN pip install --no-cache-dir -e .

# Create output directory
RUN mkdir -p /output && chown -R exporter:exporter /output /app

# Switch to non-root user
USER exporter

# Set Python path
ENV PATH=/home/exporter/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Set default output directory
ENV MINIFLUX_OUTPUT_DIR=/output

# Volume for output
VOLUME ["/output"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import miniflux_exporter; print('OK')" || exit 1

# Default command
ENTRYPOINT ["miniflux-export"]
CMD ["--help"]
