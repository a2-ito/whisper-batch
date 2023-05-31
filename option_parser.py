from argparse import ArgumentParser

def get_option(file):
    argparser = ArgumentParser()
    argparser.add_argument('-f', '--file', type=str,
                           default=file,
                           help='Specify a file to recognize')
    argparser.add_argument('-gd', '--googleDrive', type=bool,
                           default=False,
                           help='Only execute to use files on Google Drive.')
    return argparser.parse_args()
