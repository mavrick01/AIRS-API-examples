
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

Then, edit the `.env` file and provide your `CLIENT_ID` and `CLIENT_SECRET`:

```
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

## Scripts

### `syncscan.py`

Performs a synchronous (blocking) scan of a file. The script will wait for the scan to complete and then print the results.

**Usage:**

```bash
python syncscan.py -f /path/to/your/file.txt
```

### `asyncscan.py`

Initiates an asynchronous (non-blocking) scan of a file. The script will start the scan and print a report ID, which can be used with other scripts to check the scan status and retrieve the report.

**Usage:**

```bash
python asyncscan.py -f /path/to/your/file.txt
```

### `scanresults.py`

Retrieves the results of a scan using the report ID obtained from an asynchronous scan.

**Usage:**

```bash
python scanresults.py -rid <your_report_id>
```

### `scanreport.py`

Retrieves the full report of a scan using the report ID.

**Usage:**

```bash
python scanreport.py -rid <your_report_id>
```
