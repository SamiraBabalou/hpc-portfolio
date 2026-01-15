# ----------------------------------------------------------------------
# File: Dockerfile
# Author: Samira Babalou
# Date: 2026-01-15
# Purpose:
#   Provide a reproducible environment for building and running
#   MPI-based HPC experiments, including performance analysis
#   and reporting.
#
# Usage:
#   docker build -t hpc-portfolio .
#   docker run -it hpc-portfolio
# ----------------------------------------------------------------------

# Base image
FROM ubuntu:22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# -------------------------------
# Install system dependencies (as root)
# -------------------------------
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    openmpi-bin \
    libopenmpi-dev \
    python3 \
    python3-pip \
    python3-venv \
    git \
    wget \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Create non-root user for MPI safety
# -------------------------------
RUN useradd -ms /bin/bash hpcuser

# -------------------------------
# Create workspace and fix permissions
# -------------------------------
RUN mkdir -p /workspace && chown -R hpcuser:hpcuser /workspace

# -------------------------------
# Copy repository files (as root)
# -------------------------------
COPY . /workspace
RUN chown -R hpcuser:hpcuser /workspace

# -------------------------------
# Switch to non-root user
# -------------------------------
USER hpcuser
WORKDIR /workspace

# -------------------------------
# Create Python virtual environment (as hpcuser)
# -------------------------------
RUN python3 -m venv venv && \
    /bin/bash -c "source venv/bin/activate && pip install --upgrade pip matplotlib flake8 nose"

# Make venv active by default
ENV PATH="/workspace/venv/bin:$PATH"

# Default command
CMD ["/bin/bash"]
