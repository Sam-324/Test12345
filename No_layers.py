import ollama
import json
import os
import time
import tqdm
import numpy as np
import logging



input_file="final_dataset.json"
output_file="final_dataset_no_layers.json"





# Load the prompt from the dataset
def load_data(input_file):
    """Load the data from the input file"""
    with open(input_file, 'r') as f:
        data = json.load(f)
    return data

def create_prompt(data):
    """Create the prompt from the data"""
    if isinstance(data, dict):
        return data.get('prompt', '')
    return ''


def get_response(prompt):
    """Get the response from the Ollama API"""
    # Call the Ollama API to get the response
    response = ollama.chat(
        model="deepseek-r1:1.5b",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    return response.get('message', {}).get('content', '')



def save_response(data, output_file, response):
    """Save the response to the output file"""
    with open(output_file, 'w') as f:
        data_to_save = []
        for item in data:
            data_to_save.append({
                "prompt": item['prompt'],
                "response": response
            })

        json.dump(data_to_save, f, indent=4)


# Set the logging level to INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create a file handler to log to a file
file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.INFO)
# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Add the file handler to the logger
logger.addHandler(file_handler)
# Create a console handler to log to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

#create a progress bar using tqdm

def create_progress_bar(data):
    total = len(data)
    progress_bar = tqdm.tqdm(total=total, desc="Processing", unit="item")
    return progress_bar





#Program to call the Ollama API and save the response to a file
# This program loads a dataset from a JSON file, creates a prompt from the data, and then calls the Ollama API to get a response.
# The response is then saved to a new JSON file.
# The program uses the ollama library to interact with the API and the json library to handle JSON data.
# The program also uses the os, time, tqdm, numpy, and logging libraries for various tasks such as file handling, time management, progress tracking, and logging.
# The program is designed to be run from the command line and takes two arguments: the input file and the output file.
# Main function to run the script

def main():
    # Load the data from the input file
    total_data = load_data(input_file)


    # Create a progress bar for the data processing
    progress_bar = create_progress_bar(total_data)

    # Create the prompt from the data
    for item in total_data:
        # Log the data being processed
        logger.info(f"Processing item: {item}")

        prompt = create_prompt(item)

        # Log the prompt creation
        logger.info(f"Prompt created: {prompt}")

        # Get the response from the Ollama API
        response = get_response(prompt)

        # Log the response
        logger.info(f"Response received: {response}")

        # Save the response to the output file
        save_response(item, output_file, response)

        # Update the progress bar
        progress_bar.update(1)

    


if __name__ == "__main__":
    main()
    # Close the progress bar
    tqdm.tqdm.close()
    # Log the completion of the script
    logger.info("Script completed successfully.")
    # Close the file handler    
    file_handler.close()
    # Close the console handler
    console_handler.close()
    # Remove the file handler from the logger
    logger.removeandler(file_handler)
    # Remove the console handler from the logger
    logger.removeHandler(console_handler)



