# Google-Drive-File-Downloader

<a href="https://pypi.org/project/googledrivefiledownloader/" alt="Google-Drive-File-Downloader"> <img src="https://img.shields.io/pypi/dm/googledrivefiledownloader?color=green" /></a>

Helps to download google drive files with ease 🎉

Installing the Package:

`pip install googleDriveFileDownloader`

Sample code:

```python
from googleDriveFileDownloader import googleDriveFileDownloader
gdownloader = googleDriveFileDownloader()
gdownloader.downloadFile("https://drive.google.com/uc?id=1O4x8rwGJAh8gRo8sjm0kuKFf6vCEm93G&export=download")
```

You can also provide `custom file name` : 
```python
gdownloader.downloadFile("https://drive.google.com/uc?id=1O4x8rwGJAh8gRo8sjm0kuKFf6vCEm93G&export=download","NewFile.zip") #Make sure to use the custom file name along with the file extension if exists
```

* It will automatically save the file with the name as stored in the drive
