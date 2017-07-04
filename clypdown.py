from clint.textui import progress
import requests
import json
import sys


def download(mp3_url, title):
    filename = "{}.mp3".format(title)
    print("[*] Saving file to {}".format(filename))
    try:
        r = requests.get(url=mp3_url, stream=True)
        with open(filename, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
                if chunk:
                    f.write(chunk)
                    f.flush()
    except Exception as e:
        print("[-] Something has gone horribly wrong! Please report on the github issue tracker with the following backtrace: \n{}".format(e))
    print("[*] Done!")


def get_mp3_url(url):
    content_id = url.replace("https://clyp.it/", "")
    try:
        r = requests.get(url="https://api.clyp.it/{}".format(content_id))
    except Exception as e:
        print("[-] Something has gone horribly wrong! Please report on the github issue tracker with the following backtrace: \n{}".format(e))
    fucking_json = json.loads(r.text)
    song_title = fucking_json['Title']
    mp3_url = fucking_json['Mp3Url']
    if fucking_json['Status'] == "DownloadDisabled":
        print("[i] Uploader has disabled downloading. Who fucking cares.")
    print("[*] Got song title: {}".format(song_title))
    print("[*] Got mp3 url: {}".format(mp3_url))
    return song_title, mp3_url


def main(args):
    if len(args) != 2:
        sys.exit("{} https://clyp.it/lolwat".format(args[0]))
    song_title, mp3_url = get_mp3_url(url=args[1])
    download(mp3_url=mp3_url, title=song_title)


if __name__ == "__main__":
    main(args=sys.argv)
