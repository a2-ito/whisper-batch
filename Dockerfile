FROM python:3.9.16-bullseye

RUN apt-get -y update && \
  apt-get -y upgrade && \
  apt-get install -y mecab && \
  apt-get install -y libmecab-dev && \
  apt-get install -y mecab-ipadic-utf8 && \
  apt-get install -y git && \
  apt-get install -y make && \
  apt-get install -y curl && \
  apt-get install -y xz-utils && \
  apt-get install -y file && \
  apt-get install -y sudo

# mecab-ipadic-NEologdのインストール
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
  cd mecab-ipadic-neologd && \
  ./bin/install-mecab-ipadic-neologd -n -y && \
  echo dicdir = `mecab-config --dicdir`"/mecab-ipadic-neologd">/etc/mecabrc && \
  sudo cp /etc/mecabrc /usr/local/etc && \
  cd ..

WORKDIR /app
COPY batch.py /app
COPY summarize_document.py /app
COPY credentials.json /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

ARG version="6.0"
#ARG arch="arm64"
#ARG arch="amd64"

RUN export arch=$(dpkg --print-architecture) && \
    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-${arch}-static.tar.xz && \
    tar Jxvf ./ffmpeg-release-${arch}-static.tar.xz && \
    cp ./ffmpeg-${version}-${arch}-static/ffmpeg /usr/local/bin/

CMD [ "python", "./batch.py"]
