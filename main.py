import click
import argparse
import sys
import openai
import constants
from config import load_config_file, write_config_file, NoConfigException

@click.group()
def cli():
    pass

@cli.command()
@click.argument('input_file', type=click.File('rt'))
@click.argument('output_file', type=click.File('wt'))
def autocorrect(input_file, output_file):
    """This fixes common spelling and gramatical errors without changing the input text too much
    
    \b
    INPUT_FILE should be an input filename or - for stdin.
    OUTPUT_FILE should be an output filename or - for stdout.
    """
    completion = openai.ChatCompletion.create(model=constants.DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": f"Please rewrite the following with corrected grammar and spelling, but otherwise, leave the text unchanged (no extra punctuation or commentary necessary).\n###\n{input_file.read()}\n"},
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)

@cli.command()
def configure():
    """Prompts the user for an OpanAI API Key and writes it to ~/.tai
    
    Note: this is a semi-dangerous command as it blows away any previous configuration.
    """
    click.echo("Welcome to Text Artisan Interface (tai)!")
    click.echo("")
    click.echo("In order to use tai, you'll need an OpenAI API key. If you don't already have one, you can sign up for one at https://platform.openai.com/account/api-keys")
    click.echo("")
    click.echo("Once you have your API key, please enter it below:")
    click.echo("")

    secret_key = click.prompt("API key", type=str).strip()
    write_config_file(secret_key)

    click.echo("Great! We've written a configuration file to ~/.tai so you don't have to enter your API key every time you use tai.")
    click.echo("")
    click.echo("You're all set up and ready to go! Here are a few example commands you can try:")
    click.echo("")
    click.echo("  [examples]")
    click.echo("")
    click.echo("Have fun exploring tai!")

@cli.command()
@click.argument('what', type=str, required=True)
@click.argument('output_file', type=click.File('wt'))
def ghostwrite(what, output_file):
    """This ghostwrites text on a particular theme from scratch
    
    \b
    Examples:
      tai ghostwrite "a ted talk on the power to going to sleep early" article.txt
      tai ghostwrite "a joke with a twist ending on getting lost in the supermarket" -
      tai ghostwrite "an outline of an essay on how AI can be an assistive device for the neurodiverse" -

    \b
    WHAT should contain what you want to generate and on what topic. Some examples:
    * "an article on the five ideals of devops"
    * "a paragraph describing a dungeons and dragons barbarian raised by wolves"

    \b
    OUTPUT_FILE should be an output filename or - for stdout.
    """

    prompt = f"Please generate {what}"

    completion = openai.ChatCompletion.create(model=constants.DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": prompt},
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)

@cli.command()
@click.argument('input_file', type=click.File('rt'))
@click.argument('output_file', type=click.File('wt'))
def reading_level(input_file, output_file):
    """Describe the reading level of the text, are you targeting the audience you think you are?
    
    \b
    INPUT_FILE should be an input filename or - for stdin.
    OUTPUT_FILE should be an output filename or - for stdout.
    """
    content = f"Please analyze the written text and determine the reading difficulty of the content, then provide suggestions on how to make the text more digestible. Which audience is likely being targeted?\n###\n{input_file.read()}\n"
    completion = openai.ChatCompletion.create(model=constants.DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": content },
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)

@cli.command()
@click.argument('input_file', type=click.File('rt'))
@click.argument('output_file', type=click.File('wt'))
@click.option('-a', '--audience', type=str, default="business casual", show_default=True, help="audience of this rewrite")
@click.option('-g', '--goal', type=str, default="clearer and simpler", show_default=True, help="goal of this rewrite")
@click.option('-s', '--style', type=str, help="in the style of _____ (e.g., Patton Oswalt addressing an audience, Hemmingway)")
def rewrite(input_file, output_file, audience, goal, style):
    """This rewrites the sample text. It's a killer tool when you're stuck in a rewriting loop,
    never happy with how your writing is turning out.
    
    \b
    INPUT_FILE should be an input filename or - for stdin.
    OUTPUT_FILE should be an output filename or - for stdout.
    """

    prompt = "Please rewrite the following"
    if audience:
        prompt += f' for a {audience} audience'
    if style:
        prompt += f' in the style of {style}'
    if goal:
        prompt += f' with a goal of {goal}'

    completion = openai.ChatCompletion.create(model=constants.DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": f"{prompt}\n###\n{input_file.read()}"},
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)

