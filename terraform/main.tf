terraform {
  backend "s3" {}
}

resource "hcloud_server" "javelin" {
  name        = "javelin"
  location    = var.server_location
  server_type = var.server_type
  image       = data.hcloud_image.debian.id
  ssh_keys    = data.hcloud_ssh_keys.all.ssh_keys.*.id
  user_data   = file("assets/cloudinit.yml")
}

data "hcloud_image" "debian" {
  with_selector = "image=debian-10-zfs"
}

data "hcloud_ssh_keys" "all" {
}
