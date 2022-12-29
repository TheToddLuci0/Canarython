import gpg
import argparse
import feedparser
from datetime import datetime
import subprocess

VERSION = '0.0.1'
RSS_DEFAULTS = ['http://rss.cnn.com/rss/cnn_topstories.rss',
'https://moxie.foxnews.com/google-publisher/latest.xml',
'http://feeds.bbci.co.uk/news/world/rss.xml',
'https://proton.me/blog/feed']

def generate_proofs(feeds:list, no_version=False):
    proof = """====================================
Current headlines as of {dt}:

""".format(dt=datetime.now().isoformat())
    for url in feeds:
        r = feedparser.parse(url)
        proof += "Latest from '{site}' ({url})\nLast Updated {t}\n".format(site=r['feed']['title'], url=url, t=r['feed']['updated'])
        for i in range(0,3):
            proof += "{}\n{}\n\n".format(r['entries'][i]['title'], r['entries'][i]['link'])
    proof += """====================================\n"""
    if no_version == False:
        proof += "Generated with canarython version {}\n".format(VERSION)
        try:
            sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
            proof += ("Commit {}\n".format(sha))
        except:
            pass
        proof += "===================================="
    return proof


def create_canary(message:str, key:str=None, nosha:bool=False, rss_feeds:list=None):
    proofs = generate_proofs(rss_feeds, nosha)
    if message[:-1] != '\n':
        message += '\n'
    message += proofs
    if type(message) != 'bytes':
        message = message.encode()
    c = gpg.Context()
    data, result = c.sign(message, mode=gpg.constants.sig.mode.CLEAR)
    return data.decode()
    

def main():
    parser = argparse.ArgumentParser(description="Generate GPG-signed \"Warrant Cannaries\"")
    parser.add_argument('--key', help="GPG key to use. Defaults to the default of the current user.")
    parser.add_argument('--no-sha', action="store_true", help="Do not include that commit signature of this program")
    parser.add_argument('--rss', action='append', default=RSS_DEFAULTS, help="RSS feed to use as proof of current time. Can be passed more than once")
    parser.add_argument('-m', '--message', help="Message to sign. Will prompt if not provided.")
    parser.add_argument('-o', '--output', help="File to write message to (default: STDOUT)")

    args = parser.parse_args()

    if not args.message:
        print("Type your message. Ctrl-D or a line containing only a '.' to end.")
        contents = []
        while True:
            try:
                line = input()
                if line == '.':
                    break
            except EOFError:
                break
            contents.append(line)
        args.message = contents
    canary = create_canary(message=args.message, key=args.key, nosha=args.no_sha, rss_feeds=args.rss)
    if args.output:
        with open(args.output, 'w') as f:
            f.write(canary)
        return ''
    else:
        return canary

if __name__ == '__main__':
    print(main())