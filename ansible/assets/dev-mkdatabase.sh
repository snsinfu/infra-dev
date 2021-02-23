#!/bin/sh -eu

name="$1"
database="${name}"
database_host="postgres.internal"
database_user="${name}"
database_pass="$(openssl rand -hex 16)"
kube_namespace="${name}"
kube_secret="postgres"

psql \
  -w \
  -v ON_ERROR_STOP=1 \
  -v database="${database}" \
  -v user="${database_user}" \
  -v password="${database_pass}" \
  postgres \
<< END
CREATE DATABASE :"database";
CREATE USER :"user" WITH PASSWORD :'password';
GRANT ALL PRIVILEGES ON DATABASE :"database" TO :"user";
END

kubectl apply -f - << END
---
apiVersion: v1
kind: Namespace
metadata:
  name: ${kube_namespace}
---
apiVersion: v1
kind: Secret
metadata:
  namespace: ${kube_namespace}
  name: ${kube_secret}
stringData:
  host: ${database_host}
  database: ${database}
  username: ${database_user}
  password: ${database_pass}
  uri: postgresql://${database_user}:${database_pass}@${database_host}/${database}
END
