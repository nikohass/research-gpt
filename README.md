# Research-GPT: An Iterative Search Assistant

This repository contains one of my experiments with OpenAI's GPT-4. The assistant is supposed to perform complex tasks requiring multi-stage execution, including web searches and subsequent information analysis.

## Examples

There is a [Jupyter Notebook with examples](https://github.com/nikohass/research-gpt/blob/main/examples.ipynb).

## Limitations and Considerations

The assistant requires the GPT-4 32k token model for webpage comprehension. However, there is a current limitation where the model is incapable of processing the content from very large websites. If the content is too vast, it gets truncated.
The program still makes mistakes like assuming it's the year 2021, stopping before having completed the entire task, or forgetting information.
