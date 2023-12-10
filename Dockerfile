FROM python:3.10.10-slim AS base 

FROM base AS builder

# RUN apt-get update && apt-get install -y --no-install-recommends curl && apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base 

WORKDIR /usr/src/app
COPY --from=builder /usr/local/lib/python3.10/ /usr/local/lib/python3.10/

COPY . .

CMD ["python", "backend/main.py"]
