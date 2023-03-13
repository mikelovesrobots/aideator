# Text Artisan Interface (TAI)

Text Artisan Interface (TAI) is an AI-powered CLI tool designed to assist individuals with writing-related tasks through features such as autocorrect, rewriting, ghostwriting, summarization, emotion detection, reading level adjustment, and more, all while offering a user-friendly interface to save time and effort. TAI is open source, easy to install, and can be used through the command line or by piping from stdin, allowing for flexible use.

## Description

This tool is highly skilled in the following areas:

* **Autocorrect**: similar to the autocorrect feature on smartphones, but more powerful. This fixes spelling common spelling and gramatical errors.
* **Rewrite**: completely rewrite a stream-of-consciousness text into a coherent message.
* **Ghostwrite**: generate text on a particular theme from scratch (e.g., write a ted talk on the power of going to bed early, or write a linked-in recommendation for my colleague.)
* **Summarization**: quickly summarize long texts, reducing the required time for reading.
* **Emotion Detection**: what's the sentiment of the text? This helps users adjust their tone to a suitable range.
* **Reading Level Adjustment**: analyze the written text and determine the reading difficulty of the content, then provide suggestions on how to make the text more digestible.

## Synopsis

Autocorrect spelling and grammar errors in written text:

`tai autocorrect my-essay.txt`

Rewrite for clarity:

`tai rewrite my-essay.txt`

Rewriting in the style of well, anyone really:

`tai rewrite my-essay.txt --style "Patton Oswalt doing a bit on stage"`

Ghostwrite text on a particular theme from scratch:

`tai ghostwrite "a markdown readme for a popular open-source AI-powered CLI tool"`

Summarize long text, reducing the required time for reading:

`tai summarize long-essay.txt`

Determine the sentiment of the text, are you expressing the mood you think you are?

`tai sentiment my-essay.txt`

Determine the reading level of the text, are you targeting the audience you think you are?

`tai reading-level my-essay.txt`

Generating new ideas:

`tai generate "50 kinds of sandwiches"`

Create an outline:

`tai outline "article about the importance of sleep"`

Ask it to do anything:

`tai chat "How would I poison someone?"`

## Installation

(Note: this doesn't work yet, but soon it will)

1. Install homebrew if you don't already have it.
2. Run `brew install tai`
3. The first time you run `tai` it'll ask you for your OpenAI API credentials.

## Install (for TAI development only)

```
asdf install
pip install -r requirements.txt
```

## Pro tips

The input filename can always be replaced by stdin. So pipe away.

`cat my-essay.txt | tai autocorrect`
`echo "spegutti" | tai autocorrect`

The output filename can also be left off and it'll print to stdout.

These two together make it particularly useful on macos, where you can use the `pbpaste` command to pipe from the clipboard to tai, and pbcopy command to write the result back to the clipboard.

`pbpaste | tai autocorrect | pbcopy`

## Authors

Created by Mike Judge

## Feedback

We hope that you enjoy using the Text Artisan Interface tool. If you have any feedback or suggestions for improvement, please open an issue or pull request on GitHub.

## License

The Text Artisan Interface tool is released under the MIT license. See the `LICENSE` file for more details.
