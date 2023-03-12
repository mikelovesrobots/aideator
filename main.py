import argparse
import sys
import openai
import constants
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

def list_models_subcommand(args):
    try:
        response = openai.Model.list()
        model_names = [model.id for model in response.data]
        print('\n'.join(model_names))
        sys.exit(0)
    except openai.error.AuthenticationError:
        print("Incorrect OpenAI API key provided. To reconfigure, please run:")
        print("")
        print("  tai config")
        print("")
        sys.exit(1)

def generate_subcommand(args):
    try:
        completion = openai.ChatCompletion.create(model=args.model, messages=[
            {"role": "system", "content": "You are a helpful command-line program"},
            {"role": "user", "content": "Please generate 3 numbers. No punctuation necessary."},
            {"role": "assistant", "content": "1\n5\n8\n"},
            {"role": "user", "content": "Please generate 5 colors. No punctuation necessary."},
            {"role": "assistant", "content": "pink\nred\nyellow\nblue\npurple\n"},
            {"role": "user", "content": "Please generate 3 alphabet characters. No punctuation necessary."},
            {"role": "assistant", "content": "b\nc\nk\n"},
            {"role": "user", "content": f"Please generate {args.num} {args.topic}. No punctuation necessary."}
        ])
        print(completion.choices[0].message.content.strip())
        sys.exit(0)
    except openai.error.AuthenticationError:
        print("Incorrect OpenAI API key provided. To reconfigure, please run:")
        print("")
        print("  tai config")
        print("")
        sys.exit(1)

def config_subcommand(args):
    prompt_to_create_config_file()

def main():
    config = load_config_file()
    if config == None:
        prompt_to_create_config_file()
        exit(0)

    openai.api_key = config['secret_key']

    stdin = sys.stdin.read().strip() if not sys.stdin.isatty() else None

    parser = argparse.ArgumentParser(
        prog="tai",
        description='generate ideas or transform text with the power of ai')

    subparsers = parser.add_subparsers(title='Sub-commands', required=True)
    subparser1 = subparsers.add_parser('generate', help='Generate ')
    subparser1.add_argument('topic', nargs="?", type=str, default=stdin or '', help='topic (e.g., names for an ai transformation tool) also attempts to consume stdin if not provided')
    subparser1.add_argument('-n', '--num', type=int, default=5, help='number of items to generate')
    subparser1.add_argument('-m', '--model', type=str, default=constants.DEFAULT_MODEL, help='openai completion model, run list_models for full list')
    subparser1.set_defaults(func=generate_subcommand)

    subparser2 = subparsers.add_parser('list_models', help='List OpenAI models available')
    subparser2.set_defaults(func=list_models_subcommand)

    subparser3 = subparsers.add_parser('config', help='Blow away configuration and setup tai')
    subparser3.set_defaults(func=config_subcommand)
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
