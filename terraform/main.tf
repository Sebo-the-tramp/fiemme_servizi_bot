terraform {
  backend "remote" {
    organization = "system-engineering-lab"
    workspaces {
      name = "fiemme_servizi_bot"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region     = "eu-west-1"
}