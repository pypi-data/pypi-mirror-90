import time
import urllib.parse

import requests
from halo import Halo

from .exceptions import *


def authenticate_with_github(client_id, scopes=None):

    if scopes is None:
        scopes = []

    def send_auth_request(mode, payload, interval=None):
        if mode == "verify":
            response = requests.post("https://github.com/login/device/code", data=payload)

            if response.status_code != 200:
                error_message = "A connection to GitHub could not be established, or the client sent a malformed " \
                                "request."
                raise GitHubConnectionError(error_message)

            data = dict(urllib.parse.parse_qsl(response.text))

            if not data:
                error_message = "Invalid GitHub OAuth Client ID."
                raise BadClientError(error_message)

            return data

        if mode == "auth":
            print()
            spinner = Halo(text="Waiting for authentication from GitHub...")
            spinner.start()
            while True:
                response = requests.post("https://github.com/login/oauth/access_token", data=payload)

                if response.status_code != 200:
                    error_message = "A connection to GitHub could not be established."
                    spinner.fail("Authentication failed.")
                    time.sleep(1)

                    raise GitHubConnectionError(error_message)

                data = dict(urllib.parse.parse_qsl(response.text))

                if not data:
                    error_message = "Invalid GitHub OAuth Client ID."
                    spinner.fail("Authentication failed.")
                    time.sleep(1)

                    raise BadClientError(error_message)

                try:
                    error = data["error"]
                except KeyError:
                    token = data["access_token"]
                    spinner.succeed("Authentication success.")
                    time.sleep(1)

                    return token
                else:
                    if error == "access_denied":
                        error_message = "The request to connect to GitHub was denied."
                        spinner.fail("Authentication failed.")
                        time.sleep(1)

                        raise GitHubAuthenticationError(error_message)

                    if error == "expired_token":
                        error_message = "GitHub took too long to respond."
                        spinner.fail("Authentication failed.")
                        time.sleep(1)

                        raise GitHubAuthenticationError(error_message)

                    if error == "slow_down":
                        interval = data["interval"]

                    time.sleep(interval)

    auth_data = send_auth_request(mode="verify",
                                  payload={"client_id": client_id, "scope": " ".join(scopes)})

    print(f"Open {auth_data['verification_uri']} in a browser and enter the following code:\n"
          f"\n"
          f"{auth_data['user_code']}")

    token = send_auth_request(mode="auth",
                              payload={"client_id": client_id,
                                       "device_code": auth_data["device_code"],
                                       "grant_type": "urn:ietf:params:oauth:grant-type:device_code"},
                              interval=int(auth_data["interval"]))

    return token
