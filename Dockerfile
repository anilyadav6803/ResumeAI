# Dockerfile for ResumeAI - Single Container Deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/resumes data/vector_db

# Set environment variables
ENV PORT=8000
ENV STREAMLIT_PORT=8501
ENV HOST=0.0.0.0

# Expose ports
EXPOSE 8000 8501

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🚀 Starting ResumeAI..."\n\
\n\
# Start backend\n\
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 &\n\
BACKEND_PID=$!\n\
\n\
# Wait for backend\n\
sleep 5\n\
\n\
# Start frontend\n\
streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true &\n\
FRONTEND_PID=$!\n\
\n\
echo "✅ ResumeAI is running!"\n\
echo "Backend: http://localhost:8000"\n\
echo "Frontend: http://localhost:8501"\n\
\n\
# Keep container running\n\
wait\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start the application
CMD ["/app/start.sh"]
