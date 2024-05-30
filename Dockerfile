FROM python:3.10

RUN apt update && apt upgrade -y; apt-get install git curl zip neofetch ffmpeg -y\
    && apt-get install -y --no-install-recommends ffmpeg neofetch \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN chmod +x start.sh

RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

CMD bash start.sh
# CMD [""python3", "-m", "app"]
