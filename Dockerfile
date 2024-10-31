FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash"]
# CMD ["python", "community-version.py", "example/ztm-logo.png"]


# docker build -t ascii-art .

# Linux
# docker run -it --rm -v $(pwd):/app ascii-art
# Windows
# docker run -it --rm -v path:/app ascii-art
