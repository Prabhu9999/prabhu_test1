module "create_publication_replication" {
  source              = "../../modules/db_publication_replication"
  project             = var.project
  db_host_project     = var.db_host_project
  region              = var.region
  storage_class       = var.storage_class
  db_name             = var.db_name
  db_replication_name = var.db_replication_name
  db_publication_name = var.db_publication_name
}
