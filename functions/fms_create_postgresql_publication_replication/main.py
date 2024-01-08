'''
__author__ = 'Prabhu Kiran'
__contributors__=
__created_date__ = '2023-07-13'
__version__ = '1.1'
    Version:
        1.0 : 2023-07-13 - PK - initial release
        1.1 : 2023-12-13 - PK - added SQL commands to grant required privileges 
                                for db_reporting_user on PostgreSQL databasse
                                
__description__
1. Connect to PostgreSQL DB using Cloud SQL Connector
2. Creates publication and logical replication for a PostgreSQL database on Google Cloud SQL
3. Grants required privileges to the reporting user
'''

import os
import logging
import sqlalchemy

import google.cloud.logging
from google.cloud import secretmanager
from google.cloud.sql.connector import Connector

from secret_manager import add_secret_version, get_latest_secret

# Instantiates logging client
logging_client = google.cloud.logging.Client()
# Retrieves a Cloud Logging handler with the Python logging module.
logging_client.setup_logging()


# Constants
PROJECT_ID = os.getenv('project_id')
DB_HOST_PROJECT_ID = os.getenv('db_host_project_id')
DB_NAME = os.getenv('db_name')
REPLICATION_NAME = os.getenv('db_replication_name')
PUBLICATION_NAME = os.getenv('db_publication_name')


def create_db_connection(connector: Connector, instance_connection_name: str, db_user: str, db_pass: str, db_name: str) -> sqlalchemy.engine.Connection:
    '''
    Create a database connection using the Cloud SQL Connector.

    Args:
        connector (Connector): An instance of Google Cloud SQL Connector to create connections.
        instance_connection_name (str): The instance connection name of the Cloud SQL database.
        db_user (str): The database username.
        db_pass (str): The database password.
        db_name (str): The name of the database.

    Returns:
        sqlalchemy.engine.Connection: A connection object representing the database connection.
    '''

    return connector.connect(
        instance_connection_name,
        'pg8000',
        user=db_user,
        password=db_pass,
        db=db_name
    )


def init_connection_pool(connector: Connector) -> sqlalchemy.engine.Engine:
    '''
    Initialize a connection pool for a Cloud SQL instance of Postgres using Cloud SQL Python Connector.
    This function fetches database connection details from Google Cloud Secret Manager.

    Args:
        connector (Connector): An instance of Google Cloud SQL Connector to create connections.

    Returns:
        sqlalchemy.engine.Engine: An instance of SQLAlchemy Engine which represents the initialized 
        connection pool to the Postgres database instance.
        str: Database core service username.
        str: Database reporting service username.
    '''

    # Fetch secrets from Google Cloud Secret Manager
    instance_connection_name = get_latest_secret(DB_HOST_PROJECT_ID, 'fms_database_connection_name')
    db_core_user = get_latest_secret(DB_HOST_PROJECT_ID, 'core_service_db_username')
    db_core_pass = get_latest_secret(DB_HOST_PROJECT_ID, 'core_service_db_password')
    db_reporting_user = get_latest_secret(DB_HOST_PROJECT_ID, 'reporting_service_db_username')

    # Create a connection using the Cloud SQL Connector
    conn = create_db_connection(connector, instance_connection_name, db_core_user, db_core_pass, DB_NAME)

    # Create a connection pool
    pool = sqlalchemy.create_engine('postgresql+pg8000://',
                                    creator=lambda: conn)

    return pool, db_core_user, db_reporting_user


def create_publication_and_replication(connector: Connector):
    '''
    This function creates a publication and replication for the PostgreSQL database on Google Cloud SQL.

    Args:
        connector (Connector): An instance of Google Cloud SQL Connector to create connections.
    '''

    # Initialize the connection pool
    pool, db_core_user, db_reporting_user = init_connection_pool(connector)

    # SQL commands for creating publication and replication
    sql_commands = [
        f'ALTER USER {db_core_user} WITH REPLICATION',
        f'CREATE PUBLICATION {PUBLICATION_NAME} FOR ALL TABLES',
        f"SELECT PG_CREATE_LOGICAL_REPLICATION_SLOT('{REPLICATION_NAME}', 'pgoutput')",
        f'GRANT CONNECT ON DATABASE {DB_NAME} TO {db_reporting_user};'
        f'GRANT SELECT ON ALL TABLES IN SCHEMA PUBLIC TO {db_reporting_user}',
        f'GRANT USAGE ON SCHEMA PUBLIC TO {db_reporting_user}',
        f'ALTER DEFAULT PRIVILEGES IN SCHEMA PUBLIC GRANT SELECT ON TABLES TO {db_reporting_user}'
    ]

    # Execute each command
    for command in sql_commands:
        try:
            with pool.connect() as db_conn:
                db_conn.execute(sqlalchemy.text(command))
                logging.info(f'Successful - Executed command: {command}')
                db_conn.commit()
        except Exception as error:
            logging.error(f'Failed - {str(error)}')
            db_conn.rollback()
            raise RuntimeError(f'Failed - {str(error)}')


def main(request):
    '''
    The main function to execute the necessary steps:
    - Initialize Cloud SQL Python Connector
    - Create publication and replication
    - Grant necessary privileges to reporting user

    Args:
        request: A request object. Not used in this function, but required for GCF entry point.
    '''

    # Initialize Cloud SQL Python Connector
    with Connector() as connector:
        # Create publication and replication
        create_publication_and_replication(connector)
