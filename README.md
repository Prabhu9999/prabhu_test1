# **PostgreSQL to BigQuery Data Stream Pre-requisite Setup**

This pipeline is designed to perform necessary preliminary actions for the creation of a data stream between PostgreSQL and BigQuery. It connects to a PostgreSQL database hosted on Google Cloud SQL and creates a publication and logical replication. This enables real-time data replication from PostgreSQL to BigQuery.

## **Getting Started**
This setup has been designed to automatically trigger deployment to GCP using Terraform when a push to a main occurs. To deploy this setup in a specific environment, push to the corresponding environment of this repo.

## **Installing/Deployment**
We use Terraform Cloud to manage and stores our state files. We have configured three separate workspaces in Terraform Cloud, each corresponding to a specific environment: production, development, and staging.

## **Dependency**
Make sure the Cloud SQL instance for PostgreSQL is deployed before deploying this repository.

## **Technical Details**
This pipeline connects to PostgreSQL DB using Cloud SQL Connector, creates publication, enables logical replication for the PostgreSQL database on Google Cloud SQL and grants required privileges to the reporting user

The setup implements the following stack:
- Python (3.10)
- Google Cloud SQL Connector
- Google Cloud Functions
- Terraform

## **Authors**
Prabhu - Initial pipeline and deployment work.
