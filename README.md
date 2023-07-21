# Research-GPT: An Iterative Search Assistant

This repository contains one of my experiments with OpenAI's GPT-4. The assistant is supposed to perform complex tasks requiring multi-stage execution, including web searches and subsequent information analysis.

## Capabilities

This assistant efficiently processes a variety of data types like HTML, JSON, PDF, plain text, markdown, and others.

## Examples

There is a [Jupyter Notebook with examples](https://github.com/nikohass/research-gpt/blob/main/examples.ipynb).
Some of the example prompts are:
- Look up the current president of the United States and write a short biography about him or her.
  Then look up the current chancellor of Germany and write a short biography about him or her.
  Have both ever met? If so, when and where?
- Analysiere die aktuelle Marktsituation vom DAX und vergleiche sie mit der Marktsituation vom Dow Jones.
- Analyze the news reporting on the current situation in the Ukraine. Search for russian soures in russian language and compare them to german sources in german language.

## How it works

The Iterative Search Assistant is designed around GPT-4, utilizing its advanced language comprehension abilities to perform intricate tasks that involve multi-stage processes, including internet searching and acquired information interpretation.

The assistant functions in a loop, following these steps:

1. Accepts a task from the user.
2. Makes annotations regarding the task and the necessary steps for its completion.
3. Initiates a web search by submitting a URL.
4. Retrieves the text content from the provided URL.
5. Analyzes the retrieved content, updates its notes, and decides the next course of action. This could be conducting another search or concluding the task if all the required information is gathered.
6. Upon deciding to conclude the search, it generates a comprehensive summary of its findings.

## Limitations and Considerations

The assistant requires the GPT-4 32k token model for webpage comprehension. However, there is a current limitation where the model is incapable of processing the content from very large websites. If the content is too vast, it gets truncated.
The program still makes mistakes like assuming it's the year 2021 or stopping before having completed the entire task.
