from prompts import create_iterative_search_prompt, create_summary_prompt
from llm import GPT
from lookup import lookup
import re

REQUEST_LIMIT = 15

def search_loop(task, model):
    past_searches = []
    notes = None
    content = None
    log = []
    responses = []
    for request_number in range(REQUEST_LIMIT):
        prompt = create_iterative_search_prompt(
            task,
            past_searches,
            notes,
            content
        )
        #print(prompt)
        log.append(prompt)

        for _ in range(4):
            try:
                response = model.get_response(prompt)
            except KeyError:
                print("Warning: The model returned an error. This should not happen. Retrying...")
                content = content[:len(content)//2] + "\nContent truncated due to error."
                prompt = create_iterative_search_prompt(
                    task,
                    past_searches,
                    notes,
                    content
                )
                continue
            break
        #print(response)
        log.append(response)
        responses.append(response)

        # Parse response
        notes_block = re.findall(r"START NOTES(.*?)END NOTES", response, re.DOTALL)
        if len(notes_block) == 0:
            print("Warning: The model did not write any notes. This should not happen.")
        elif len(notes_block) > 1:
            print("Warning: The model wrote multiple notes. This should not happen.")
        else:
            notes = notes_block[0].strip()

        get_searches = re.findall(r"GET\(['\"]?(.*?)['\"]?\)", response)
        if len(get_searches) > 0:
            # The model wants to conduct a search
            url = get_searches[0]
            past_searches.append(url)
            content = lookup(url)
            if len(get_searches) > 1:
                print("Warning: The model wants to conduct multiple searches. Only the first search will be conducted.")
        elif "FINISH" in response:
            break
        else:
            print("Warning: The model did not conduct a search and did not finish. This should not happen.")
    #print("The model has finished.")

    with open("out/log.txt", "w") as log_file:
        log_file.write("\n\n=========================\n\n".join(log))

    with open("out/reasoning.md", "w") as responses_file:
        responses_file.write("\n\n=========================\n\n".join(responses))

    return responses

def complete_task(task, model):
    responses = search_loop(task, model)
    summary_prompt = create_summary_prompt(task, responses)
    summary_response = model.get_response(summary_prompt)
    with open("out/summary.md", "w") as summary_file:
        summary_file.write(f"{task}\n\n{summary_response}\n\n")
    return summary_response

if __name__ == "__main__":
    model = GPT()
    task = "Search for the current President of the United States."
    responses = search_loop(task, model)
    summary_prompt = create_summary_prompt(task, responses)
    print(summary_prompt)
    summary_response = model.get_response(summary_prompt)
    print(summary_response)