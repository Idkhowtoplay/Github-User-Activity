import argparse
import json
import urllib.error
import urllib.request

def main():
    parser = argparse.ArgumentParser(description="User Activity")
    subparsers = parser.add_subparsers(dest="command")

    parser_a = subparsers.add_parser("github-activity", help="Display user activity in the terminal")
    parser_a.add_argument("user", type= str, help="Username")
    args = parser.parse_args()

    if args.command == "github-activity":
        data(args.user)

def data(user):
    print("output:")
    try:
        api = urllib.request.urlopen(f"https://api.github.com/users/{user}/events")
        if api.status != 200:
            print(f"Error: Response code {api.status}")
        else:
            item = json.load(api)
            for event in item:
                repo = event["repo"]["name"]
                name = event["actor"]["login"]
                if event["type"] == "PushEvent":
                    print(f"- Pushed {len(event["payload"]["commits"])} commits to {repo}")
                elif event["type"] == "CreateEvent":
                    print(f"- User {name} create repo {repo}")
                elif event["type"] == "WatchEvent":
                    print(f"- Starred {repo}")
                elif event["type"] == "PullRequestEvent":
                    print(f"- Opened pull request on {repo}")
                elif event["type"] == "ForkEvent":
                    print(f"- Forked {repo}")
                elif event["type"] == "IssuesEvent":
                    print(f"- opened issue on {repo}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User {user} not found")
        else:
            print(f"HTTP Error: {e.code}")
    
main()