from subprocess import Popen, PIPE
from collections import namedtuple

from youtube_dl.YoutubeDL import YoutubeDL

__all__ = ('YoutubeFormat',)

__InternalYoutubeFormat = namedtuple('YoutubeVideoFormat', ['video_id', 'id', 'name', 'dimensions', 'resolution', 'rest'])

class YoutubeFormat(__InternalYoutubeFormat):
    def is_best(self):
        return self.rest.endswith('(best)')


def youtube_url_by_video_id(video_id):
    return f'https://www.youtube.com/watch?v={video_id}'


def youtube_list_formats_by_video_id(video_id):
    video_url = youtube_url_by_video_id(video_id)

    ydl_proc = Popen(['youtube-dl', '--simulate', '--list-formats', video_url], stdout=PIPE)
    ydl_grep_proc = Popen(['grep', '-E', '[[:digit:]]+p'], stdin=ydl_proc.stdout, stdout=PIPE)

    ydl_proc.stdout.close()

    output = ydl_grep_proc.communicate()[0]

    return [
        YoutubeFormat(video_id, *row.split(None, 4))
        for row in output.decode().split('\n')
        if row
    ]


def youtube_stream_url_by_format(video_format):
    video_url = youtube_url_by_video_id(video_format.video_id)

    ydl_proc = Popen(['youtube-dl', '--get-url', '--format', video_format.id, video_url], stdout=PIPE)

    output = ydl_proc.communicate()[0]

    return output.decode()
