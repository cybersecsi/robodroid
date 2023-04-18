# Build stage
FROM python:3.11-slim-bullseye as builder
WORKDIR /usr/src/app
COPY . /usr/src/app/
RUN apt update && apt install -y build-essential \
    && pip install poetry \
    && poetry install \
    && poetry build -f wheel \
    && rm -rf /var/lib/apt/lists/*

# Final stage
FROM python:3.11-slim-bullseye
ENV USER="robodroid" \
    GROUP="robodroid" \
    PATH="/home/robodroid/.local/bin:$PATH"
RUN RUN getent group $GROUP || groupadd -r -g 1000 $GROUP \
    && useradd -rm -d /home/robodroid -s /bin/bash -g $GROUP -u 1000 robodroid
COPY --from=builder /usr/src/app/dist/*.whl .
RUN pip install robodroid-*.whl \
    && rm robodroid-*.whl
USER robodroid
# Ensure the main .RoboDroid folder is created
RUN mkdir -p /home/robodroid/.RoboDroid
ENTRYPOINT ["robodroid"]
