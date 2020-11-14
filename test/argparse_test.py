
# from: https://stackoverflow.com/questions/17909294/python-argparse-mutual-exclusive-group

import argparse


if __name__ == '__main__':
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('--foo', action='store_true', help='help for foo arg.')
    subparsers = parser.add_subparsers(help='help for subcommand')

    # create the parser for the "command_1" command
    parser_a = subparsers.add_parser('command_1', help='command_1 help')
    parser_a.add_argument('a', type=str, help='help for bar, positional')

    # create the parser for the "command_2" command
    parser_b = subparsers.add_parser('command_2', help='help for command_2')
    parser_b.add_argument('-b', type=str, help='help for b')
    parser_b.add_argument('-c', type=str, action='store', default='', help='test')