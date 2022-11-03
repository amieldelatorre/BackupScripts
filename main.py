from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gAuth = GoogleAuth()
gAuth.LocalWebserverAuth()

drive = GoogleDrive(gAuth)

file1 = drive.CreateFile({'title': 'Hello2.txt'})
file1.SetContentFile("H:/ISOs/ubuntu-22.04.1-desktop-amd64.iso")
file1.Upload()
