# Use Amazon Linux as base image
FROM amazonlinux:latest

# Set environment variables to reduce cache size
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

# Install Python and remove cache to save space
RUN yum install -y python3 && \
    alternatives --install /usr/bin/python python /usr/bin/python3 1 && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3 && \
    yum clean all && rm -rf /var/cache/yum

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt /app/
COPY app /app

# Install dependencies without cache
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "main.py"]
