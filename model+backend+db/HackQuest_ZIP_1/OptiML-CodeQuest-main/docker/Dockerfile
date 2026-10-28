FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PYTHONPATH=/opt/app

WORKDIR /opt/app

RUN apt-get update && apt-get install -y --no-install-recommends \
	build-essential \
	&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt /opt/app/requirements.txt
RUN pip install --no-cache-dir -r /opt/app/requirements.txt \
	&& python -m spacy download en_core_web_sm

# Copy backend source and models
COPY backend/app /opt/app/app
# Remove accidental nested duplicate if present
RUN rm -rf /opt/app/app/app || true

# Copy models directory (may be empty initially)
COPY models /opt/app/models

# Build the model inside the image so it always exists
COPY backend/build_model.py /opt/app/build_model.py
RUN python /opt/app/build_model.py

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
