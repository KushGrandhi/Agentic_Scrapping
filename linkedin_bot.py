from agno.agent import Agent
from agno.models.google import Gemini
import os
from linkedin_tools import linkedin_search_tool
from typing import List, Dict

import pandas as pd

def writeer(data: List[Dict[str, str]]) -> str:
    """
    Saves a list of dictionaries to a CSV file.

    Parameters:
    - data (List[Dict[str, str]]): A list of dictionaries where each dictionary represents a row.
      Example format:
      [
          {"name": "John Doe", "headline": "Software Engineer", "url": "https://linkedin.com/in/johndoe"},
          {"name": "Jane Smith", "headline": "Data Scientist", "url": "https://linkedin.com/in/janesmith"}
      ]

    Returns:
    - str: Confirmation message that the file has been successfully saved.
    """

    # Ensure `data` is not empty and structured properly
    if not data or not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        return "Error: Invalid data format. Expected a non-empty list of dictionaries."

    # Ensure all dictionaries have expected keys
    required_keys = {"name", "headline", "url"}
    for item in data:
        if not required_keys.issubset(item.keys()):
            return f"Error: Missing required keys in data. Expected keys: {required_keys}"

    try:
        # Convert list of dictionaries to a Pandas DataFrame
        df = pd.DataFrame(data)

        # Save to CSV without index
        file_path = "results.csv"
        df.to_csv(file_path, index=False)

        return f"Successfully saved the file to {file_path}"

    except Exception as e:
        return f"Error saving the file: {str(e)}"
    
linkedin = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", search=False),
    role='search linkedin profiles to scrappe data',
    instructions=["Use the tool to find the profiles by collecting profiles","Query using linkedin Boolean search","write to path= results.csv"],
    tools=[linkedin_search_tool],
    # add_history_to_messages=True,
    # num_history_responses=8,
    # read_tool_call_history=True,
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

writer = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", search=False),
    role='write csv files',
    instructions=["write to path= results.csv"],
    tools=[writeer],
    # add_history_to_messages=True,
    # num_history_responses=8,
    # read_tool_call_history=True,
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

chatbot = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", search=False),
    role='Agent to help me filter linkedin profiles',
    instructions=["Chat with me to help me get the best profiles","Filter the candidates based on my given needs","once you get the result "],
    team=[linkedin, writer],
    add_history_to_messages=True,
    num_history_responses=8,
    read_tool_call_history=True,
    show_tool_calls=True,
    markdown=True,
)

if __name__ == '__main__':
    msg = ''
    # writeer( [
    #       {'name': 'John Doe', 'headline': 'Software Engineer', 'url': 'https://linkedin.com/in/johndoe'},
    #       {'name': 'Jane Smith', 'headline': 'Data Scientist', 'url': 'https://linkedin.com/in/janesmith'}
    #   ],'helloworld.csv')
    while msg != 'bye':
        msg = input('You: ')
        chatbot.print_response(msg, stream=False, show_message=True)
