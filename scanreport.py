"""
 Python Example for Querying Scan Reports by Report ID

This script takes a scan ID as a command-line argument and retrieves the
corresponding scan results from the AI Security API.

API Reference: https://pan.dev/prisma-airs/api/get-scan-results-by-report-i-ds/
"""

import os
import argparse
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv

import aisecurity
# IMPORTANT: For asynchronous operations, import the Scanner from aisecurity.scan.asyncio
from aisecurity.scan.asyncio.scanner import Scanner

async def main():
    """
    Main function to parse arguments, and query the scan results.
    """
    # Load variables from the .env file into the environment
    load_dotenv()

    # --- Argument Parsing Setup ---
    # Sets up the script to accept a single scan_id
    parser = argparse.ArgumentParser(
        description="Query scan results by Report ID using the Palo Alto Networks AI Security API.",
        epilog="Example: python3 scanresults.py 00000000-0000-0000-0000-000000000000",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'report_id',
        help="The Report ID to query. This is returned from the AIRS Scanning endpoint."
    )
    args = parser.parse_args()

    # --- Environment Variable and SDK Setup ---
    API_KEY = os.getenv("PANW_AI_SEC_API_KEY")

    if not API_KEY:
        raise ValueError("API Key not found. Make sure PANW_AI_SEC_API_KEY is set in your .env file.")

    aisecurity.init(api_key=API_KEY)

    # --- Scanning Execution ---
    scanner = Scanner()
    try:
        print(f"Querying results for Report ID: {args.report_id}...")
        
        # See API documentation for response structure
        # https://pan.dev/prisma-airs/api/airuntimesecurity/get-scan-reports-by-report-i-ds/
        scan_by_ids_response = await scanner.query_by_report_ids(report_ids=[args.report_id])
        
        print("\nQuery complete. Response:")
        # The response is a list of result objects. We need to convert each one to a dictionary.
        # A list comprehension is a clean way to do this.
        response_dicts = [item.to_dict() for item in scan_by_ids_response]
        # Custom serializer for datetime objects, which are not handled by the default JSON encoder.
        def datetime_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        print(json.dumps(response_dicts, indent=2, default=datetime_serializer))

    except Exception as e:
        print(f"An error occurred during the query: {e}")
    finally:
        print("\nClosing scanner.")
        await scanner.close()

if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(main())