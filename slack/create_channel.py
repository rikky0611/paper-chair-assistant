import argparse
import logging
import os
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Constants
REQUEST_LIMIT_PER_MINUTE = 20
LOG_DIR = Path("./log")

def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Create Slack channels from CSV data")
    parser.add_argument("--csv", type=str, help="Assignment CSV file path", required=True)
    return parser.parse_args()


def ensure_log_directory():
    """Create log directory if it doesn't exist."""
    LOG_DIR.mkdir(exist_ok=True)


def get_logger(name):
    """Setup and return a configured logger."""
    ensure_log_directory()
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # File handler
    log_file = LOG_DIR / f"{name}.log"
    if log_file.exists():
        log_file.unlink()
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


if __name__ == "__main__":
    args = get_args()
    csv_path = args.csv
    
    # Validate CSV file exists
    if not os.path.exists(csv_path):
        print(f'File {csv_path} does not exist.')
        exit(1)
    
    # Validate Slack token exists
    slack_token = os.getenv("SLACK_BOT_TOKEN")
    if not slack_token:
        print("Error: SLACK_BOT_TOKEN environment variable is not set.")
        exit(1)
    
    csv_name = os.path.basename(csv_path.replace('.csv', ''))
    logger = get_logger(csv_name)
    logger.debug(f'CSV: {csv_name}')

    client = WebClient(token=slack_token)
    assignment_df = pd.read_csv(csv_path)
    logger.debug(f'Creating {len(assignment_df)} channels')
    
    # Enhanced log data structure
    log_data = {
        'Channel_ID': [], 
        'Channel_Name': [], 
        'Members': [],
        'Success': [],
        'Error': []
    }

    for i, row in tqdm(assignment_df.iterrows(), total=len(assignment_df), desc="Creating channels"):
        logger.debug(f'Processing {i+1}/{len(assignment_df)}')
        channel_name = row['Channel_Name']
        members = [member.strip() for member in row['Members'].split(',')]
        
        success = False
        error_msg = None
        channel_id = None
        
        try:
            # Create private channel
            response = client.conversations_create(
                name=channel_name,
                is_private=True
            )
            channel_id = response["channel"]["id"]
            
            # Invite members to channel
            client.conversations_invite(
                channel=channel_id,
                users=members
            )
            
            # Bot removes itself from the channel
            client.conversations_leave(channel=channel_id)
            
            success = True
            logger.debug(f'[success] Channel ID: {channel_id}, Name: {channel_name}, Members: {members}')
            
        except SlackApiError as e:
            error_msg = f"Slack API Error: {e.response['error']}"
            logger.error(f'[failure] {error_msg}')
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f'[failure] {error_msg}')
        
        # Save log data
        log_data['Channel_ID'].append(channel_id)
        log_data['Channel_Name'].append(channel_name)
        log_data['Members'].append(members)
        log_data['Success'].append(success)
        log_data['Error'].append(error_msg)
        
        # Rate limiting
        time.sleep(60 / (REQUEST_LIMIT_PER_MINUTE - 1))

    # Save results to CSV
    log_df = pd.DataFrame(log_data)
    log_file_path = LOG_DIR / f'{csv_name}.csv'
    log_df.to_csv(log_file_path, index=False)
    logger.info(f'Results saved to {log_file_path}')
    
    # Summary
    total_channels = len(log_data['Success'])
    successful_channels = sum(log_data['Success'])
    failed_channels = total_channels - successful_channels
    
    print(f"\nSummary:")
    print(f"Total channels processed: {total_channels}")
    print(f"Successfully created: {successful_channels}")
    print(f"Failed: {failed_channels}")
    print(f"Results saved to: {log_file_path}")