import getpass
from argparse import ArgumentParser

from imgflip import __version__
from imgflip.api import Client


def parse_args():
    parser = ArgumentParser(prog='imgflip', description='Create memes with the api from Imgflip.')
    parser.add_argument('-V', '--version', action='version', version=__version__)

    subparsers = parser.add_subparsers(dest='action', description='memes caption')
    subparsers.add_parser('memes')
    parser_caption = subparsers.add_parser('caption')
    parser_caption.add_argument('-u', '--username', help='Username')
    parser_caption.add_argument('-p', '--password', help='Password')
    parser_caption.add_argument('-i', '--index', type=int, help='Meme index')
    parser_caption.add_argument('text', type=str, nargs='+', help='The text for the image')

    args = parser.parse_args()
    return args, parser


def main():
    args, parser = parse_args()
    client = Client()
    if args.action == 'memes':
        for i, meme in enumerate(client.get_memes()):
            print(i, meme['name'])
    elif args.action == 'caption':
        client.username = args.username or input('Username: ')
        client.password = args.password or getpass.getpass()
        index = args.index or int(input('Index: '))
        image = client.caption_image(index=index, text0=args.text[0], text1=args.text[1])
        image.webbrowser()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
