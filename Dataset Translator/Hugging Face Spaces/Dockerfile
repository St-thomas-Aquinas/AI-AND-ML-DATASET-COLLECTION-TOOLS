# ✅ Use lightweight Python base image
FROM python:3.10-slim

# ✅ Set working directory
WORKDIR /app

# ✅ Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy app code
COPY . .

# ✅ Expose port (7860 for Hugging Face, 8000 for local)
EXPOSE 7860

# ✅ Run FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
