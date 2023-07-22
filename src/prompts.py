
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
My task is to find information on Business Simulation and What If analyses. I'm interested in knowing the main providers and their products, scientific publications, and key individuals in this field.
To complete my task, the following are the steps I need to follow:
* Step 1: Conduct a search for business simulation providers using a search engine.
* Step 2: Identify the most promising results and visit the websites. Compile a list of providers and their products. 
* Step 3: Conduct another search for scientific publications related to Business Simulation and What If analyses. 
* Step 4: Identify the most cited or recognized publications and the authors involved.
* Step 5: Write down all the information acquired and finish the task. 

END NOTES

I will start my task by searching for business simulation providers. GET('https://www.google.com/search?q=business+simulation+providers')
"""
    if content is not None and len(content) > 0:
        content_formatted = f"""The content from your previous search is: {content}"""
        steps_formatted = "Considering the notes and the content from your previous search, you will now write your notes using the START NOTES ... END NOTES notation. Note that you need to write your notes again, even if you have already written them in your previous search. Then you have two options. If you still have things to do to complete your task conduct a new search using the GET('enter your url here') notation. If you have completed your task or you realize that you are unable to complete your task you will stop the multi-turn interaction system by typing FINISH."
        example = """START NOTES
My task is to find information on Business Simulation and What If analyses. I'm interested in knowing the main providers and their products, scientific publications, and key individuals in this field.

To complete my task, the following are the steps I need to follow:

* Step 1: Conduct a search for business simulation providers using a search engine. [Completed]
* Step 2: Identify the most promising results and visit the websites. Compile a list of providers and their products. [Completed]
* Step 3: Conduct another search for scientific publications related to Business Simulation and What If analyses. [Completed]
* Step 4: Identify the most cited or recognized publications and the authors involved.[Next Step]
* Step 5: Write down all the information acquired and finish the task.

From my previous searches, I found promising providers in the field of Business Simulation:

