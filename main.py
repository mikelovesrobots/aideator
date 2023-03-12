import argparse
import os
import json
import sys
from config import load_config_file, write_config_file

def prompt_to_create_config_file():
    print("Welcome to tai (text artisan interface)!")
    print("")
    print("It looks like this is your first time running tai, and we couldn't find a configuration file.")
    print("")
    print("In order to use tai, you'll need an OpenAI API key. If you don't already have one, you can sign up for one at https://platform.openai.com/account/api-keys")
    print("")
    print("Once you have your API key, please enter it below:")
    print("")
    print("API Key: ", end='')

    secret_key = input().strip()
    write_config_file(secret_key)

    print("Great! We've written a configuration file to ~/.tai so you don't have to enter your API key every time you use tai.")
    print("")
    print("You're all set up and ready to go! Here are a few example commands you can try:")
    print("")
    print("  tai generate \"10 names for a French swashbuckler\"")
    print("  tai names \"French swashbuckler\"")
    print("  cat 'goblin dork soda' | tai transform \"sort alphabetically\"")
    print("")
    print("Have fun exploring tai!")

def generate_subcommand(args):
    print(args)

def main():
    config = load_config_file()
    if config == None:
        prompt_to_create_config_file()
        exit(0)

    stdin = sys.stdin.read().strip() if not sys.stdin.isatty() else None

    parser = argparse.ArgumentParser(
        prog="tai",
        description='generate ideas or transform text with the power of ai')

    subparsers = parser.add_subparsers(title='Sub-commands', required=True)
    subparser1 = subparsers.add_parser('generate', help='Generate ')
    subparser1.add_argument('topic', nargs="?", type=str, default=stdin or '', help='topic (e.g., names for an ai transformation tool)')
    subparser1.set_defaults(func=generate_subcommand)
    # parser.add_argument('-c', '--config', type=config_file_exists, help='path to config file', default=CONFIG_FILE_PATH)
    # parser.add_argument('-g', '--generate', type=str, help='Argument 1')
    # parser.add_argument('-b', '--arg2', type=int, help='Argument 2', default=1)
    
    # subparsers = parser.add_subparsers(title='Sub-commands', required=True)
    # subparser1 = subparsers.add_parser('config', help='Setup ~/.aideator json config')
    # subparser1.set_defaults(func=config)
    # subparser1.add_argument('-c', '--arg3', type=str, help='Argument 3')
    # subparser1.add_argument('-d', '--arg4', type=int, help='Argument 4', default=2)

    # subparser2 = subparsers.add_parser('command2', help='Command 2 help message')
    # subparser2.add_argument('-e', '--arg5', type=str, help='Argument 5')
    # subparser2.add_argument('-f', '--arg6', type=int, help='Argument 6', default=3)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