@cli.command()
@click.argument('input_file', type=click.File('rt'))
@click.argument('output_file', type=click.File('wt'))
def sentiment(input_file, output_file):
    """Describe the sentiment of the text, are you expressing the mood you think you are?
    
    \b
    INPUT_FILE should be an input filename or - for stdin.
    OUTPUT_FILE should be an output filename or - for stdout.
    """
    content = f"Please describe the sentiment of the following text. Which parts are positive? Which parts are negative? What's the intensity?\n###\n{input_file.read()}\n"
    completion = openai.ChatCompletion.create(model=constants.DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": content },
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)

@cli.command()
@click.argument('input_file', type=click.File('rt'))
@click.argument('output_file', type=click.File('wt'))
@click.option('-l', '--length', type=str, default="one paragraph", show_default=True, help="length of the desired output (e.g., one paragraph)")
def summarize(input_file, output_file, length):
    """Summarize long text, reducing the required time for reading.
    
    \b
    INPUT_FILE should be an input filename or - for stdin.
    OUTPUT_FILE should be an output filename or - for stdout.
    """
    content = f"Please write {length} summarizing the following text.\n###\n{input_file.read()}\n"
    completion = openai.ChatCompletion.create(model=constants.DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": content },
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)


if __name__ == '__main__':
    try:
        openai.api_key = load_config_file()['secret_key']
        cli()
    except NoConfigException:
        click.echo("No config file found. It looks like this is your first time running tai.")
        click.echo("")
        click.echo("To configure the app, please run:")
        click.echo("")
        click.echo("  tai configure")
        click.echo("")
        sys.exit(1)
    except openai.error.AuthenticationError:
        click.echo("Incorrect OpenAI API key provided. To reconfigure, please run:")
        click.echo("")
        click.echo("  tai configure")
        click.echo("")
        sys.exit(1)

# def reconfigure_subcommand(args):
#     prompt_to_create_config_file()

# def list_models_subcommand(args):
#     try:
#         response = openai.Model.list()
#         model_names = [model.id for model in response.data]
#         print('\n'.join(model_names))
#         sys.exit(0)
#     except openai.error.AuthenticationError:
#         print("Incorrect OpenAI API key provided. To reconfigure, please run:")
#         print("")
#         print("  tai reconfigure")
#         print("")
#         sys.exit(1)

# def autocorrect_subcommand(args):
#     try:
#         if args.input_file is sys.stdin:
#             input_text = sys.stdin.read()
#         else:
#             with args.input_file as f:
#                 input_text = f.read()

#         print(input_text)
#         sys.exit(0)

#         completion = openai.ChatCompletion.create(model=args.model, messages=[
#             {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
#             {"role": "user", "content": f"Please rewrite the following with corrected grammar and spelling, but otherwise, leave the text unchanged (no extra punctuation or commentary necessary).\n###\n{input_text}\n"},
#         ])

#         result = completion.choices[0].message.content.strip()
#         args.output_file.write(result)
#         args.output_file.close()

#         sys.exit(0)
#     except openai.error.AuthenticationError:
#         print("Incorrect OpenAI API key provided. To reconfigure, please run:")
#         print("")
#         print("  tai reconfigure")
#         print("")
#         sys.exit(1)

# def generate_subcommand(args):
#     try:
#         completion = openai.ChatCompletion.create(model=args.model, messages=[
#             {"role": "system", "content": "You are a helpful command-line program"},
#             {"role": "user", "content": "Please generate 3 numbers. No punctuation necessary."},
#             {"role": "assistant", "content": "1\n5\n8\n"},
#             {"role": "user", "content": "Please generate 5 colors. No punctuation necessary."},
#             {"role": "assistant", "content": "pink\nred\nyellow\nblue\npurple\n"},
#             {"role": "user", "content": "Please generate 3 alphabet characters. No punctuation necessary."},
#             {"role": "assistant", "content": "b\nc\nk\n"},
#             {"role": "user", "content": f"Please generate {args.num} {args.topic}. No punctuation necessary."}
#         ])
#         print(completion.choices[0].message.content.strip())
#         sys.exit(0)
#     except openai.error.AuthenticationError:
#         print("Incorrect OpenAI API key provided. To reconfigure, please run:")
#         print("")
#         print("  tai reconfigure")
#         print("")
#         sys.exit(1)

# def rewrite_subcommand(args):
#     try:
#         completion = openai.ChatCompletion.create(model=args.model, messages=[
#             {"role": "system", "content": "You are a helpful grammar tool"},
#             {"role": "user", "content": f"Please rewrite the following to be {args.transformation}\n###\n{args.text}"}
#         ])
#         print(completion.choices[0].message.content.strip())
#         sys.exit(0)
#     except openai.error.AuthenticationError:
#         print("Incorrect OpenAI API key provided. To reconfigure, please run:")
#         print("")
#         print("  tai reconfigure")
#         print("")
#         sys.exit(1)

