# LinkedIn Profile Search & Scrape Bot

## Overview

This project utilizes AI agents powered by the `agno` library and Google Gemini, combined with Selenium browser automation, to search for LinkedIn profiles based on user input, scrape profile information and save the results to a CSV file.

The system uses a chatbot interface to interact with the user, understand their search requirements (including LinkedIn Boolean search syntax), delegate the search task to a specialized agent, and then delegate the writing task to another agent.

## Features

* **AI-Powered Chatbot:** Uses Google Gemini via the `agno` library for natural language interaction and task delegation.
* **LinkedIn Profile Search:** Leverages Selenium to automate searching LinkedIn for people based on user queries.
    * Supports LinkedIn Boolean search syntax within the query (e.g., `"Software Engineer" AND Google NOT Intern`).
* **Pagination Handling:** Automatically clicks through search result pages to gather the desired number of profiles (up to `max_results`).
* **CSV Output:** Saves the scraped data neatly into a `results.csv` file using `pandas`.
* **Automated Login:** Attempts to log into LinkedIn automatically using provided credentials (or environment variables).
* **Browser Automation:** Uses Selenium and `webdriver-manager` to control a Chrome/Brave browser instance.

## Requirements

* Python 3.x
* Google Chrome browser installed. (The code is currently configured for Chrome, but could be adapted for Brave or others).
* A LinkedIn account.
* Required Python packages:
    * `agno`
    * `pandas`
    * `selenium`
    * `webdriver-manager`
* (Implicit) Access configured for Google Gemini API via the `agno` library.

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    virtualenv <name>
    # On Windows
    source <name>/bin/activate
    # On macOS/Linux
    source <name>/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install agno pandas selenium webdriver-manager
    ```

4.  **Configure Browser Path (If Necessary):**
    * Open `linkedin_tools.py`.
    * Locate the `linkedin_search_tool` function.
    * Modify the `options.binary_location` if your Chrome installation is not in the default path shown (`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`). Remove this line if Chrome is in the system's default PATH.
    * The `options.add_argument("--user-data-dir=...")` line tries to use an existing browser profile to potentially maintain login sessions. **Update the path** `/Users/kush/Library/Application Support/Google/Chrome` to match *your* user's Chrome profile path on your system, or comment it out if you don't want to use a specific profile. Ensure the `--profile-directory` matches the profile you want to use (often `Default`). Using a specific profile *might* help bypass some login hurdles but isn't guaranteed.

5.  **Configure LinkedIn Credentials (IMPORTANT):**
    * The script currently uses `os.getenv` with hardcoded fallback credentials in `linkedin_tools.py`:
        ```python
        username = os.getenv("LINKEDIN_USERNAME", "<Username>")
        password = os.getenv("LINKEDIN_PASSWORD", "<Password>")
        ```
    * **It is strongly recommended NOT to keep credentials directly in the code.** Instead, set them as environment variables:
        * **On macOS/Linux:**
            ```bash
            export LINKEDIN_USERNAME="your_linkedin_email@example.com"
            export LINKEDIN_PASSWORD="your_linkedin_password"
            ```
        * **On Windows (Command Prompt):**
            ```bash
            set LINKEDIN_USERNAME="your_linkedin_email@example.com"
            set LINKEDIN_PASSWORD="your_linkedin_password"
            ```
        * **On Windows (PowerShell):**
            ```bash
            $env:LINKEDIN_USERNAME="your_linkedin_email@example.com"
            $env:LINKEDIN_PASSWORD="your_linkedin_password"
            ```
    * Alternatively, modify the script to load credentials from a secure configuration file.

6.  **Configure `agno` / Gemini:**
    * Ensure your environment is set up for the `agno` library to access the Google Gemini API. This usually involves setting environment variables like `GOOGLE_API_KEY`. Refer to the `agno` library's documentation for specifics.

## Usage

1.  **Run the Main Script:**
    ```bash
    python linkedin_bot.py
    ```

2.  **Interact with the Chatbot:**
    * The script will prompt you with `You: `.
    * Enter your desired LinkedIn search query. You can use keywords and LinkedIn's Boolean operators (AND, OR, NOT, parentheses). Examples:
        * `"Data Scientist" AND Python`
        * `("Software Engineer" OR "Backend Developer") AND Google NOT Intern`
        * `Recruiter AND ("Tech Industry" OR SaaS)`
    * The bot will confirm, use the `linkedin` agent to perform the search (showing tool calls if `debug_mode=True`), and then use the `writer` agent to save the results.
    * The bot will respond with the status (e.g., confirmation of file saving).

3.  **Exit:**
    * Type `bye` when prompted to stop the script.

4.  **Check Results:**
    * A file named `results.csv` will be created in the same directory, containing the scraped `name`, `headline`, and `url` for the profiles found.

## Important Notes & Limitations

* **LinkedIn Terms of Service:** Automating interaction with LinkedIn, especially scraping data, may violate their Terms of Service. Use this tool responsibly and ethically. Excessive use could lead to warnings or account restrictions.
* **Website Changes:** LinkedIn frequently updates its website design. This can break the Selenium selectors (XPaths, CSS selectors, element IDs) used in `linkedin_tools.py`. If the script stops working, these selectors likely need to be updated.
* **Login Challenges:** LinkedIn may present CAPTCHAs, multi-factor authentication prompts, or other security checks that can block automated logins. Using an existing browser profile (`--user-data-dir`) *might* help but isn't a guaranteed solution.
* **Rate Limiting:** Making too many requests (searches, profile views) in a short period can trigger LinkedIn's rate limits or temporary blocks. The `time.sleep()` calls in the code are basic attempts to mitigate this but may need adjustment.
* **Error Handling:** The current error handling is basic. More robust error checking and recovery mechanisms could be added.
* **Data Scraped:** This script only collects Name, Headline, and URL. Modifying `get_profile_details` in `linkedin_tools.py` would be required to scrape additional information (like Experience, Education, etc.), which would also increase the risk of detection by LinkedIn.
