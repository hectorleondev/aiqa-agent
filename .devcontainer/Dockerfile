# Use Python 3.11 slim image for smaller size and faster builds
FROM python:3.11-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Essential build tools
    build-essential \
    # Git for version control
    git \
    # Curl for downloading packages
    curl \
    # For debugging and development
    procps \
    # For network troubleshooting
    net-tools \
    # For file operations
    tree \
    # Clean up apt cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install common development tools
RUN pip install --upgrade pip setuptools wheel

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /workspace -s /bin/bash appuser

# Copy requirements files first to leverage Docker layer caching
COPY requirements.txt dev-requirements.txt ./

# Install Python dependencies
# Install production dependencies first, then dev dependencies
RUN pip install -r requirements.txt && \
    pip install -r dev-requirements.txt

# Install additional development tools for better dev experience
RUN pip install \
    # Code formatting
    black \
    isort \
    # Linting
    flake8 \
    pylint \
    # Type checking
    mypy \
    # Auto-completion and development server with reload
    python-lsp-server[all] \
    # For interactive debugging
    ipdb \
    # For environment management
    python-dotenv

# Create directories that might be needed
RUN mkdir -p /workspace/.vscode \
    /workspace/.pytest_cache \
    /workspace/__pycache__ \
    /workspace/app \
    /workspace/tests \
    && chown -R appuser:appuser /workspace

# Switch to non-root user
USER appuser

# Expose the default FastAPI port
EXPOSE 8000

# Set the default command to keep container running
CMD ["/bin/bash"]

# Health check for FastAPI application (optional, can be used when running the app)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1
