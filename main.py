#import telegram
import telebot
# import youtube_dl
# import ffmpeg
# import pytube
# import youtube_dl
# from gevent._socket2 import _fileobject
# from gevent.libev.corecext import callback
# from telebot import callback_data
# from youtube_dl.utils import DownloadError
# from youtube_transcript_api import YouTubeTranscriptApi
import pytube
import requests
import re
from urllib.request import urlretrieve
from os.path import exists, getsize
from instalooter.looters import *
from urllib.request import urlretrieve ,URLopener, urlopen, Request

from time import time, sleep
#import shutil
LIMIT_SIZE = 52428800
MY_CHAT_ID = 156956400
KEY = "5073344380:AAGu_vY4zRkfgkS_ZgI5vgFPXc31IFDGgPk"
bot = telebot.TeleBot(KEY)
basic_urls = ["https://www.youtube.com/watch?v=", "http://www.youtube.com/watch?v=", "http://www.m.youtube.com/watch?v=", "https://www.m.youtube.com/watch?v=", "https://youtube.com/shorts/" ,"https://youtu.be/"]
is_link = False
title = ''
TITLE = ''
size = 0
link =""
types = telebot.types
file = ''
apsurl = ''
spchars = ['\\', '/', ':', '*', "?", "'", "<", ">", "|", " "]
msid = ''
chid = ''
id = ''
isinsta = 0
multi_instagram = 0
code = ''
d_inst = ''
def downloadit(link, type, message):
    print("from downloadit")
    global file, msid, chid
    msid = message.message_id
    chid = message.chat.id

    if isinsta == 0:
        res = requests.get( link, stream=True )
        if res.status_code == 200:
            print( msid )
            ext = ".mp3" if type == "0" else ".mp4"
            file_name = f"{id}_{type}{ext}"
            print(file_name)
            urlretrieve(link, file_name, Handle_Progress)
            if type == '0':
                print(file_name)
                openf = open(file_name, 'rb')
                senddel = bot.send_message( message.chat.id,disable_notification=True,  text=f'Sending Audio {getrealsize(size)}')
                bot.send_document(  message.chat.id,  openf)
            if type == "1" or type == '2':
                print(file_name)
                openf = open(file_name, 'rb')
                senddel = bot.send_message( message.chat.id,disable_notification=True,  text=f'Sending Video{getrealsize(size)}')
                bot.send_video(message.chat.id,  openf,disable_notification=True)
            bot.delete_message(message.chat.id, senddel.id)
            print( ' sucessfully Downloaded: ', file_name )
            bot.delete_message(chid, msid)
            bot.send_message( message.chat.id,disable_notification=False,  text="Sended Successfully ✅")
    # else:  # it's instagram
    #     global code, d_inst
    #     if multi_instagram == 0:
    #         file_name = f"{code}_1.{type}"
    #         print(file_name)
    #         urlretrieve( apsurl, file_name, Handle_Progress )
    #         openf = open( file_name, 'rb' )
    #         print("after openf")
    #         if type == 'jpg':
    #             bot.send_photo( message.chat.id, openf )
    #         else:
    #             bot.send_video( message.chat.id, openf )
    #     else:
    #         print( "multi" )
    #         for n in range( len( link ) ):
    #             if int(link[n]['size']) > LIMIT_SIZE:
    #                 continue
    #             else:
    #                 file_name = f"{code}_{n}.{link[n]['type']}"
    #
    #                 openf = open( file_name, 'rb' )
    #                 if link[n]['type'] == 'jpg':
    #                     bot.send_photo( message.chat.id, openf )
    #                 else:
    #                     bot.send_video( message.chat.id, openf )
    #         bot.delete_message( message.chat.id, int( d_inst ) )
def getrealsize(n):
    if n >= 1024 and n <= 1048576:
        return f'{round( n / 1024, 2 )} KB'
    elif n >= 1048576 and n <= 1073741824:
        return f'{round( n / 1048576, 2 )} MB'
    elif n >= 1073741824 and n <= 1099511627776:
        return f'{round( n / 1073741824, 2 )} GB'
    elif n >= 1099511627776 and n <= 1125899906842624:
        return f'{round( n / 1099511627776, 2 )} TB'
    elif n == 0:
        return "0"
    else:
        return "file to big"
def mycb(total, recvd, ratio, rate, eta):
    print(f"{str( int( ratio * 100 ) )}%" )
    print( f'{getrealsize( recvd )}/{getrealsize( total )}' )

