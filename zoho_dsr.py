import http.client
import json
import datetime
import subprocess
import urllib.parse

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(description="Zoho DSR Tool to add DSR records in Zoho CRM")

# This tool creates a Daily Work Status Report (DSR) record in Zoho People.
@mcp.tool()
def create_dsr_record(activities:list[str]):
    """
    Create a Daily Work Status Report record in Zoho People.
    Parameters:
    - activities: List of activities to be recorded in the DSR.
    Example:
        create_dsr_record(["Activity 1", "Activity 2", "Activity 3"])
    """
    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Authorization": f"Zoho-oauthtoken {get_access_token()}",
        "Content-Type": "application/x-www-form-urlencoded" 
    }

    input_data = {
        "inputData": { 
            "DSR_Date": datetime.date.today().strftime("%d-%b-%Y"),
            "Activity": activities,
            "Lookup_1": "29929000007049341"
        }
    }
    payload = urllib.parse.urlencode(input_data)

    conn = http.client.HTTPSConnection("people.zoho.in")
    conn.request("POST", "/api/forms/json/DSR/insertRecord", payload, headersList)
    response = conn.getresponse()
    result = response.read()

    print(result.decode("utf-8"))

# This function retrieves an access token from Zoho using OAuth2.
def get_access_token():
    """
    Get access token from Zoho using OAuth2.
    """

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)",
        "Content-Type": "application/x-www-form-urlencoded" 
    }

    payload = ""
    conn = http.client.HTTPSConnection("accounts.zoho.in")
    conn.request("POST", "/oauth/v2/token?refresh_token=1000.ac22f5753323d784b7758db5756c5f54.24bae40731b3a407741b025a2c524091&client_id=1000.WFK56S2AP7E1DCH4HJPFBG7LKVUGSW&client_secret=193df6efed9cd734792830516b9080fef4e333e758&grant_type=refresh_token", payload, headersList)
    response = conn.getresponse()
    result = response.read()
    response_data = json.loads(result.decode("utf-8"))
    access_token = response_data.get("access_token")
    return access_token

# This tool fetches the git status and log, useful for debugging or tracking changes.
@mcp.tool()
def get_git_status_and_log():
    """Run 'git status' and 'git log' commands and return their outputs as strings."""
    status = subprocess.check_output(["git", "status"], text=True)
    return status + "\n\n" + status


if __name__ == "__main__":
    mcp.run(transport="stdio")

