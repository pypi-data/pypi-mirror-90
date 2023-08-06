import subprocess
from os.path import join, exists
import requests
from requests.exceptions import Timeout
from enum import IntEnum
from tempfile import gettempdir
import youtube_dl
import pafy


class StreamStatus(IntEnum):
    OK = 200
    DEAD = 404
    FORBIDDEN = 401
    ERROR = 500
    SLOW = 666  # evil
    UNKNOWN = 0


def check_stream(url, timeout=5, verbose=False):
    # verify is url is dead or alive
    # NOTE might be temporarily down but still valid
    try:
        s = requests.get(url, timeout=timeout).status_code
        if s == 200:
            if verbose:
                print("stream OK:", url, s)
            return StreamStatus.OK
        if s == 404:
            if verbose:
                print("stream DEAD:", url, s)
            return StreamStatus.DEAD
        elif str(s).startswith("4"):
            if verbose:
                print("stream FORBIDDEN:", url, s)
            return StreamStatus.FORBIDDEN
        if verbose:
            print("stream ?:", url, s)
    except Timeout as e:
        # error, either a 500 or timeout
        if verbose:
            print("stream SLOW:", url, str(e))
        return StreamStatus.SLOW
    except Exception as e:
        # error, usually a 500
        if verbose:
            print("stream ERROR:", url, str(e))
        return StreamStatus.ERROR
    return StreamStatus.UNKNOWN


def parse_m3u8(m3, verify=False, verbose=False):
    if m3.startswith("http"):
        content = requests.get(m3).content
        m3 = join(gettempdir(), "pyvod.m3u8")
        with open(m3, "wb") as f:
            f.write(content)
    with open(m3) as f:
        m3ustr = f.read().split("\n")
        m3ustr = [l for l in m3ustr if l.strip()]

    movies = []
    for idx, line in enumerate(m3ustr):
        if not line.strip():
            continue
        next_line = m3ustr[idx + 1] if idx + 1 < len(m3ustr) else None
        if not next_line:
            break
        if line.startswith("#EXTINF:"):
            data = {
                "stream": next_line
            }
            sections = line.replace("#EXTINF:", "").split(",")
            fields = sections[0].split("=")
            data["name"] = sections[1]
            data["aliases"] = sections[1:]

            k, val = None, None
            for idx, entry in enumerate(fields):
                if idx == 0:
                    if len(entry.split(" ")) == 1:
                        data["duration"] = entry
                    else:
                        data["duration"], k = entry.split(" ")
                    data["duration"] = float(data["duration"])
                else:
                    _ = entry.split(" ")
                    new_k = _[-1]
                    val = " ".join(_[:-1])

                    if val.startswith("\""):
                        val = val[1:].strip()
                    if val.endswith("\""):
                        val = val[:-1].strip()

                    if k and val:
                        data[k] = val
                        k, val = new_k, None
            if "identifier" not in data:
                data['identifier'] = data["name"].lower().strip().replace(" ",
                                                                          "_")
            movies.append(data)

    entries = {}
    for movie in movies:
        name = movie["name"]
        entries[movie['identifier']] = movie

        # verify is url is dead or alive
        if verify:
            # NOTE might be temporarily down but still valid
            # Either way seems to be a bad stream, very slow of server side
            # implementation errors
            stream = movie["stream"]
            if verbose:
                print("Checking stream:", name, stream)
            status = check_stream(stream, verbose=verbose)
            if not status == StreamStatus.OK:
                continue

    return entries


def ydl(url, name=None, download=False, to_mp3=True, output_folder=None,
        verbose=False, audio=False):
    if audio:
        ydl_opts = {
            "no_color": True,
            'quiet': not verbose,
            "requested_formats": "bestaudio[ext=m4a]"
        }
        # TODO proper format detection, meanwhile force mp3
        to_mp3 = True
        if to_mp3:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
    else:
        ydl_opts = {
            "no_color": True,
            'quiet': not verbose
        }
    if download:
        output_folder = output_folder or gettempdir()
        name = name or "%(title)s"
        ydl_opts['outtmpl'] = join(output_folder, name + '.%(ext)s')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=download)
        if 'entries' in result:
            # Can be a playlist or a list of videos
            video = result['entries'][0]
        else:
            # Just a video
            video = result
        if "url" in video:
            return video['url']
        # TODO ensure correct format selection
        streams = video["formats"]
        stream = streams[-1]["url"]
    if download:
        name = video["title"]
        if to_mp3:
            ext = "mp3"
        else:
            ext = video["ext"]
        return join(output_folder, name + '.' + ext)
    return stream


def url2stream(url, audio_only=False, download=False, to_mp3=True,
               output_folder=None):
    # skip direct streams
    if audio_only:
        exts = [".mp3", ".wav", ".ogg"]
    else:
        exts = [".mp3", ".mpeg", ".ogv", ".mp4", ".wav", ".ogg"]
    for ext in exts:
        if url.endswith(ext):
            if audio_only and ext != ".mp3":
                name = url.split("/")[-1]
                output_folder = output_folder or gettempdir()
                path = join(output_folder, name)
                with open(path, 'wb') as f:
                    f.write(requests.get(url).content)
                return convert_to_m3(path, output_folder)
            return url

    try:
        if audio_only:
            return get_audio_stream(url, download=download, to_mp3=to_mp3,
                                    output_folder=output_folder)
        return get_video_stream(url, download=download,
                                output_folder=output_folder)
    except Exception as e:
        pass
        # specific implementations can be added here
    return url


def get_youtube_audio_stream(url, name=None, download=False, to_mp3=True,
                             output_folder=None):
    stream = pafy.new(url).getbestaudio()
    if download:
        name = name or url.split("watch?v=")[-1].split("/")[-1]
        output_folder = output_folder or gettempdir()
        path = join(output_folder, name + "." + stream.extension)
        if not exists(path):
            stream.download(path)
        if to_mp3:
            mp3 = convert_to_m3(path, name, output_folder=output_folder)
            if mp3:
                return mp3
        return path
    return stream.url


def get_youtube_video_stream(url, name=None, download=False,
                             output_folder=None):
    stream = pafy.new(url).streams[0]
    if download:
        name = name or url.split("watch?v=")[-1].split("/")[-1]
        output_folder = output_folder or gettempdir()
        path = join(output_folder, name + "." + stream.extension)
        if not exists(path):
            stream.download(path)
        return path
    return stream.url


def get_audio_stream(url, download=False, to_mp3=True, output_folder=None):
    if "youtube." in url or "youtu.be" in url:
        return get_youtube_audio_stream(url, download=download, to_mp3=to_mp3,
                                        output_folder=output_folder)
    else:
        return ydl(url, audio=True, download=download, to_mp3=to_mp3,
                   output_folder=output_folder)


def get_video_stream(url, download=False, output_folder=None):
    if "youtube." in url or "youtu.be" in url:
        return get_youtube_video_stream(url, download=download,
                                        output_folder=output_folder)
    else:
        return ydl(url, audio=False, download=download,
                   output_folder=output_folder)


def convert_to_m3(path, name=None, output_folder=None):
    name = name or path.split("/")[-1]
    output_folder = output_folder or gettempdir()
    mp3 = join(output_folder, name.replace(".mp3", "") + ".mp3")
    if not exists(mp3):
        # convert file to mp3
        command = ["ffmpeg", "-n", "-i", path, "-acodec",
                   "libmp3lame",
                   "-ab", "128k", mp3]
        subprocess.call(command)
    if exists(mp3):
        return mp3
    return None

