import click
import argparse
import sys
import openai
from constants import DEFAULT_MODEL
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
    openai.api_key = load_config_file()['secret_key']
    completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": f"Please rewrite the following with corrected grammar and spelling, but otherwise, leave the text unchanged (no extra punctuation or commentary necessary).\n###\n{input_file.read()}\n"},
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)

@cli.command()
@click.argument('input_file', type=click.File('rt'))
@click.argument('output_file', type=click.File('wt'))
def chat(input_file, output_file):
    """Say anything to OpenAI's GPT3.5 model. Use this whenever one of the templates isn't doing it for you.
    
    \b
    INPUT_FILE should be an input filename or - for stdin.
    OUTPUT_FILE should be an output filename or - for stdout.
    """
    openai.api_key = load_config_file()['secret_key']

    completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": input_file.read()},
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
    openai.api_key = load_config_file()['secret_key']

    prompt = f"Please generate {what}"

    completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": prompt},
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)

@cli.command()
def models():
    """Returns openai model names you have access to"""

    openai.api_key = load_config_file()['secret_key']
    completion = openai.Model.list()
    print(completion.data)

@cli.command()
def summarize():
    """Returnsa available model names.
    """
    openai.api_key = load_config_file()['secret_key']

    content = f"Please write {length} summarizing the following text.\n###\n{input_file.read()}\n"
    completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": content },
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
    openai.api_key = load_config_file()['secret_key']

    content = f"Please analyze the written text and determine the reading difficulty of the content, then provide suggestions on how to make the text more digestible. Which audience is likely being targeted?\n###\n{input_file.read()}\n"
    completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=[
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
    openai.api_key = load_config_file()['secret_key']

    prompt = "Please rewrite the following"
    if audience:
        prompt += f' for a {audience} audience'
    if style:
        prompt += f' in the style of {style}'
    if goal:
        prompt += f' with a goal of {goal}'

    completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=[
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
    openai.api_key = load_config_file()['secret_key']

    content = f"Please describe the sentiment of the following text. Which parts are positive? Which parts are negative? What's the intensity?\n###\n{input_file.read()}\n"
    completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=[
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
    openai.api_key = load_config_file()['secret_key']

    content = f"Please write {length} summarizing the following text.\n###\n{input_file.read()}\n"
    completion = openai.ChatCompletion.create(model=DEFAULT_MODEL, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": content },
    ])
    
    result = completion.choices[0].message.content
    output_file.write(result)

@cli.command()
@click.argument('job_listing_file', type=click.File('rt'))
@click.argument('resume_file', type=click.File('rt'))
@click.argument('output_file', type=click.File('wt'))
@click.option('-m', '--model', type=str, default=DEFAULT_MODEL, show_default=True, help="model id")
def candidate_check(job_listing_file, resume_file, output_file, model):
    """Review a candidate's resume for fit against a job listing. On a scale of -10 to 10, is this job a good fit for the candidate?
    
    \b
    JOB_LISTING_FILE should be an input text filename or - for stdin.
    RESUME_FILE should be a resume textfile's filename or - for stdin.
    OUTPUT_FILE should be an output filename or - for stdout.
    """
    openai.api_key = load_config_file()['secret_key']

    content = f"""
    Given the following job listing summary and then following candidate summary, please rate the fit of the candidate on a scale 
    of -10 to 10 with -10 being a poor fit, and 10 being a perfect fit for the job. Note that an underqualified or barely qualified
    candidate would not be a particularly good fit, so please be somewhat critical. If the job listing lists certain advanced
    technical skills as required and the candidate does not have those skills, that would indicate a very poor fit too. Also please 
    respond in json with an object containing a fit property containing your fit score, a reason property
    explaining why you chose that score, a underqualified boolean that indicates if they're underqualified, and an overqualified
    boolean that indicates if they're overqualified .
    ###
    [JOB LISTING]
    {job_listing_file.read()}
    ###
    [CANDIDATE RESUME]
    {resume_file.read()}
    """

    completion = openai.ChatCompletion.create(model=model, messages=[
        {"role": "system", "content": "You are a helpful and no-nonsense command-line program."},
        {"role": "user", "content": content },
    ], temperature=0)
    
    result = completion.choices[0].message.content
    output_file.write(result)
    output_file.write("\n")

def main():
    try:
        cli()
    except NoConfigException:
        if sys.argv[1] == 'configure':
            configure()
            sys.exit(0)

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

if __name__ == '__main__':
    main()