def link_checker(message):
    global link, is_link, LIMIT_SIZE, id, apsurl, isinsta, multi_instagram ,type, code, d_inst
    link = message.text

    bot.send_message(MY_CHAT_ID, f"trying{link}", disable_notification=True)
    bot.send_message(MY_CHAT_ID, str(message), disable_notification=True)
    print(link)
    if str(link).find("youtube.com") > -1 and str(link).find("watch?v=") > -1 or str(link).startswith(basic_urls[-1]) :
        id = pytube.streams.extract.video_id( link )
        getdel = bot.send_message( message.chat.id, 'Getting Informations 🔎' ).id

        print("yes")
        print( "Choose===>" )
        is_link = True
        Apsolute_url = pytube.YouTube( link )
        audio = Apsolute_url.streams.get_audio_only()
        lowvideo = Apsolute_url.streams.get_lowest_resolution()
        highvideo = Apsolute_url.streams.get_highest_resolution()
        keybourd = types.InlineKeyboardMarkup()
        audioOnly = types.InlineKeyboardButton(text=f"Audio Only {getrealsize(audio.filesize)}", callback_data="0")
        lowQuality = types.InlineKeyboardButton(text=f"Low Quality {getrealsize(lowvideo.filesize)}", callback_data='1')
        highQuality = types.InlineKeyboardButton(text=f"High Quality {getrealsize(highvideo.filesize)}", callback_data="2")
        toolarge = types.InlineKeyboardButton("Try another link", callback_data=-1)
        if audio.filesize < LIMIT_SIZE:
            keybourd.add(audioOnly)
        if lowvideo.filesize < LIMIT_SIZE:
            keybourd.add(lowQuality)
        if highvideo.filesize < LIMIT_SIZE:
            keybourd.add(highQuality)
        else:
            bot.send_message(message.chat.id, "File Too Large (50MB FILE LIMIT)")
            keybourd.add(toolarge)
        bot.send_message( message.chat.id,disable_notification=True,  text="Choose One:", reply_markup=keybourd)
        bot.delete_message(message.chat.id, getdel)
    # elif str(link).startswith('https://www.instagram.com/p/'):
    #     print("instagram")
    #     global d_inst
    #     isinsta = 1
    #     multi_instagram = 0
    #     d_inst = bot.send_message(message.chat.id, "Getting Informations from Instagram").id
    #     url = str(link).replace("tv/", 'p/')
    #     url = url[url.find( "p/" ) + 2:url.find( "/", url.find( "p/" ) + 2 )]
    #     code = url
    #     print(code)
    #     looter = ProfileLooter("valyria_downloader")
    #     post_info = looter.get_post_info(code)
    #     if "edge_sidecar_to_children" not in post_info:
    #         if 'video_url' in post_info:
    #             data_type = 'video_url'
    #             type = 'mp4'
    #         else:
    #             data_type = 'display_url'
    #             type = 'jpg'
    #         apsurl = post_info[data_type]
    #         print( apsurl )
    #         downloadit(apsurl, type, message)
    #     if "edge_sidecar_to_children" in post_info:
    #         multi_instagram = 1
    #         urls = {}
    #         for n in range( len( post_info['edge_sidecar_to_children']['edges'] ) ):
    #             if 'video_url' in post_info['edge_sidecar_to_children']['edges'][n]['node']:
    #                 if n == 0:
    #                     data_type = 'video_url'
    #                     type = 'mp4'
    #             else:
    #                 if n == 0:
    #                     data_type = 'display_url'
    #                     type = 'jpg'
    #             urls[n] = {}
    #             urls[n]['url'] = post_info['edge_sidecar_to_children']['edges'][n]['node'][
    #                 data_type]
    #             urls[n]['type'] = type
    #             urls[n]['size'] = urlopen( Request(
    #                 post_info['edge_sidecar_to_children']['edges'][n]['node'][data_type] ) ).info()[
    #                 'Content-Length']
    #         apsurl = urlopen(
    #             Request( post_info['edge_sidecar_to_children']['edges'][n]['node'][data_type] ) )
    #         print(urls)
    #         downloadit(urls, type='multi', message=message)
        # headers = apsurl.info()
        # if 'Content-Length' in headers:
        #     filesize = int( headers['Content-Length'] )
        # else:
        #     filesize = 0
    else:
        print(link)
        print("no")
        bot.send_message( message.chat.id,disable_notification=True,  text="Send Valid Link Only")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "use /download command to start download your videos")
@bot.message_handler(commands=['download'])
def download(message):
    link = bot.reply_to(message, "Send Your Link")
    bot.register_next_step_handler(link, link_checker)
    print("download")


def Handle_Progress(blocknum, blocksize, totalsize):
    global msid, chid, isinsta
    try:
        readed_data = blocknum * blocksize
        if totalsize > 0:
            #sleep( 0.1 )
            print( getrealsize( readed_data ), blocknum, getrealsize(size) )
            download_percentage = readed_data * 100 / totalsize
            #sleep(0.5)
            if blocknum % 75 == 0 and blocknum > 75 and isinsta == 0:
                bot.edit_message_text(
                    f"Downloading {round( download_percentage, 3 )}% | {getrealsize( readed_data )}/{getrealsize(size)}", chid,
                int(msid))
            if readed_data > totalsize:
                print( "Download Completed 100%" )
    except ConnectionResetError:
        bot.send_message( msid, "Download Error Check Your Internet Connection", disable_notification=False )
@bot.callback_query_handler( func=lambda call: True )
def callback_worker(call):
    print(call.data)
    global size, title, spchars, TITLE
    Apsolute_url = pytube.YouTube(link)
    pretitle = Apsolute_url.title
    title = ''
    for t in pretitle:
        if t not in spchars:
            title +=t
            TITLE +=t
    try:
        if call.data == "0":
            apslink = Apsolute_url.streams.get_audio_only().url
            size = Apsolute_url.streams.get_audio_only().filesize
            downloadit(apslink, '0', call.message)
        if call.data == '1':
            apslink = Apsolute_url.streams.get_lowest_resolution().url
            size = Apsolute_url.streams.get_lowest_resolution().filesize
            downloadit(apslink, '1', call.message)
        if call.data == '2':
            apslink = Apsolute_url.streams.get_highest_resolution().url
            size = Apsolute_url.streams.get_highest_resolution().filesize
            downloadit(apslink, '2', call.message)
        if call.data == '-1':
            download(call.message)
    except ConnectionResetError:
        bot.send_message(call.message.chat.id, 'Connection Error Try Again Later ❌')



bot.polling()
