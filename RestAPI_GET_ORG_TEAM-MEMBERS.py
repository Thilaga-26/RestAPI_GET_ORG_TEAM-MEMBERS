""" Fetching teams and members for a GitHub organization """
import argparse
import os
import requests

# Retrieving GitHub access token from environment variable
access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
if not access_token:
    print("Error: GitHub access token not found. Please set GITHUB_ACCESS_TOKEN environmental variable.")

# Parsing command-line arguments
parser = argparse.ArgumentParser(description="Fetch teams and its members for a GitHub organization")
parser.add_argument("--org_name", help="Name of the GitHub organization")
args = parser.parse_args()

organization_name = args.org_name

def fetch_organization_teams(orgs_name , access_token):
    """
    Fetches teams for a GitHub organization.

    Args:
        orgs_name (str): The name of the GitHub organization.
        access_token (str): The access token for authentication.

    Returns:
        list: A list of dictionaries representing the teams. Each dictionary contains
              information about a single team, including its name and ID.
    """
    url = f"https://api.github.com/orgs/{orgs_name}/teams"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        teams = response.json()
        return teams
    else:
        print(f"Failed to fetch organization teams. Status code: {response.status_code}")
        return None

def fetch_team_members(team_id, access_token):
    """
    Fetches members of a GitHub team.

    Args:
        team_id (int): The ID of the GitHub team whose members are to be fetched.
        access_token (str): The access token for authentication.

    Returns:
        list or None: A list of dictionaries representing the members of the team if the
                      request is successful (HTTP status code 200). Each dictionary contains
                      information about a single member. Returns None if the request fails.
    """
    url = f"https://api.github.com/teams/{team_id}/members"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        members = response.json()
        return members
    else:
        print(f"Failed to fetch team members. Status code: {response.status_code}")
        return None

# If organization name is provided, fetch Teams for that organization    
teams = fetch_organization_teams(organization_name , access_token)
# Displaying Teams names if found, otherwise printing a message
if teams:
    print(f"Teams for organization '{organization_name}':")
    for team in teams:
        print(f"Team Name: {team["name"]}  &  Team ID: {team["id"]}")
        members = fetch_team_members(team["id"], access_token)
        print("Members of Team:")
        # Displaying Members names if found, otherwise printing a message
        if members:
            for member in members:
                print(member['login'])
        else:
            print("No members found")

else:
    print("No Teams found.")
