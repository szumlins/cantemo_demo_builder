# Cantemo Demo Builder

Automatically Grab Content for Cantemo Customer Demo, creates XDCAM clips, and
loads into Portal Storage

## Prerequisites

  - Cantemo Portal
  - Python
  - ffmpeg
  - youtube-dl
  - requests

## Installing

After having the prerequisites in place this script requires youtube-dl and requests be installed. You can
install youtube-dl and requests with pip.

```
pip install -r requirements.txt
```

## Usage

```
demo_builder.py [-h] -y URL -d PATH -t PATH [-l INT] [-f PATH]
                    [-g PATH] [--description-field MD_FIELD_ID]
                    [--tags-field MD_FIELD_ID]
                    [--category-field MD_FIELD_ID]
                    [--metadata-group MD_GROUP_NAME]
```

### Options overview

| short flag | long flag | description |
| ------ | ------ | ------ |
|  `-h` | `--help`  | show this help message and exit |
|  `-y <URL>` | `--youtube-url <URL>` | URL of Youtube Playlist or User Page |
|  `-d <PATH` | `--cantemo-storage <PATH>` | Path to importable Cantemo Storage |
|  `-t <PATH` | `--temp-dir <PATH>` | Temporary path to store processing files |
|  `-l <INT` | `--dl-limit <INT>` | Limit of how many items you want downloaded from the channel/playlist. If this is higher than the available items, all items will be downloaded |
|  `-f <PATH` | `--ffmpeg-path <PATH>` | Path to ffmpeg (if not defined, assumes `/usr/bin/ffmpeg`) |
|  `-g <PATH` | `--youtube-dl-path <PATH>` | Path to youtube-dl (if not defined, assumes `/usr/bin/youtube-dl`) |
|  | `--description-field <MD_FIELD_ID>` | Portal metadata field ID for description field |
|  | `--tags-field <MD_FIELD_ID>` | Portal metadata field ID for tags field |
|  | `--category-field <MD_FIELD_ID>` | Portal metadata field ID for category field |
|   | `--metadata-group <MD_GROUP_NAME>` | Portal metadata group (default is Film) |
