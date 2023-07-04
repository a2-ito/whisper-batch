from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError as HTTPError

from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io

import whisper
import os
import sys
import summarize_document
import add_punctuation
import option_parser
import logging
import time
import add_newline

from dotenv import load_dotenv
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive']
SHARE_FOLDER_ID = os.getenv('SHARE_FOLDER_ID')

# sa_creds = service_account.Credentials.from_service_account_file( 'credentials.json')
# scoped_creds = sa_creds.with_scopes(SCOPES)

# drive_service = build('drive', 'v3', credentials=scoped_creds)
# drive_service_v2 = build('drive', 'v2', credentials=scoped_creds)

def setLogger():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s:%(name)s - %(message)s")

def upload(uploadFileName, uploadFilePath, folderId):
    mimeType = "text/plain"
    media = MediaFileUpload(uploadFilePath, mimetype=mimeType, resumable=True)

    file_metadata = {
        'name': uploadFileName,
        'parents': [folderId],
        'driveId': os.getenv('DRIVE_ID')
    }

    response = drive_service.files().create(
        body=file_metadata, media_body=media, fields='id', supportsAllDrives=True
    ).execute()

def download(fileName, fileId):
    request = drive_service.files().get_media(fileId=fileId)
    fh = io.FileIO(fileName, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

def speech2text(inputAudio, outputText):

    modelType = 'small' if not os.getenv('MODEL_TYPE') else os.getenv('MODEL_TYPE') 
    model = whisper.load_model(modelType)
    result = model.transcribe(inputAudio, language="ja")

    with open(outputText, mode='w') as f:
        f.write(result["text"])

def fileMove(fileId, destFolderId, previousParents):
    file = drive_service.files().update(
        fileId=fileId,
        addParents=destFolderId,
        removeParents=previousParents,
        fields='id, parents',
        supportsAllDrives=True
    ).execute()

def uploadToGoogleDrive():
    # upload outputText
    upload(outputText, path, doneFolderId)
    # upload summary
    upload(summaryText, path, doneFolderId)

def addPunctuation(file):
    outputText = file + ".txt"
    punctuatedText = file + ".punctuation.txt"

    res, lines = add_punctuation.from_file(outputText)
    with open(punctuatedText, mode='w') as f:
        f.writelines(lines)

    if res == 1:
        logging.error("error occured")
        # outputText に上書きする
        with open(outputText, mode='w') as f:
            f.writelines(lines)
        return None

    return punctuatedText

def batch(file, skipRecognition):
    startTime = time.time()

    isFile = os.path.isfile(file)
    if not isFile:
        logging.error('not exists:', file)
        sys.exit(1)

    logging.info("batch started.")
    inputAudio = file
    outputText = inputAudio + ".txt"
    summaryText = inputAudio + ".summary.txt"
    newlineText = inputAudio + ".newline.txt"
    path = "./" + outputText

    if not skipRecognition:
        speech2text(inputAudio, outputText)

    # add punctuation
    punctuatedText = addPunctuation(file)
    if punctuatedText is None:
        logging.info("puctuated error. " + str(time.time() - startTime) + "[s]")
        exit(1)

    # create summary text
    lines =  summarize_document.document_summarize(punctuatedText)
    with open(summaryText, mode='w') as f:
        f.writelines(lines)

    # newline
    lines = add_newline.from_file(punctuatedText)
    with open(newlineText, mode='w') as f:
        f.writelines(lines)

    logging.info("batch terminated. " + str(time.time() - startTime) + "[s]")

def batchOnGoogleDrive():
    logging.info("[Google Drive] batch started.")
    wipFolderId = os.getenv('WIP_FOLDER_ID')
    doneFolderId = os.getenv('DONE_FOLDER_ID')
    previousParents = SHARE_FOLDER_ID

    response = drive_service.files().list(
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        q=f"parents in '{SHARE_FOLDER_ID}' and trashed = false",
        fields="nextPageToken, files(id, name)"
        ).execute()

    # 音声認識対象拡張子
    targetExtList = ['.mov', '.mp4']

    for file in response.get('files', []):
        logging.info(f"Found file: {file.get('name')} ({file.get('id')})")
        path, ext = os.path.splitext(file['name'])
        if ext.lower() in targetExtList:
            print(path, ext)

            # move to wip
            fileMove(file['id'], wipFolderId, previousParents)
            # ファイルをダウンロード
            download(file['name'], file['id'])
            batch(file['name'])
            # move to done
            fileMove(file['id'], doneFolderId, wipFolderId)
            uploadToGoogleDrive()

    logging.info("[Google Drive] batch terminated.")

def main():
    setLogger()

    defaultFile = 'test.mp4'
    args = option_parser.get_option(defaultFile)
    if args.googleDrive:
        batchOnGoogleDrive()
    else:
        batch(str(args.file), args.skipRecognition)

if __name__ == "__main__":
    main()
