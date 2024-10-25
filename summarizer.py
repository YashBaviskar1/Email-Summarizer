from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_email(email_text):
   #  prompt1 = "Summarize and Extract tasks only, prefixed with 'Task:', and exclude extra details."
   #  prompt2 = "Summarize the email in concise way, highlight only imoprtant points : "
   #  input_text = f"{prompt1} \n {email_text}"
    
    max_length = 150
    min_length = 80
    
    summary = summarizer(email_text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']



def extract_tasks_dynamic(email_text):

    sentences = email_text.split('.')
    tasks = []
    
    for sentence in sentences:
        if "task" in sentence.lower() or "include" in sentence.lower():
            tasks += [task.strip() for task in sentence.split(',')]
    
    # Clean up the task list by removing extra text
    tasks = [task for task in tasks if task] 
    return tasks

# print("/n/n/n")
# dynamic_tasks_list = extract_tasks_dynamic(summary)


# print("Dynamic Tasks to Complete:")
# for task in dynamic_tasks_list:
#     print(f"- {task}")
