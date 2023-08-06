from cryptography.fernet import Fernet
import pickle
import os
import pathlib
from google_auth_oauthlib import flow
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials


def get_credentials(client_id, client_secret):
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        }
    }
    scopes = ("https://www.googleapis.com/auth/devstorage.read_write",)

    app_flow = flow.InstalledAppFlow.from_client_config(client_config, scopes=scopes)
    app_flow.run_local_server()  # Should catch exception here?
    return app_flow.credentials


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def pickle_user_credentials(credentials, path, key):
    path = pathlib.Path(path)
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True, exist_ok=True)
    credentials.token = None
    data = credentials_to_dict(credentials)
    encrypt_fields(data, ("refresh_token", "client_id", "client_secret"), key)
    with open(path, "wb") as f:
        pickle.dump(data, f)


def unpickle_user_credentials(path, key):
    with open(path, "rb") as f:
        data = pickle.load(f)
    decrypt_fields(data, ("refresh_token", "client_id", "client_secret"), key)
    return Credentials(**data)


def encrypt_fields(data, keys, key_path):
    cipher = get_cipher(key_path)
    for key in keys:
        data[key] = cipher.encrypt(data[key].encode("utf-8"))


def decrypt_fields(data, keys, key_path):
    cipher = get_cipher(key_path)
    for key in keys:
        data[key] = cipher.decrypt(data[key]).decode("utf-8")


def unpickle_service_account_credentials(path, key, as_credentials=True):
    with open(path, "rb") as f:
        data = pickle.load(f)
    decrypt_fields(data, ("private_key_id", "private_key"), key)
    bucket = data.pop("bucket") if "bucket" in data else None
    if as_credentials:
        data = service_account.Credentials.from_service_account_info(data)
    return data, bucket


def pickle_service_account_credentials(data, path, key, bucket=None):
    data = {
        k: data[k]
        for k in [
            "private_key",
            "private_key_id",
            "token_uri",
            "client_email",
        ]
    }
    encrypt_fields(data, ("private_key_id", "private_key"), key)
    if bucket is not None:
        data["bucket"] = bucket
    with open(path, "wb") as f:
        pickle.dump(data, f)


def unpickle_client_secret_file(path, key):
    with open(path, "rb") as f:
        data = pickle.load(f)

    decrypt_fields(
        data["installed"],
        ("client_secret",),
        key,
    )
    return data


def pickle_client_secret_file(data, path, key):
    encrypt_fields(data["installed"], ("client_secret",), key)
    with open(path, "wb") as f:
        pickle.dump(data, f)


def get_credentials_via_client_secrets_file(pickled_client_secret_file, key):
    data = unpickle_client_secret_file(pickled_client_secret_file, key)
    appflow = flow.InstalledAppFlow.from_client_config(
        data,
        scopes=["https://www.googleapis.com/auth/devstorage.read_write"],
    )
    appflow.run_local_server()
    return appflow.credentials


def gen_key(path):
    return Fernet.generate_key()


def get_cipher(key):
    if os.path.isfile(key):
        with open(key, "rb") as f:
            return Fernet(f.read())
    return Fernet(key)


def default_bucket_from_service_account_file(service_account_path):
    if not os.path.isfile(service_account_path):
        return None
    with open(service_account_path, "rb") as f:
        data = pickle.load(f)
    return data.pop("bucket") if "bucket" in data else None
