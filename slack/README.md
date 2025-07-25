# Slack Channel Creator

A Python script to automatically create private Slack channels and invite members based on CSV data.

I refered to [this repository](https://github.com/kashtodi/Slack-Channel-Creator) when I created this script.


## Requirements

- Python 3.7+
- Slack Bot Token with appropriate permissions
- Required Python packages

## Slack Bot Setup

Your Slack bot needs the following OAuth scopes:

### Bot Token Scopes:
- `channels:write` - Create public channels
- `groups:write` - Create private channels
- `users:read` - Read user information

### How to set up the bot:
1. Go to [Slack API](https://api.slack.com/apps)
2. Create a new app or select an existing one
3. Go to "OAuth & Permissions"
4. Add the required scopes listed above
5. Install the app to your workspace
6. Copy the "Bot User OAuth Token" to your `.env` file

## Usage

```bash
python create_channel.py --csv path/to/your/channels.csv
```

### Command Line Arguments

- `--csv`: Path to the CSV file containing channel information (required)

## CSV Format

The CSV file must contain the following columns:

| Column Name | Description | Example |
|-------------|-------------|---------|
| `Channel_Name` | Name of the channel to create | `project-alpha-team` |
| `Members` | Comma-separated list of user IDs | `U087PCY6SUW,U087PCY6SUY` |


**Important Notes:**
- Channel names must follow Slack's naming conventions (lowercase, no spaces, use hyphens)
- Member IDs should be slack user IDs

## Output

The script generates several types of output:

### 1. Console Output
- Real-time progress bar showing channel creation progress
- Final summary with success/failure statistics

### 2. Log Files (in `./log/` directory)
- `{csv_name}.log`: Detailed logs of the entire process
- `{csv_name}.csv`: CSV file with results including:
  - Channel ID (if successful)
  - Channel Name
  - Members list
  - Success status (True/False)
  - Error message (if failed)

### 3. Summary Statistics
```
Summary:
Total channels processed: 10
Successfully created: 8
Failed: 2
Results saved to: ./log/channels.csv
```

## Workflow

### Step 1: Prepare User ID Mapping
The most time-consuming part is preparing the CSV file with correct Slack user IDs. Follow these steps:

1. **Extract user information from your source system (e.g., PCS)**
   - Export user names/emails from your management system
   - Ensure names match exactly as they appear in Slack

2. **Get Slack user IDs**
   - Use Slack's web interface: Go to a user's profile → More → Copy member ID
   - Or use Slack API to batch retrieve user IDs by email
   - Or use the Slack desktop app: Right-click user → View profile → Copy member ID

3. **Create name-to-ID mapping**
   - Build a spreadsheet mapping real names to Slack user IDs
   - Verify each ID is correct to avoid invitation failures

### Step 2: Generate the CSV File
1. Create your channel assignment logic (e.g., reviewers per paper, team assignments)
2. Generate the CSV with proper channel names and member lists
3. Format member IDs as comma-separated values: `U087PCY6SUW,U087PCY6SUY,U087PCY6SUZ`

### Step 3: Set Up Environment
1. Install dependencies: `pip install -r requirements.txt`
2. Configure your Slack bot token in `.env` file
3. Test with a small sample CSV first

### Step 4: Execute Channel Creation
1. Run the script: `python create_channel.py --csv your_file.csv`
2. Monitor progress and check for any errors
3. Review the generated log files for results

### Step 5: Verify Results
1. Check the summary statistics
2. Review failed channels in the log files
3. Manually verify a few channels in Slack to ensure proper setup

**Pro Tips:**
- It will be helpful to use not just the paper id but also the title in the channel name.
- Start with a small test batch (5-10 channels) to verify your setup
- Keep your user ID mapping file for future use
- The script respects rate limits, so larger batches will take time