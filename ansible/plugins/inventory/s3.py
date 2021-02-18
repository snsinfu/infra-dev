DOCUMENTATION = """
    name: s3
    plugin_type: inventory
    short_description: Load modular inventory files from S3
    options:
      plugin:
        type: str
        required: true
        choices:
          - s3
      bucket:
        type: str
        env:
          - name: ANSIBLE_INVENTORY_S3_BUCKET
      overrides:
        type: list
        default: []
"""

from ansible.errors import AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin

try:
    import boto3
except ImportError:
    raise AnsibleError("s3 inventory plugin requires boto3")


class InventoryModule(BaseInventoryPlugin):
    NAME = "s3"

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)

        self._read_config_data(path)
        bucket_name = self.get_option("bucket")
        overrides = self.get_option("overrides")

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(bucket_name)

        for override in overrides:
            key = override["key"]
            obj = bucket.Object(key)
            try:
                obj_body = obj.get()["Body"]
            except s3.meta.client.exceptions.NoSuchKey:
                if override.get("optional"):
                    continue
                raise

            filename = f"<s3>:{key}"
            data = loader.load(obj_body, filename)

            if data:
                parse_override(self.inventory, data)


def parse_override(inventory, data):
    groups_data = data.get("groups")
    if groups_data:
        parse_groups(inventory, groups_data)

    vars_data = data.get("vars")
    if vars_data:
        parse_vars(inventory, vars_data)


def parse_groups(inventory, groups_data):
    for group_name, group_data in groups_data.items():
        group = inventory.add_group(group_name)

        for host_name in group_data.get("hosts", []):
            inventory.add_host(host_name, group)

        for child_name in group_data.get("children", []):
            child = inventory.add_group(child_name)
            inventory.add_child(group, child)


def parse_vars(inventory, vars_data):
    common_vars = vars_data.get("common", {})
    hosts_data = vars_data.get("host", {})
    groups_data = vars_data.get("group", {})

    for host_name in inventory.hosts:
        for k, v in common_vars.items():
            inventory.set_variable(host_name, k, v)

    for host_name, host_vars in hosts_data.items():
        for k, v in host_vars.items():
            inventory.set_variable(host_name, k, v)

    for group_name, group_vars in groups_data.items():
        for k, v in group_vars.items():
            inventory.set_variable(group_name, k, v)
