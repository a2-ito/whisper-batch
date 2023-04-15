# whisper-batch

Transcrbes and summarize data on google drive with whisper.

## usage

### prequisite

A credential file like `credentials.json` is required to use Google Drive API.

You also need to specify `.env` as below
```.env
SHARE_FOLDER_ID=[ommited]
DRIVE_ID=[ommitted]
MODEL_TYPE=small
WIP_FOLDER_ID=[ommited]
DONE_FOLDER_ID=[ommitted]
```
```
python batch.py
```