1. Cesim - A leading provider of multilingual, multidisciplinary business simulation games. [Website Link](https://www.cesim.com/)
2. Business Simulations - Covers a wide range of Leadership Topics including; Change Management, Commercial Acumen & Business Strategy. [Website Link](https://businesssimulations.com/)
3. SimulationStudios - Provides an engaging, hands-on business simulation that addresses leadership, strategic thinking, business acumen, innovation, and more. [Website Link](https://simulationstudios.com/)
4. IndustryMasters - Creates digital business simulations that develop business acumen and leadership skills. [Website Link](https://www.industrymasters.com/)
5. Capsim - Provide immersive, hands-on learning experiences for developing essential skills in business leaders. [Website Link](https://www.capsim.com/)
6. Celemi - Uses interactive business simulations to move people and organizations to higher levels of performance. [Website Link](https://celemi.com/)

Looking at the results from my previous search, several relevant scientific publications relating to Business Simulation and What If analyses, and their respective URLs stand out:

1. "What-if Simulation Modeling in Business Intelligence" - [ResearchGate](https://www.google.com/url?q=https://www.researchgate.net/publication/220613754_What-if_Simulation_Modeling_in_Business_Intelligence&sa=U&ved=2ahUKEwiut6W2lqCAAxUB-DgGHUxQB5MQFnoECAoQAg&usg=AOvVaw1NWAVWypokUQcBd5vhC_UJ). This article analyzes the impact of What-if Simulation in the context of business intelligence.
2. "Simulation-based analytics: A systematic literature review" - [ScienceDirect](https://www.google.com/url?q=https://www.sciencedirect.com/science/article/abs/pii/S1569190X22000211&sa=U&ved=2ahUKEwiut6W2lqCAAxUB-DgGHUxQB5MQFnoECAYQAg&usg=AOvVaw3RnJoTrK8bdA9nz65tg-LG). This scholarly article reviews the existing literature on simulation-based analytics in Business Analytics.
3. "Developing and validating a business simulation systems success" - [ScienceDirect](https://www.google.com/url?q=https://www.sciencedirect.com/science/article/pii/S1472811722000362&sa=U&ved=2ahUKEwiut6W2lqCAAxUB-DgGHUxQB5MQFnoECAIQAg&usg=AOvVaw2_ZNV8cYCK4kdgDTVYAeLa). This study shows how a business simulation systems success model was developed and validated.
4. "An Analysis of Influence of Business Simulation Games on Business" - [SAGE Journals](https://www.google.com/url?q=https://journals.sagepub.com/doi/full/10.1177/0735633117746746&sa=U&ved=2ahUKEwiut6W2lqCAAxUB-DgGHUxQB5MQFnoECAUQAg&usg=AOvVaw3170sey-LCgFdfBZhAEQZk). This publication examines the impact of business simulation games in the business domain.
   
Next step is to visit these URLs to better understand the publications and identify key individuals related to the studies. After visiting these URLs, I will write down all the information acquired and finish the task.
END NOTES

GET('https://www.researchgate.net/publication/220613754_What-if_Simulation_Modeling_in_Business_Intelligence')"""

    prompt = f"""You are Research-gpt, a AI model involved in a multi-turn interaction system. You have been given a task by a human user, and you are trying to complete it. The task is: 

```{task}```

As an AI model, you do not have direct access to the internet. However, you can ask me to search the internet for you.
You give me a valid URL, and I will return the text of the webpage at that URL. Note that I will not return the text of any images or videos. Supported formats are HTML, JSON, PDF, plain text, json, Markdown, csv and many similar formats. Each time you conduct a search, you will receive the text of the webpage at the URL you provided. You can then use that text to complete your task. If you want to conduct a search with a search engine, use the URL of the search results page. E.g. if you want to search for the definition of the word 'cat' on Wikipedia, use the URL GET('https://www.google.com/search?q=cat+wikipedia') or GET('https://duckduckgo.com/?q=cat+wikipedia'). Please stick to the GET('enter your url here') format so that I can understand you. Note that if reasonable, you can conduct your searches in different languages. For example, you can use german search terms if you are researching a german topic. Make sure you note everything that might be relevant for your task.

I want you to use reliable and trustworthy sources, so that these sources could be used as references in a scientific context. I encurage you to use search engines but please note that search engines are not considered reliable sources. Use them to find sources. The best sources are official government websites, scientific papers, books and websites that have a good reputation and are fact checked.

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

For your understanding here is an example of how your answer should look like. The task in this case was ```Find all relevant information about the topic of Business Simulation and What If Analyses.
Identify the main providers and their products, scientific publications, and key individuals in this field.```
{example}
```

Now it's your turn. Complete your task step by step. Write your notes and then conduct a search, or finish your task.
If you finish your task you do not need to summarize your findings.
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

As an AI model, you did not have direct access to the internet. However, you could ask me to search the internet for you. You gave me a valid URL, and I returned the text of the webpage at that URL. Each time you conducted a search, you received the text of the webpage at the URL you provided. You could then use that text to complete your task. Every iteration you made notes that you can read now. You are now at the last step of the multi-turn interaction system. The loop of the multi-turn interaction system has ended. You now write a summary of your findings. Write this summary in Markdown. Use hyperlinks to reference the sources you used. Do not use footnotes. Do not describe the steps of you search if you do not have to. Just write down the results of your search and your sources. Use the most extensive way possible to write down your findings. Use reliable and trustworthy sources. Prefer sources that could be used as references in a scientific context. Search engines are not reliable sources.

The following is a list of all the responses you gave during the multi-turn interaction system. Include all the details that might be relevant: {past_responses_formatted}

Please write your summary as a well structured continuous text in Markdown.
Here is a template for your summary:
```
Introduction
- Describe the task you were given.
- Describe the context of the task and the background information the reader needs to understand the task.
Main Part
- Finding 1
  - Describe the finding.
    - Describe the source.
- Finding 2
    - Describe the finding.
    - Describe the source.
- Finding 3
    - Describe the finding.
    - Describe the source.
Conclusion
- Summarize your findings.
- Describe the implications of your findings.
- Describe the limitations of your findings.
- Describe the next steps that could be taken to further investigate the topic.
```
Of course you can deviate from this template if you want to. You can also add or remove sections or structure the entire text in a diffrent way if the task requires it. 

Write the summary.
"""
    return prompt