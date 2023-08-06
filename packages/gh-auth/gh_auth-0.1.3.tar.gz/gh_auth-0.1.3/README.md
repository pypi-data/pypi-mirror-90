# gh-auth

A simple Python library for web-based GitHub authentication using the [device flow](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps#device-flow).

## Installation
```
pip install gh-auth
```

## Usage

1. On GitHub, [create a GitHub or OAuth app](https://github.com/settings/apps).

2. In your code, import the `authenticate_with_github()` function and pass it your app's client ID.

```python
from gh_auth import authenticate_with_github

authenticate_with_github(client_id)
```
That's it.

When called, the function will prompt users to visit https://github.com/login/device and enter an eight-character code, 
then continously ping GitHub for a response. Upon sucessful authentication, the function will return a token you can use
to interact with the GitHub API via libraries such as [PyGithub](https://github.com/PyGithub/PyGithub).

### Scopes

If you're using an OAuth app, you'll probably also want to define what scopes you want your app to be granted. Simply pass
a list of scopes into the ``authenticate_with_github()`` function alongside your client ID, like so:

```python
authenticate_with_github(client_id, scopes=["example_scope", "another_scope"])
```
See a full list of available OAuth scopes [here](https://docs.github.com/en/free-pro-team@latest/developers/apps/scopes-for-oauth-apps).

If you're using an OAuth app and don't define any scopes, GitHub will default to granting it read-only access to the
public data associated with the account being authenticated and nothing more. (For GitHub apps, [scopes are defined
on GitHub](https://docs.github.com/en/free-pro-team@latest/developers/apps/editing-a-github-apps-permissions) 
and can't be changed from this module.)

## License

gh-auth's source code is released under the MIT License.