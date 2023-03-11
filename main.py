import argparse
import os
import json
import sys

VERSION = 0.1

home_dir = os.path.expanduser("~")
config_file_path = os.path.join(home_dir, ".aideate")

def write_config_file(secret_key):
    config = {"version": VERSION, "secret_key": secret_key}

    with open(config_file_path, "w") as outfile:
        json.dump(config, outfile)

def load_config_file():
    if not os.path.exists(config_file_path):
        return None
    with open(config_file_path, "r") as f:
        return json.load(f)

def prompt_to_create_config_file():
    print("Welcome to AIdeate!")
    print("")
    print("It looks like this is your first time running AIdeate, and we couldn't find a configuration file.")
    print("")
    print("In order to use AIdeate, you'll need an OpenAI API key. If you don't already have one, you can sign up for one at https://platform.openai.com/account/api-keys")
    print("")
    print("Once you have your API key, please enter it below:")
    print("")
    print("API Key: ", end='')

    secret_key = input().strip()
    write_config_file(secret_key)

    print("Great! We've written a configuration file to ~/.aideate so you don't have to enter your API key every time you use AIdeate.")
    print("")
    print("You're all set up and ready to go! Here are a few example commands you can try:")
    print("")
    print("  aideate generate \"10 names for a French swashbuckler\"")
    print("  aideate names \"French swashbuckler\"")
    print("  cat 'goblin dork soda' | aideate transform \"sort alphabetically\"")
    print("")
    print("Have fun exploring AIdeate!")

def main():
    config = load_config_file()
    if config == None:
        prompt_to_create_config_file()
        exit(0)

    parser = argparse.ArgumentParser(
        prog="aideator",
        description='generate ideas or transform text with the power of ai')
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
    # if args['func']:
    #     args.func(args)
    # else:
        
    #args.func(args)

    # # Use the arguments
    # # print(args.arg1)
    # # print(args.arg2)
    # if args.subparser_name == 'config':
    #     print("we're in config")
    #     # print(args.arg3)
    #     # print(args.arg4)
    # elif args.subparser_name == 'command2':
    #     print("we're in command2")
    #     # print(args.arg5)
    #     # print(args.arg6)

if __name__ == '__main__':
    main()
