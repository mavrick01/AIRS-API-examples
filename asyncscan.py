"""
Traditional Python Batch (Asynchronous/Multiple) Scan Example

This script reads a CSV file to perform a batch scan using the AI Security API.
Each row in the CSV should correspond to one scan request.
The CSV format is: prompt,response,context (with a header row)
Note context must include the prompt and response

API Reference: https://pan.dev/prisma-airs/api/airuntimesecurity/scan-async-request/
"""

import os
import csv
import argparse
import asyncio
from pprint import pprint
from dotenv import load_dotenv

import aisecurity
from aisecurity.generated_openapi_client.models.ai_profile import AiProfile
from aisecurity.generated_openapi_client.models.async_scan_object import AsyncScanObject
from aisecurity.generated_openapi_client.models.scan_request import ScanRequest
from aisecurity.generated_openapi_client.models.scan_request_contents_inner import (
    ScanRequestContentsInner,
)
# IMPORTANT: For asynchronous operations, import the Scanner from aisecurity.scan.asyncio
from aisecurity.scan.asyncio.scanner import Scanner

async def main():
    """
    Main function to parse arguments, read CSV, and run the async scan.
    """
    # Load variables from the .env file into the environment
    load_dotenv()

    # --- Argument Parsing Setup ---
    # Sets up the script to accept a single filename
    parser = argparse.ArgumentParser(
        description="Scan content from a CSV file using Palo Alto Networks AI Security API.",
        epilog="Example: python your_script_name.py path/to/your/file.csv",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'filename',
        help="Path to the CSV file containing content to scan. Format: prompt,response,context"
    )
    args = parser.parse_args()

    # --- Environment Variable and SDK Setup ---
    AI_PROFILE_NAME = os.getenv("AI_PROFILE_NAME")
    API_KEY = os.getenv("PANW_AI_SEC_API_KEY")

    if not API_KEY or not AI_PROFILE_NAME:
        raise ValueError("API Key or AI Profile Name not found. Make sure your .env file is configured correctly.")

    aisecurity.init(api_key=API_KEY)

    # --- CSV Processing and Content Preparation ---
    async_scan_objects = []
    req_ids = 0
    try:
        with open(args.filename, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader, None)  # Skip the header row

            for row in reader:
                # Ensure row has enough columns to avoid IndexError
                prompt = row[0] if len(row) > 0 else ""
                response = row[1] if len(row) > 1 else ""
                context = row[2] if len(row) > 2 else ""

                content_args = {}
                if prompt:
                    content_args['prompt'] = prompt
                if response:
                    content_args['response'] = response
                if context:
                    content_args['context'] = context

                # Only create a scan object if there is content to scan
                if content_args:
                    req_ids += 1
                    scan_object = AsyncScanObject(
                        req_id=req_ids,
                        scan_req=ScanRequest(
                            ai_profile=AiProfile(profile_name=AI_PROFILE_NAME),
                            contents=[ScanRequestContentsInner(**content_args)],
                        ),
                    )
                    async_scan_objects.append(scan_object)

    except FileNotFoundError:
        print(f"Error: The file '{args.filename}' was not found.")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    if not async_scan_objects:
        print("No valid content to scan was found in the CSV file.")
        return

    # --- Scanning Execution ---
    scanner = Scanner()
    try:
        print(f"Sending {len(async_scan_objects)} items for batch scanning...")
        response = await scanner.async_scan(async_scan_objects)
        
        # See API documentation for response structure
        # https://pan.dev/prisma-airs/api/airuntimesecurity/scan-async-request/
        print("\nScan request sent successfully:")
        pprint({
            "received": response.received,
            "scan_id": response.scan_id,
            "report_id": response.report_id,
        })
    finally:
        print("\nClosing scanner.")
        await scanner.close()

if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())
