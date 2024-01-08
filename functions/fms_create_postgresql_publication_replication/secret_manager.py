'''
__author__ = 'Prabhu Kiran'
__contributors__=
__created_date__ = '2023-02-02'
__version__ = '1.2'
    Version:
        1.0 : 2023-02-02 - PK - initial release
        1.1 : 2023-04-13 - PK - added logic to generate new version for a given secret
        1.2 : 2023-12-13 - PK - reordered the initials
__description__
Library module that contains api methods to interact with secret manager.
Currently mapped methods are,
- Get the latest secret version data
- Generate new version for a secret
'''

from google.cloud import secretmanager


def add_secret_version(project_id, secret_id, secret_data):
    '''
    Add a new secret version to the given secret with the provided payload.

    Args:
        project_id (string): The Google Cloud project ID where the secret will be stored.
        secret_id (string): The unique identifier for the secret.
        secret_data (string): The data to be stored as the secret.

    Returns:
        The created secret object, or None if an error occurred.
    '''

    # Create the Secret Manager client
    sm_client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    parent = sm_client.secret_path(project_id, secret_id)

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    secret_data = secret_data.encode('UTF-8')

    # Add the secret version.
    response = sm_client.add_secret_version(request={'parent': parent, 'payload': { 'data': secret_data}})

    # Print the new secret version name.
    print('Added secret version: {}'.format(response.name))


def get_latest_secret(project_id, secret_id):
    '''
    Access the latest secret version if one exists.

    Args:
        project_id (string): GCP project_id
        secret_id (string): Secret name

    Returns:
        Decrypted or plain secret key
    '''

    # Create the Secret Manager client
    sm_client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = f'projects/{project_id}/secrets/{secret_id}/versions/latest'

    # Access the secret version
    response = sm_client.access_secret_version(request={'name': name})
    secret_key = response.payload.data.decode('UTF-8')

    return secret_key
