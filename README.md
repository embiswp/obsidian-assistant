# Google Keep to Markdown Daily Notes Processor

This Python script automates the process of syncing notes from **Google Keep** to a **Markdown-based daily notes system**. It extracts tasks and diary entries from Google Keep notes, processes them using **OpenAI's GPT-4**, and organizes them into a structured daily note file. This is particularly useful for individuals who use Google Keep for quick note-taking and want to integrate their notes into a daily journal or task management system.

---

## Features

- **Google Keep Integration**: Fetches notes from Google Keep using the `gkeepapi` library.
- **Task Extraction**: Uses OpenAI's GPT-4 to extract tasks from note content and formats them in a Markdown checklist format (`- [ ] task`).
- **Daily Notes System**: Creates or updates a daily Markdown file based on a template, organizing tasks and diary entries under specific headers.
- **Environment Variable Configuration**: Uses environment variables for secure and flexible configuration.
- **Continuous Sync**: Runs in a loop, syncing new notes every 60 seconds.

---

## Environment Variables

If you are running this script inside a Docker container, you must set the following environment variables to configure its behavior:

### Required Variables
1. **`GKEEP_EMAIL`**  
   - **Description**: The email address associated with your Google Keep account.  
   - **Example**: `user@example.com`

2. **`MASTER_TOKEN`**  
   - **Description**: The master token for authenticating with Google Keep. This can be obtained using the `gkeepapi` library.  
   - **Example**: `your_master_token_here`

3. **`OPENAPI_KEY`**  
   - **Description**: The API key for OpenAI to use GPT-4 for task extraction.  
   - **Example**: `sk-12345abcdef`

4. **`DAILY_TEMPLATE_PATH`**  
   - **Description**: The file path to the Markdown template used for creating new daily notes.  
   - **Example**: `/app/templates/daily_template.md`

5. **`DAILY_NOTES_FOLDER`**  
   - **Description**: The folder where daily notes will be saved.  
   - **Example**: `/app/daily_notes`

6. **`TASKS_HEADER`**  
   - **Description**: The header in the Markdown file where tasks will be inserted.  
   - **Example**: `## Tasks`

7. **`DIARY_HEADER`**  
   - **Description**: The header in the Markdown file where diary entries will be inserted.  
   - **Example**: `## Diary`

---

## Running the Script

### Without Docker
1. Set the required environment variables in your terminal:
   ```bash
   export GKEEP_EMAIL="user@example.com"
   export MASTER_TOKEN="your_master_token_here"
   export OPENAPI_KEY="sk-12345abcdef"
   export DAILY_TEMPLATE_PATH="/app/templates/daily_template.md"
   export DAILY_NOTES_FOLDER="/app/daily_notes"
   export TASKS_HEADER="## Tasks"
   export DIARY_HEADER="## Diary"
   ```

2. Install the required Python packages:
   ```bash
   pip install gkeepapi openai pytz
   ```

3. Run the script:
   ```bash
   python script.py
   ```

### With Docker
1. Create a `.env` file with the required environment variables:
   ```plaintext
   GKEEP_EMAIL=user@example.com
   MASTER_TOKEN=your_master_token_here
   OPENAPI_KEY=sk-12345abcdef
   DAILY_TEMPLATE_PATH=/app/templates/daily_template.md
   DAILY_NOTES_FOLDER=/app/daily_notes
   TASKS_HEADER=## Tasks
   DIARY_HEADER=## Diary
   ```

2. Build the Docker image:
   ```bash
   docker build -t keep-to-markdown .
   ```

3. Run the Docker container:
   ```bash
   docker run --env-file .env keep-to-markdown
   ```

---

## Dockerfile Example

Here’s an example `Dockerfile` for containerizing the script:
```dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY script.py .

# Set the entrypoint
ENTRYPOINT ["python", "script.py"]
```

---

## How It Works

1. **Authentication**: The script authenticates with Google Keep using the provided email and master token.
2. **Note Fetching**: It queries Google Keep for notes created after the last sync timestamp.
3. **Task Extraction**: Each note's content is sent to OpenAI's GPT-4 to extract tasks in a Markdown checklist format.
4. **Daily Notes Creation**: A new daily note file is created (if it doesn't exist) using a template. Tasks and diary entries are inserted under their respective headers.
5. **Continuous Sync**: The script runs in a loop, syncing new notes every 60 seconds.

---

## Example Output

### Input (Google Keep Note)
```
Buy groceries:
- Milk
- Eggs
- Bread

Meeting with John at 3 PM.
```

### Output (Markdown Daily Note)
```markdown
## Tasks
- [ ] Buy groceries
- [ ] 3 PM Meeting with John

## Diary
Buy groceries:
- Milk
- Eggs
- Bread

Meeting with John at 3 PM.
```

---

## Contributing

If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Notes
- Ensure that your Google Keep account allows third-party access if you encounter authentication issues.
- The OpenAI API key should be kept secure and not exposed publicly.
