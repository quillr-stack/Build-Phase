FROM python:3.11-slim
WORKDIR /app
# Copy the whole project or at least the backend folder into the backend module
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt
COPY backend/ ./backend/
COPY data/ ./data/
# Set PYTHONPATH to the current directory so 'import backend' works
ENV PYTHONPATH=/app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
