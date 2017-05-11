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
|  `-t <PATH` | `--temp-dir <PATH>` | Temporary path to store processing files.  For best performance, make this on the same filesystem as your Cantemo Portal storage as the script collects encodes here and moves finished files to the Cantemo Storage|
|  `-l <INT` | `--dl-limit <INT>` | Limit of how many items you want downloaded from the channel/playlist. If this is higher than the available items, all items will be downloaded |
|  `-f <PATH` | `--ffmpeg-path <PATH>` | Path to ffmpeg (if not defined, assumes `/usr/bin/ffmpeg`) |
|  `-g <PATH` | `--youtube-dl-path <PATH>` | Path to youtube-dl (if not defined, assumes `/usr/bin/youtube-dl`) |
|  | `--description-field <MD_FIELD_ID>` | Portal metadata field ID for description field |
|  | `--tags-field <MD_FIELD_ID>` | Portal metadata field ID for tags field |
|  | `--category-field <MD_FIELD_ID>` | Portal metadata field ID for category field |
|   | `--metadata-group <MD_GROUP_NAME>` | Portal metadata group (default is Film) |

### Example Syntax

`python ./demo_builder.py -y https://www.youtube.com/channel/UCxKextGEOb00qlNpFuAZgSQ -l 2 -t /path/to/processing/folder -d /path/to/cantemoportal/storage`

This will grab the first two items on my Youtube channel, place them in the `/path/to/processing/folder`, then create a folder `/path/to/processing/folder/encodes`, place encoded files and xml sidecar there, and move all those items to `/path/to/cantemoportal/storage` when complete.

`python ./demo_builder.py -y https://www.youtube.com/channel/UCxKextGEOb00qlNpFuAZgSQ -t /path/to/processing/folder -d /path/to/cantemoportal/storage -f /root/bin/ffmpeg --tags-field portal_mf34323`

This will download all items from my Youtube channel, place them in the `/path/to/processing/folder`, then create a folder `/path/to/processing/folder/encodes`, place encoded files and xml sidecar there, and move all those items to `/path/to/cantemoportal/storage` when complete.  It will assume the ffmpeg binary lives in `/root/bin/ffmpeg` on your system for the XDCAM encode.  It will also populate the XML sidecar with the tags from the Youtube items and assign them to the Cantemo Portal tags field `portal_mf34323`
