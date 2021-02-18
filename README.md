## Instruction

### 1. S3 bucket

This project uses AWS S3 to store Terraform states and Ansible inventory.

Open the S3 dashboard and create a new bucket. Then, go to the IAM dashboard
and create a policy for accessing the bucket:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject", "s3:ListBucket"],
            "Resource": [
                "arn:aws:s3:::YOUR_BUCKET",
                "arn:aws:s3:::YOUR_BUCKET/*",
            ]
        }
    ]
}
```

Next, create a group and attach the policy to the group. Then, create a user
with "program access" and add the user to the group. Take note of the access
key ID and the access secret and add them to `.env`:

```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
```

We'll use the bucket as a storage of Ansible inventory. An Ansible plugin will
need to access to the bucket, so add the following variable to `.env`:

```
ANSIBLE_INVENTORY_S3_BUCKET=
```


### 2. Hetzner Cloud

Create a Hetzner Cloud project. Go to the security page and insert SSH keys.
Generate an API token and add it to `.env`:

```
HCLOUD_TOKEN=
```

Now, encrypt the env file:

```console
$ gpg --symmetric .env
$ rm .env
```

Load the environment variables. You may want to use [dotenv][dotenv].

```
$ dotenv
dotenv: Loading .env.gpg
```

Then, [create a Debian ZFS image][zfsimage].

[dotenv]: https://github.com/snsinfu/dotenv
[zfsimage]: https://github.com/snsinfu/hetzner-zfs-image


### 3. Create server

Enter the `terraform` directory and create Terraform backend config file named
`_backend.conf`. Set the name of the S3 bucket you created to `bucket`:

```
bucket = "YOUR_BUCKET"
key = "terraform/state"
```

Then, type `make` to spin up the server. Check ssh connectivity.

```console
$ make
$ make ssh
```


### 4. Ansible

Enter the `ansible` directory. You need to define your inventory and variables.
