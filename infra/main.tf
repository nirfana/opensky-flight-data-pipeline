terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = ">= 3.0.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "data_net" {
  name = "data_pipeline_network"
}

resource "docker_volume" "postgres_data" {
  name = "postgres_data_vol"
}