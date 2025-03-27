
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend build
COPY backend /app/backend
COPY frontend/dist /app/backend/app/static

# Expose port
EXPOSE 8888

# Run the FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8888"]
