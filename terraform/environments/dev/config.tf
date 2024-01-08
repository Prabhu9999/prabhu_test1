terraform {
  cloud {
    organization = "ridezoomo"

    workspaces {
      name = "dna-fms-dw-cloudsql-setup-dev"
    }
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.10.1"
    }
  }
}