# def chat_subcommand(args):
#     try:
#         completion = openai.ChatCompletion.create(model=args.model, messages=[
#             {"role": "system", "content": "You are a helpful chatbot."},
#             {"role": "user", "content": args.text}
#         ])
#         print(completion.choices[0].message.content.strip())
#         sys.exit(0)
#     except openai.error.AuthenticationError:
#         print("Incorrect OpenAI API key provided. To reconfigure, please run:")
#         print("")
#         print("  tai reconfigure")
#         print("")
#         sys.exit(1)

# def reconfigure_subcommand(args):
#     prompt_to_create_config_file()


# def main():
#     config = load_config_file()
#     if config == None:
#         prompt_to_create_config_file()
#         exit(0)

#     openai.api_key = config['secret_key']

#     parser = argparse.ArgumentParser(
#         prog="tai",
#         description='generate ideas or transform text with the power of ai')

#     subparsers = parser.add_subparsers(title='Sub-commands', required=True)
    
#     autocorrect_subparser = subparsers.add_parser('autocorrect', help='Autocorrect spelling and grammar errors in written text')
#     autocorrect_subparser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='input file path (or will default to stdin)')
#     autocorrect_subparser.add_argument('output_file', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='output file path (or will default to stdout)')
#     autocorrect_subparser.add_argument('-m', '--model', type=str, default=constants.DEFAULT_MODEL, help='openai completion model, run list_models for full list')
#     autocorrect_subparser.set_defaults(func=autocorrect_subcommand)

#     list_models_subparser = subparsers.add_parser('list_models', help='List OpenAI models available')
#     list_models_subparser.set_defaults(func=list_models_subcommand)

#     reconfigure_subparser = subparsers.add_parser('reconfigure', help='Blow away configuration and re-setup tai')
#     reconfigure_subparser.set_defaults(func=reconfigure_subcommand)

#     # autocorrect_parser = subparsers.add_parser('autocorrect', help='Autocorrect spelling and grammar errors in written text')

#     # parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)


#     # ideate_parser = subparsers.add_parser('generate', help='Generate things')
#     # ideate_parser.add_argument('topic', nargs="?", type=str, default=stdin or '', help='topic (e.g., names for an ai transformation tool) also attempts to consume stdin if not provided')
#     # ideate_parser.add_argument('-n', '--num', type=int, default=5, help='number of items to generate')
#     # ideate_parser.add_argument('-m', '--model', type=str, default=constants.DEFAULT_MODEL, help='openai completion model, run list_models for full list')
#     # ideate_parser.set_defaults(func=generate_subcommand)

#     # rewrite_parser = subparsers.add_parser('rewrite', help='Rewrite text')
#     # rewrite_parser.add_argument('text', nargs="?", type=str, default=stdin or '', help='text to rewrite (tip: also attempts to consume stdin if not provided) so feel free to pipe text to it')
#     # rewrite_parser.add_argument('-t', '--transformation', type=str, default='clearer for a business casual audience', help='how to edit the text')
#     # rewrite_parser.add_argument('-m', '--model', type=str, default=constants.DEFAULT_MODEL, help='openai completion model, run list_models for full list')
#     # rewrite_parser.set_defaults(func=rewrite_subcommand)



#     # chat_parser = subparsers.add_parser('chat', help='Convenience method for just talking to chatgpt')
#     # chat_parser.add_argument('text', nargs="?", type=str, default=stdin or '', help='text to send to chatgpt')
#     # chat_parser.add_argument('-m', '--model', type=str, default=constants.DEFAULT_MODEL, help='openai completion model, run list_models for full list')
#     # chat_parser.set_defaults(func=chat_subcommand)
#     # parser.add_argument('-c', '--config', type=config_file_exists, help='path to config file', default=CONFIG_FILE_PATH)
#     # parser.add_argument('-g', '--generate', type=str, help='Argument 1')
#     # parser.add_argument('-b', '--arg2', type=int, help='Argument 2', default=1)
    
#     # subparsers = parser.add_subparsers(title='Sub-commands', required=True)
#     # subparser1 = subparsers.add_parser('config', help='Setup ~/.aideator json config')
#     # subparser1.set_defaults(func=config)
#     # subparser1.add_argument('-c', '--arg3', type=str, help='Argument 3')
#     # subparser1.add_argument('-d', '--arg4', type=int, help='Argument 4', default=2)

#     # subparser2 = subparsers.add_parser('command2', help='Command 2 help message')
#     # subparser2.add_argument('-e', '--arg5', type=str, help='Argument 5')
#     # subparser2.add_argument('-f', '--arg6', type=int, help='Argument 6', default=3)

#     args = parser.parse_args()
#     args.func(args)

# if __name__ == '__main__':
#     main()
