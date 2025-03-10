import gkeepapi
import time
from datetime import datetime
import pytz
from openai import OpenAI
import os

def printf(text):
    print(text, flush=True)

def init_keep():
    keep = gkeepapi.Keep()

    email = os.getenv("GKEEP_EMAIL")
    master_token = os.getenv("MASTER_TOKEN")

    try:
        success = keep.authenticate(email, master_token)
        printf("Login successful!")
    except gkeepapi.exception.LoginException as e:
        printf(f"Login failed: {e}")
        return None

    return keep

def query_notes_created_after(keep, timestamp):
    gnotes = keep.find(func=lambda x: not x.deleted and not x.archived and x.timestamps.created > timestamp)
    return gnotes

def parse_tasks(note):
    client = OpenAI(api_key=os.getenv("OPENAPI_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": "Collect tasks from the following text and list them, one task per line, in a following format: - [ ] task. If the task has a specific time, format them in the following format: - [ ] time task. Answer only with the list of tasks, or nothing if there are no tasks. The text to collect the tasks from:" + note}],
    )
    content = response.choices[0].message.content
    printf(f"Answer: {content}")
    return content

def get_note_content(note):
    return note.text

def print_note(note):
    printf(f"Title: {note.title}")
    printf(f"Content: {note.text}")
    printf(f"Color: {note.color}")
    printf(f"Pinned: {note.pinned}")
    printf(f"Archived: {note.archived}")
    printf(f"Created: {note.timestamps.created}")
    printf(f"Updated: {note.timestamps.updated}")
    printf("-" * 40)

def get_daily_note_file_or_create_from_template(template_file_path, folder) -> str:
    today_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today_date}.md"
    file_path = os.path.join(folder, filename)
    if os.path.exists(file_path):
        return file_path

    try:
        with open(template_file_path, "r") as template_file:
            template_content = template_file.read()
    except FileNotFoundError:
        printf(f"Template file '{template_file_path}' not found.")
        return None
    except Exception as e:
        printf(f"An error occurred while reading the template file: {e}")
        return None

    try:
        with open(file_path, "w") as new_file:
            new_file.write(template_content)
        printf(f"File '{filename}' created successfully in '{folder}'.")
        return file_path
    except Exception as e:
        printf(f"An error occurred while creating the file: {e}")
        return None
    
def insert_content_after_text(filepath, text, content):
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()

        text_line_index = -1
        for i, line in enumerate(lines):
            if text in line:
                text_line_index = i
                break

        if text_line_index == -1:
            printf(f"Text '{text}' not found in the file.")
            return

        empty_line_index = -1
        for i in range(text_line_index + 1, len(lines)):
            if lines[i].strip() == "":
                empty_line_index = i
                break

        if empty_line_index == -1:
            printf("No empty line found after the text.")
            return

        lines.insert(empty_line_index, content + "\n")
        with open(filepath, "w") as file:
            file.writelines(lines)
    except FileNotFoundError:
        printf(f"File '{filepath}' not found.")
    except Exception as e:
        printf(f"An error occurred: {e}")

def process_note_content(note_content):
    tasks = parse_tasks(note_content)
    path_to_daily_template=os.getenv("DAILY_TEMPLATE_PATH")
    daily_notes_folder=os.getenv("DAILY_NOTES_FOLDER")
    daily_note_file_path = get_daily_note_file_or_create_from_template(path_to_daily_template, daily_notes_folder)
    tasks_header=os.getenv("TASKS_HEADER")
    insert_content_after_text(daily_note_file_path, tasks_header, tasks)
    diary_header=os.getenv("DIARY_HEADER")
    insert_content_after_text(daily_note_file_path, diary_header, note_content)

def loop():
    tz = pytz.timezone('Europe/Vienna')
    keep = init_keep()
    timestamp = datetime.now(tz)

    while True:
        printf(f"Querying notes created since {timestamp}...")
        keep.sync()
        notes = query_notes_created_after(keep, timestamp)
        timestamp = datetime.now(tz)
        printf(f"Done")

        for note in notes:
            note_content = get_note_content(note)
            printf(f"Note: {note_content}")
            process_note_content(note_content)

        time.sleep(60)

def main():
    loop()

if __name__ == "__main__":
    main()