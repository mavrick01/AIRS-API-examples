
# AIRS API Examples

This repository contains Python scripts that demonstrate how to interact with the AIRS API for scanning files and retrieving reports.

## Requirements

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

## Environment Variables

Before running the scripts, you need to set up your environment variables. Copy the `.env_example` file to a new file named `.env`:

```bash
cp .env_example .env
```

Then, edit the `.env` file and provide your `PANW_AI_SEC_API_KEY` and `AI_PROFILE_NAME`:

```
PANW_AI_SEC_API_KEY=your_airs_api_key
AI_PROFILE_NAME=your_airs_security_profile name
```

## Scripts

### `syncscan.py`

Performs a synchronous (blocking) scan of a file. The script will wait for the scan to complete and then print the results.

**Usage:**

```bash
python syncscan.py  "prompt"
python syncscan.py  -p "prompt"
python syncscan.py  -r "response"
python syncscan.py  -p "prompt" -r "response" -c "context"
```

### `asyncscan.py`

Initiates an asynchronous (non-blocking) scan of a file with multiple prompts/responses/contexts or combinations of these fields. 

The script will start the scan and print a report ID, which can be used with other scripts to check the scan status and retrieve the report.

**Usage:**

```bash
python asyncscan.py <your_csvfile>
```

The CSV file must have the headers: 

`prompt,response,context`

Blank columns are permitted

**Example**
A `test.csv` file is provided to show an example of how the CSV file will look.
### `scanresults.py`

Retrieves the results of a scan using the `scan_id` returned by `asyncscan.py` or `syncscan.py`. This script will query the AIRS API and print the detailed results of the scan in JSON format.

**Usage:**

The script requires a single argument: the `scan_id` of the scan you want to query.

```bash
python scanresults.py <your_scan_id>
```

**Example:**

```bash
python scanresults.py 00000000-0000-0000-0000-000000000000
```

The output will be a JSON object containing the scan results, including any detected threats or issues.

### `scanreport.py`

Retrieves the full report of a scan using the report ID.

**Usage:**

```bash
python scanreport.py <your_report_id>
```
