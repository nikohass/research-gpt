
def create_iterative_search_prompt(
        task: str,
        past_searches: list,
        notes: str,
        content: str,
) -> str:  
    past_searches_prompt = "You have not conducted any searches yet. Depending on your task, you may need to conduct a search."
    if len(past_searches) > 0:
        past_searches_formatted = ', '.join(past_searches)
        past_searches_prompt = f"""So far have conducted {len(past_searches)} search{'es' if len(past_searches) != 1 else ''}. Your past searches in chronological order are: {past_searches_formatted}"""
    
    notes_formatted = "You have not written any notes yet."
    if notes is not None and len(notes) > 0:
        notes_formatted = f"""Your notes are: {notes}"""

    content_formatted = "There is no content from previous searches yet."
    steps_formatted = "This is the first call of the multi-turn interaction system. You will first wite your notes using the START NOTES ... END NOTES notation. Note the steps you need to complete to finish your task. You may also note your thoughts. Then conduct your first search using the GET('enter your url here') notation."
    example = """START NOTES
My task is to look up the top 20 companies in the S&P 500.
To complete my task I have to do the following:
* Step 1: Conduct a search for the S&P 500 using a search engine.
* Step 2: Pick the most promising result and visit the website.
* Step 3: Find the list of the top 20 S&P 500 companies. If there is no such list, I will either have to look for it on a different website or a subpage of the website I am currently on.
* Step 4: Write down the list of the top 20 S&P 500 companies and finish my task by typing FINISH.
END NOTES
I will start with the search for the S&P 500 using Google. GET('https://www.google.com/search?q=s%26p+500')
"""
    if content is not None and len(content) > 0:
        content_formatted = f"""The content from your previous search is: {content}"""
        steps_formatted = "Considering the notes and the content from your previous search, you will now write your notes using the START NOTES ... END NOTES notation. Note that you need to write your notes again, even if you have already written them in your previous search. Then you have two options. If you still have things to do to complete your task conduct a new search using the GET('enter your url here') notation. If you have completed your task or you realize that you are unable to complete your task you will stop the multi-turn interaction system by typing FINISH."
        example = """START NOTES
My task is to look up the top 20 companies in the S&P 500.
To complete my task I have to do the following:
* Step 1: Conduct a search for the S&P 500 using a search engine.
* Step 2: Pick the most promising result and visit the website.
* Step 3: Find the list of the top 20 S&P 500 companies. If there is no such list, I will either have to look for it on a different website or a subpage of the website I am currently on.
* Step 4: Write down the list of the top 20 S&P 500 companies and finish my task by typing FINISH.
I have already completed step 1. The most promising results in chronological order are:
* https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
* https://www.slickcharts.com/sp500
* https://www.investopedia.com/ask/answers/08/find-stocks-in-sp500.asp
* https://markets.businessinsider.com/index/components/s&p_500
END NOTES

Based on the contend I found in my previous search, I will now open the most promising search result. GET('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')"""

    prompt = f"""You are an AI model involved in a multi-turn interaction system. You have been given a task by a human user, and you are trying to complete it. The task is: 

```{task}```

As an AI model, you do not have direct access to the internet. However, you can ask me to search the internet for you.
You give me a valid URL, and I will return the text of the webpage at that URL. Note that I will not return the text of any images or videos. Supported formats are HTML, JSON, PDF, plain text, json, Markdown, and similar formats. Each time you conduct a search, you will receive the text of the webpage at the URL you provided. You can then use that text to complete your task. If you want to conduct a search with a search engine, use the URL of the search results page. E.g. if you want to search for the definition of the word 'cat' on Wikipedia, use the URL GET('https://www.google.com/search?q=cat+wikipedia') or GET('https://duckduckgo.com/?q=cat+wikipedia'). Please stick to the GET('enter your url here') format so that I can understand you. Note that if reasonable, you can conduct your searches in different languages. For example, you can use german search terms if you are researching a german topic. I want you to use reliable and trustworthy sources, so that these sources could be used as references in a scientific context. I encurage you to use search engines but please note that search engines are not considered reliable sources. Use them to find sources. The best sources are official government websites, scientific papers, books and websites that have a good reputation and are fact checked.

Inside the multi-turn interaction system, there can be multiple searches. But you will only be able to see the results of the most recent search and conduct a new search. You will not be able to see the results of previous searches. {past_searches_prompt}. Do not search for the same thing twice.

Of course you need to remember what you found out in your previous searches. That's why you have the ability to make notes. I will give you your notes again the next time so that you can continue from where you left of. You can write down anything you want in your notes. For example URLs that sound promising or that you want to visit, or the results of your previous searches, or a todo list of steps you have to complete to finish your task. You can also note your sources there. Write down any information that you found that is somehow related to your task. Keep everything that might be relevant to not foreget it. You can write as many notes or entire paragraphs of text in your notes. You can write down anything you want. For readability, please type START NOTES before your notes and END NOTES after your notes. For example:
```
START NOTES
I have to look up the definition of the word 'cat' on Wikipedia. I will use the following steps to complete my task:
* Step 1: Conduct a search for the word 'cat' on Google.
* Step 2: Pick the most promising result and visit the website.
* Step 3: Find the definition of the word 'cat' on the website.
* Step 4: Write down the definition of the word 'cat' and finish my task by typing FINISH.

(Write further notes here.)

END NOTES

{notes_formatted}

{content_formatted}

To summarize: {steps_formatted}

For your understanding here is an example of how your answer should look like. Let's say you want to look up the top 20 companies in the S&P 500. You would write:
{example}
```

Now it's your turn. Please write your notes, conduct a search, or finish your task.
"""
    return prompt
"""
print(create_iterative_search_prompt(
    "Identify key studies and their findings, and discuss potential implications for public health policy.",
    [],
    "",
    ""
))"""

def create_summary_prompt(
        task: str,
        past_responses: list,
) -> str:
    past_responses_formatted = "\n\n".join(past_responses)
    prompt = f"""You are an AI model involved in a multi-turn interaction system. Previously, you were given a task by a human user, and you were trying to complete it. The task was: 

```{task}```

As an AI model, you did not have direct access to the internet. However, you could ask me to search the internet for you. You gave me a valid URL, and I returned the text of the webpage at that URL. Note that I did not return the text of any images or videos. Supported formats are HTML, JSON, PDF, plain text, json, Markdown, and similar formats. Each time you conducted a search, you received the text of the webpage at the URL you provided. You could then use that text to complete your task. Every iteration you made notes that you can read now. You are now at the last step of the multi-turn interaction system. The loop of the multi-turn interaction system has ended. You now write a summary of your findings. Write this summary in Markdown. Use hyperlinks to reference the sources you used. Do not use footnotes. Do not describe the steps of you search if you do not have to. Just write down the results of your search and your sources. Use the most concise way possible to write down your findings. Use reliable and trustworthy sources. Prefer sources that could be used as references in a scientific context. Search engines are not reliable sources.

The following is a list of all the responses you gave during the multi-turn interaction system: {past_responses_formatted}

Please write your summary.
"""
    return prompt