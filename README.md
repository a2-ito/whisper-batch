# whisper-batch

Transcrbes and summarize data on google drive with whisper.

## usage

### prequisite

python package install
```
pip install -r requirements.txt
```

[FFmpeg](https://ffmpeg.org/download.html) is required on whisper.

### 1. Local Mode
```
python batch.py -f [input file]
```

### 2. Google Drive Mode
A credential file like `credentials.json` is required to use Google Drive API.

You also need to specify `.env` as below
```.env
SHARE_FOLDER_ID=[ommited]
DRIVE_ID=[ommitted]
MODEL_TYPE=small
WIP_FOLDER_ID=[ommited]
DONE_FOLDER_ID=[ommitted]
```
