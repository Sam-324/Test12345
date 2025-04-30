import ollama
import json
import tqdm
import logging
import os
import time


#Program to call the Ollama API and save the response to a file
# This program loads a dataset from a JSON file, creates a prompt from the data, and then calls the Ollama API to get a response.
# The response is then saved to a new JSON file.
# The program uses the ollama library to interact with the API and the json library to handle JSON data.
# It also uses the tqdm library to create a progress bar and the logging library to log messages to a file and the console.


input_file="final_dataset.json"
output_file="no_layers2.json"

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
    print(prompt)
    # Call the Ollama API to get the response
    response = ollama.chat(
        model="deepseek-r1:1.5b",
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    return response.get('message', {}).get('content', '')




def save_response(prompt, output_file, response):
    """Save only prompt and response to the output file"""
    try:
        # Check if file exists and load existing data
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                data_to_save = json.load(f)
        else:
            data_to_save = []

        # Only save prompt and response
        new_entry = {
            "prompt": prompt if isinstance(prompt, str) else prompt.get('prompt', ''),
            "response": response
        }
        data_to_save.append(new_entry)

        with open(output_file, 'w') as f:
            json.dump(data_to_save, f, indent=4)
            
    except Exception as e:
        logger.error(f"Error saving response: {e}")
        raise

# Clear the context window
def reset_context():
    """Reset the Ollama context by creating a new chat session"""
    try:
        # Reset by calling with an empty message
        ollama.chat(
            model="deepseek-r1:1.5b",
            messages=[],
            options={"reset": True}
        )
        logger.info("Context reset successful")
    except Exception as e:
        logger.error(f"Error resetting context: {e}")




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






# Main function to run the script

def main():
    # Load the data from the input file
    total_data = load_data(input_file)
    progress_bar = create_progress_bar(total_data)
    prompt_counter = 0
    reset_context()  # Reset context at the start
    logger.info("Starting the main processing loop...")
    try:
        for item in total_data:
            logger.info(f"Processing item: {item}")
            prompt = create_prompt(item)
            logger.info(f"Prompt created: {prompt}")
            
            # Get response and save
            response = get_response(prompt)
            logger.info(f"Response received: {response}")
            save_response(prompt, output_file, response)
            
            # Update counter and progress
            prompt_counter += 1
            progress_bar.update(1)
            
            if prompt_counter % 5 == 0:
                logger.info("Clearing context window...")
                reset_context() ## Clear context every 5 prompts
                time.sleep(1)  # Small delay to ensure clear completes
                
    except Exception as e:
        logger.error(f"Error in main processing loop: {e}")
        raise
    finally:
        progress_bar.close()



 

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
    logger.removeHandler(file_handler)
    # Remove the console handler from the logger
    logger.removeHandler(console_handler)

