resource "google_storage_bucket" "bucket_gcf_archives" {
  name          = "${var.project}-functions"
  project       = var.project
  storage_class = var.storage_class
  location      = var.region
  force_destroy = true
}

data "archive_file" "postgresql_gcf_config_source" {
  type        = "zip"
  source_dir  = "../../../functions/fms_create_postgresql_publication_replication"
  output_path = "../../../functions/fms_create_postgresql_publication_replication.zip"

  depends_on = [
    google_storage_bucket.bucket_gcf_archives
  ]
}

resource "google_storage_bucket_object" "postgresql_gcf_config_object" {
  name   = "fms_create_postgresql_publication_replication.zip"
  bucket = google_storage_bucket.bucket_gcf_archives.name
  source = data.archive_file.postgresql_gcf_config_source.output_path

  depends_on = [
    google_storage_bucket.bucket_gcf_archives,
    data.archive_file.postgresql_gcf_config_source
  ]
}

resource "google_cloudfunctions_function" "create_postgresql_publication_replication" {
  project                      = var.project
  region                       = var.region
  name                         = "fms_create_postgresql_publication_replication"
  runtime                      = "python310"
  timeout                      = 540
  available_memory_mb          = 512
  max_instances                = 1
  trigger_http                 = true
  https_trigger_security_level = "SECURE_ALWAYS"
  ingress_settings             = "ALLOW_INTERNAL_ONLY"
  source_archive_bucket        = google_storage_bucket.bucket_gcf_archives.name
  source_archive_object        = google_storage_bucket_object.postgresql_gcf_config_object.name
  entry_point                  = "main"

  environment_variables = {
    project_id          = var.project
    db_host_project_id  = var.db_host_project
    db_name             = var.db_name
    db_replication_name = var.db_replication_name
    db_publication_name = var.db_publication_name
  }

  depends_on = [google_storage_bucket.bucket_gcf_archives,
    data.archive_file.postgresql_gcf_config_source,
    google_storage_bucket_object.postgresql_gcf_config_object
  ]
}
