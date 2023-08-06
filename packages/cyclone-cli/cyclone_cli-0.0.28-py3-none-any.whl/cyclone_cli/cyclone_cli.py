import argparse
from ._version import __version__
import requests
import json


def main(parser=argparse.ArgumentParser()):

    print("Executing 'main()' from my app!")

    subparsers = parser.add_subparsers(help="valid commands", dest="command")

    sub_parser_put = subparsers.add_parser("put")
    sub_parser_put.add_argument(
        "-k", "--key", type=str, help="Unique key to write to.", required=True
    )
    sub_parser_put.add_argument("file", type=str, help="Path to the JSON file to put.")

    sub_parser_put = subparsers.add_parser("get")
    sub_parser_put.add_argument("key", type=str, help="Content key to use.")
    sub_parser_put.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output path to write to.",
        default="content.json",
        required=False,
    )

    sub_parser_put = subparsers.add_parser("set-deployment-options")
    sub_parser_put.add_argument(
        "-k", "--key", type=str, help="Unique key to write to.", required=True
    )
    sub_parser_put.add_argument("file", type=str, help="Path to the JSON file to put.")

    sub_parser_put = subparsers.add_parser("get-deployment-options")
    sub_parser_put.add_argument("key", type=str, help="Content key to use.")

    sub_parser_put = subparsers.add_parser("deploy")
    sub_parser_put.add_argument("key", type=str, help="Content key to use.")

    subparsers.add_parser("version")

    args = parser.parse_args()

    if args.command is None:
        print("No command detected. Please add --help to see all commands.")
    elif args.command == "put":
        put_command(args.key, args.file)
    elif args.command == "get":
        get_command(args.key, args.output)
    elif args.command == "set-deployment-options":
        set_deployment_options(args.key, args.file)
    elif args.command == "get-deployment-options":
        get_deployment_options(args.key)
    elif args.command == "deploy":
        deploy(args.key)
    elif args.command == "version":
        show_version()


def show_version():
    print(__version__)


def set_deployment_options(key: str, file: str):
    with open(file, "r") as f:
        data = json.load(f)
    item_data = {"key": key, "deployment_options": data}
    post_item("https://api.cyclonecms.com/putDeploymentOptions", item_data)


def get_deployment_options(key: str):
    endpoint = "https://api.cyclonecms.com/getDeploymentOptions"
    get_payload_from_endpoint(endpoint, key)


def deploy(key: str):
    post_item("https://api.cyclonecms.com/executeDeployment", {"key": key})


def put_command(key: str, file: str):
    with open(file, "r") as f:
        data = json.load(f)
    item_data = {"key": key, "content": data}
    post_item("https://api.cyclonecms.com/putContent", item_data)


def get_command(key: str, output: str):
    endpoint = "https://api.cyclonecms.com/getContent"
    status_code, payload = get_payload_from_endpoint(endpoint, key)
    if status_code == 200:
        print(f"Writing output to {output}")
        with open(output, "w") as f:
            json.dump(payload, f, indent=2)


def post_item(endpoint: str, item: dict):
    r = requests.post(endpoint, json=item)
    print("Got Response")
    print(r.status_code)
    print(r.json())


def get_payload_from_endpoint(endpoint: str, key: str):
    query_params = {"key": key}
    r = requests.get(endpoint, params=query_params)

    response_object = r.json()
    status_code = r.status_code
    print("Got Response")
    print(status_code)
    print(response_object)

    if status_code == 200:
        payload = json.loads(response_object["payload"])
        print(f"Got payload: {payload}")
        return status_code, payload
    else:
        return status_code, None