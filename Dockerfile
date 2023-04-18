# Build stage
FROM python:3.11-slim-bullseye as builder
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN apt update && apt install -y build-essential \
    && pip install poetry \
    && poetry install \
    && poetry build \
    && rm -rf /var/lib/apt/lists/*

# Final stage
FROM python:3.11-slim-bullseye
COPY --from=builder /usr/src/app/dist/*.whl .
RUN pip install robodroid-*.whl
ENTRYPOINT ["robodroid"]
