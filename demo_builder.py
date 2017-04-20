import os
import sys
import argparse
import subprocess
import requests
import json
from xml.sax.saxutils import escape

#build our arguments
parser = argparse.ArgumentParser(description='Automatically Grab Content for Cantemo Customer Demo, creates XDCAM clips, and loads into Portal Storage',epilog='This script requires ffmpeg, youtube-dl and requests be installed.  You can install youtube-dl and requests with pip.')
parser.add_argument('-y','--youtube-url',dest='yt_url',metavar="URL",type=str,help="URL of Youtube Playlist or User Page",required=True)
parser.add_argument('-d','--cantemo-storage',dest='storage',metavar="PATH",type=str,help="Path to importable Cantemo Storage",required=True)
parser.add_argument('-t','--temp-dir',dest='temp_dir',type=str,metavar="PATH",help="Temporary path to store processing files",required=True)
parser.add_argument('-l','--dl-limit',dest='limit',type=int,metavar="INT",default=0,help="Limit of how many items you want downloaded from the channel/playlist.  If this is higher than the available items, all items will be downloaded")
parser.add_argument('-f','--ffmpeg-path',dest='ffmpeg_path',type=str,metavar="PATH",default='/usr/bin/ffmpeg',help='Path to ffmpeg (if not defined, assumes /usr/bin/ffmpeg)')
parser.add_argument('-g','--youtube-dl-path',dest='youtubedl_path',type=str,metavar="PATH",default='/usr/bin/youtube-dl',help='Path to youtube-dl (if not defined, assumes /usr/bin/youtube-dl)')
parser.add_argument('--description-field',dest='md_desc',type=str,default=False,metavar="MD_FIELD_ID",help='Portal metadata field ID for description field')
parser.add_argument('--tags-field',dest='md_tags',type=str,default=False,metavar="MD_FIELD_ID",help='Portal metadata field ID for tags field')
parser.add_argument('--category-field',dest='md_cat',type=str,default=False,metavar="MD_FIELD_ID",help='Portal metadata field ID for category field')
parser.add_argument('--metadata-group',dest='md_group',type=str,default='Film',metavar="MD_GROUP_NAME",help='Portal metadata group (default is Film)')
args = parser.parse_args()

#functions
def check_vars():
	#check our vars
	r = requests.get(args.yt_url)
	if r.status_code != 200:
		print "URL " + args.yt_url + " could not be accessed or returned an improper response.  Exiting."
		exit(1)
	
	if not os.path.exists(args.storage):
		print "Path " + args.storage + " could not be found.  Exiting."
		exit(1)

	if not os.path.exists(args.temp_dir):
		print "Path " + args.temp_dir + " could not be found.  Exiting."
		exit(1)

def encode_item(item_path):
	if not os.path.exists(os.path.abspath(args.temp_dir) + '/encodes'):
		os.makedirs(os.path.abspath(args.temp_dir) + '/encodes')
	this_filename = os.path.splitext(os.path.basename(item_path))[0]
	out_file = os.path.abspath(args.temp_dir) + '/encodes/' + this_filename + '.mxf'	
	print 'Starting encode of ' + out_file
	ffcmd = [args.ffmpeg_path,'-y','-i',item_path,'-hide_banner','-loglevel','info','-r','29.97','-vf','scale=1920:1080','-pix_fmt','yuv422p','-vcodec','mpeg2video','-non_linear_quant','1','-flags','+ildct+ilme','-top','1','-dc','10','-intra_vlc','1','-qmax','3','-lmin','1*QP2LAMBDA','-vtag','xd5c','-rc_max_vbv_use','1','-rc_min_vbv_use','1','-g','12','-b:v','50000k','-minrate','50000k','-maxrate','50000k','-bufsize','8000k','-acodec','pcm_s16le','-ar','48000','-bf','2','-ac','2',out_file]
	p = subprocess.Popen(ffcmd)
	p.wait()
	sys.stdout.write("\n")
	if p.returncode !=0:
		print 'There were errors while encoding ' + item_path + '.  Please check this file'
	
