import pytube as p
import os, shutil

red, yel, rese = '\033[1;31m', '\033[93m', '\033[00m'
current = os.getcwd()
tempdir = current+"/.tmp"


if not(os.path.exists(tempdir)):
    os.mkdir(tempdir)
os.chdir(tempdir)


def bar(iteration, total, prefix='', suffix='', per=0, fill='█', typ=''):
    length = 25
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r[{typ}]|{bar}| {per}% {suffix}', end='\r')


def dlanim(stream, chunk, remaining):
    file_size = stream.filesize
    percent = round((100*(file_size-remaining))/file_size, 1)
    bar(int(percent), 100, prefix='', suffix='Downloaded',
        per=percent, typ=str(stream.type).upper())


def download(ln):
    print(yel+"\n[Video title] "+rese+yt.title+"\n")
    choose2 = int(input(
        '[1]Audio and video \n[2]Audio (FLAC)\n[3]Chosen file\n[4]Download Playlist (audio/flac)\n: '))
    video_list = p.query.StreamQuery(
        yt.streams.fmt_streams).filter(type="video").asc()
    audio_list = p.query.StreamQuery(
        yt.streams.fmt_streams).filter(type="audio").asc()
    if choose2 == 1:
        show(video_list)
        print(os.getcwd())
        os.system("ffmpeg -loglevel quiet -i '" + video_list[int(input('Input Index: '))].download(
            filename_prefix="video") + "' -i '" + audio_list[0].download(filename_prefix="audio") + f"' -c:v copy -c:a copy '{current}/" + yt.title + ".mp4'")
    if choose2 == 2:
        show(audio_list)
        os.system('ffmpeg -loglevel quiet -i "' + \
            audio_list[int(input('Input Index: '))].download(
                filename_prefix="flac") + '" -b:a 512k "{current}/' + yt.title + '.flac"')
    if choose2 == 3:
        show(yt.streams)
        yt.streams.fmt_streams[int(input('Input Index: '))].download(output_path=current)
    if choose2 == 4:
        playlist = p.Playlist(ln)
        for x in playlist.video_urls:
            try:
                ytu = p.YouTube(x, on_progress_callback = dlanim)
            except Exception:
                print("[ERROR]Couldn't download"+ytu.title)
                pass
            print('\n'+ytu.title)
            audio_listt = p.query.StreamQuery(ytu.streams.fmt_streams).filter(type="audio").asc()
            os.system('ffmpeg -loglevel quiet -i "' + \
            audio_listt[0].download(
                filename_prefix="flac") + f'" -b:a 512k "{current}/' + ytu.title + '.flac"')
            
def show(listl):
    c = 0
    for x in listl:
        cdc = str(x.codecs).strip('[').strip(']').replace('\'', '')
        print(f'\n=======================Option'+yel+f'[{format(c, "02d")}]'+rese+f'======================\nType : [{x.subtype}]'+yel+f' [{x.type}]'+rese+' || Resolution : '+yel+f'[{x.resolution}]\n'+rese+'Framerate : '+red+f'[{x.fps}]'+rese+'     || BitRate : '+yel+f'{round(int(x.bitrate)/1024,2)}kB/s\n'+rese+'Codec : '+red+f'[{cdc}]'+ rese)
        c=int(c)+1


while True:
    try:
        link = input('Link: ')
        yt=p.YouTube(link, on_progress_callback = dlanim)
        download(link)
        shutil.rmtree(tempdir)
        ex = input('\nExit?[Y/n]: ')
        if ex == 'y' or ex == "":
            print("\nExiting..")
            exit()
    except Exception as e:
        print(e,"\nExiting..")
        exit()
    except KeyboardInterrupt:
        print('\nExiting..')
        exit()
