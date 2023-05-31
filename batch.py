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

from dotenv import load_dotenv
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive']
SHARE_FOLDER_ID = os.getenv('SHARE_FOLDER_ID')

sa_creds = service_account.Credentials.from_service_account_file( 'credentials.json')
scoped_creds = sa_creds.with_scopes(SCOPES)

drive_service = build('drive', 'v3', credentials=scoped_creds)
drive_service_v2 = build('drive', 'v2', credentials=scoped_creds)

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

    model = whisper.load_model(os.getenv('MODEL_TYPE'))
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

def batch(file):
    isFile = os.path.isfile(file)
    if not isFile:
        print('not exists:', file)
        sys.exit(1)

    print("batch started.")
    inputAudio = file
    outputText = inputAudio + ".txt"
    summaryText = inputAudio + ".summary.txt"
    path = "./" + outputText
    speech2text(inputAudio, outputText)

    # add punctuation
    add_punctuation.from_sentence(outputText)

    # create summary text
    lines =  summarize_document.document_summarize(outputText)
    with open(summaryText, mode='w') as f:
        f.writelines(lines)

    print("batch terminated.")

def batchOnGoogleDrive():
    print("[Google Drive] batch started.")
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
        print(f"Found file: {file.get('name')} ({file.get('id')})")
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

    print("[Google Drive] batch terminated.")

def main():
    args = option_parser.get_option('test.mp4')
    if args.googleDrive:
        batchOnGoogleDrive()
    else:
        batch(str(args.file))

if __name__ == "__main__":
    main()