def parse_item(item_path):
	#parse out our json from YT
	with open(item_path) as data_file:    
		data = json.load(data_file)
		
	#build our metadata template
	metadata_doc_template = """<?xml version="1.0" encoding="UTF-8"?>
<MetadataDocument xmlns="http://xml.vidispine.com/schema/vidispine">
	<group>""" + args.md_group + """</group>
	<timespan start="-INF" end="+INF">
		<field>
			<name>title</name>
			<value>""" + escape(data['title']) + """</value>
		</field>"""
			
	if args.md_desc is not False:
		metadata_doc_template = metadata_doc_template + """
		<field>
			<name>""" + args.md_desc + """</name>
			<value>""" + escape(data['description']) + """</value>
		</field>"""

	if args.md_tags is not False:
		metadata_doc_template = metadata_doc_template + """
		<field>
			<name>""" + args.md_tags + """</name>"""
		for tag in data['tags']:
			metadata_doc_template = metadata_doc_template + """
			<value>""" + escape(tag) + """</value>"""
		metadata_doc_template = metadata_doc_template + """
		</field>""" 

	if args.md_cat is not False:		
		metadata_doc_template = metadata_doc_template + """
		<field>
			<name>""" + args.md_cat + """</name>"""
		for cat in data['categories']: 
			metadata_doc_template = metadata_doc_template + """
			<value>""" + escape(cat) + """</value>"""
		metadata_doc_template = metadata_doc_template + """
		</field>"""

	metadata_doc_template = metadata_doc_template + """			
	</timespan>
</MetadataDocument>"""		
	
	#get the path of the XML sidecar
	this_filename = os.path.splitext(os.path.basename(item_path))[0]	
	out_file = os.path.abspath(args.temp_dir) + '/encodes/' + this_filename[:-5] + '.xml'	

	#create our xml sidecar
	try:
		f = open(out_file,'w')
		f.write(metadata_doc_template)
		f.close()
	except:
		print "Couldn't create xml sidecar"	

#form validation
check_vars()

#build our youtube-dl command
cmd = [args.youtubedl_path,'--write-info-json']
if args.limit != 0:
	cmd.append('--playlist-end')
	cmd.append(str(args.limit))	
cmd = cmd + ['-o',os.path.abspath(args.temp_dir) + '/%(title)s.%(ext)s']
cmd.append(args.yt_url)

#start downloading to our output directory and provide progress
p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
for line in iter(p.stdout.readline, b''):
    print(">>> " + line.rstrip())
p.wait()
if p.returncode != 0:
	print "There was an error with our downloads.  Exiting."
	exit(1)

#get all of our movie file paths
all_files = os.listdir(args.temp_dir)
for this_file in all_files:
	if this_file.endswith('.info.json'):
		parse_item(os.path.abspath(args.temp_dir) + "/" + this_file)
	elif this_file.endswith('.mp4') or this_file.endswith('.mkv') or this_file.endswith('.webm'):
		encode_item(os.path.abspath(args.temp_dir) + "/" + this_file)
	elif this_file == 'encodes':
		pass
	else:
		print this_file + " is being ignored"

#move all our items into portal storages and clean up afterwards
if not os.path.exists(os.path.abspath(args.temp_dir) + '/not_processed'):
	os.makedirs(os.path.abspath(args.temp_dir) + '/not_processed')

ready_to_move = os.listdir(args.temp_dir + "/encodes")
for this_file in ready_to_move:
	source = os.path.abspath(args.temp_dir) + "/encodes/" + this_file
	dest = os.path.abspath(args.storage) + "/" + this_file
	print "Moving " + source + " to " + dest
	try:
		os.rename(source,dest)
	except:
		os.rename(source,os.path.abspath(args.temp_dir) + '/not_processed/' + this_file)
		print "Could not move " + source
	all_files = os.listdir(args.temp_dir)
	for this_file in all_files:
		if this_file == 'not_processed':
			pass
		elif this_file == 'encodes':
			pass
		else:
			print this_file + " is being deleted"
			try:
				os.remove(os.path.abspath(args.temp_dir) + '/' + this_file)
			except:
				print "Could not remove " + os.path.abspath(args.temp_dir) + '/' + this_file
