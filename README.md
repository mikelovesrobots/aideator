# Text Artisan Interface (TAI)

The Text Artisan Interface (TAI) is a powerful AI-powered natural language processing tool that simplifies complex writing-related tasks. TAI's user-friendly command-line interface can fix grammatical and spelling errors, rewrite text for brevity, positivity, or an entirely different audience, offer reading level suggestions, summarize long texts quickly, detect emotions in texts, and create content on specific topics from scratch.

## Description

The TAI tool works well in the following areas:

* **Autocorrection**: Correct spelling and grammar automatically.
* **Rewrite**: Rewrite text for clarity, brevity, or other goals.
* **Ghostwrite**: Create new texts on specific themes from scratch.
* **Summarization**: Provide quick summaries of long texts.
* **Emotion Detection**: Analyze the text for sentiment.
* **Reading Level Detection**: Determine the text's target reading level and suggest changes for better readability.

## Synopsis

Some examples of how to use TAI:

Automatically correct grammatical, spelling errors:

`tai autocorrect my-essay.txt output.txt`

Rewrite for clarity:

`tai rewrite my-essay.txt output.txt`

Rewrite for brevity:

`tai rewrite my-essay.txt output.txt --goal "brevity"`

Rewrite for a fourth grade audience:

`tai rewrite my-essay.txt output.txt --audience "fourth graders"`

Rewriting in any style:

`tai rewrite my-essay.txt output.txt --style "Mitch Hedberg doing a bit on stage"`

Ghostwrite:

`tai ghostwrite "a markdown readme for a popular open-source AI-powered CLI tool" output.txt`

Summarize long documents:

`tai summarize long-essay.txt output.txt`

Summarize docs to just a project title:

`tai summarize README.md output.txt --length="project title"`

Determine the sentiment of the text:

`tai sentiment my-essay.txt output.txt`

Determine the reading level of the text:

`tai reading-level my-essay.txt output.txt`

Chat with OpenAI:

`tai chat my-prompt.txt output.txt`

## Dependencies

TAI relies on OpenAI's gpt-3.5-turbo model to function, and thus an OpenAI API key is necessary for use. Get an API key at: https://platform.openai.com/account/api-keys

As of writing, an account is free and comes with $18 of credit, which covers about 9,000 executions.

## Installation (macos)

To install TAI, follow these steps:


(Note: this doesn't work yet, but soon it will)

1. Install [homebrew](https://brew.sh/)
2. Run `brew install mikelovesrobots/tai/tai`
3. Get a [private key from OpenAI](https://platform.openai.com/account/api-keys)
3. Run `tai configure` and it will ask you to paste in your OpenAI credentials

## Development Installation

This is just if you want to work on the TAI software:

1. Run `asdf install`
2. Run `pip install -r requirements.txt`
3. Run the project via `python3 main.py` instead of `tai`

## Pro Tips

The input filename can always be replaced by stdin if you provide a dash character for the input filename.

`cat my-essay.txt | tai autocorrect - output.txt`

The output filename can be replaced by stdout if you provide a dash character for the output filename. Use this feature on macos to pipe clipboard contents to TAI and write the result back to the clipboard.

`pbpaste | tai autocorrect - - | pbcopy`

## Author

Created by Mike Judge

## Feedback

I hope that you enjoy using the Text Artisan Interface tool. If you have any feedback or suggestions for improvement, please open an issue or pull request on GitHub.

## License

The Text Artisan Interface tool is released under the MIT license. See the `LICENSE` file for more details.
