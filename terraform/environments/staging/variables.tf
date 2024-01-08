variable "project" {
  description = "The ID of the Google Cloud Project where resources will be deployed"
  type        = string
}

variable "db_host_project" {
  description = "The ID of the Google Cloud Project where PostgreSQL is deployed"
  type        = string
}

variable "region" {
  description = "The Google Cloud region where resources will be provisioned"
  type        = string
}

variable "storage_class" {
  description = "The storage class to be applied to the Google Cloud Storage Bucket"
  type        = string
}

variable "db_name" {
  description = "The name of the database in PostgreSQL"
  type        = string
}

variable "db_replication_name" {
  description = "The name of the replication process for the PostgreSQL database"
  type        = string
}

variable "db_publication_name" {
  description = "The name of the publication process for the PostgreSQL database"
  type        = string
}
