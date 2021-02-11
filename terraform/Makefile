ARTIFACTS = \
  _init.ok \
  _server.ok

.PHONY: all clean destroy ssh

all: _server.ok
	@:

clean: destroy
	rm -f $(ARTIFACTS)

destroy:
	terraform destroy -auto-approve
	@rm -f _server.ok

ssh: _server.ok
	ssh admin@$$(terraform output -raw javelin_ip)

_init.ok: _backend.conf
	terraform init -backend-config _backend.conf
	@touch $@

_server.ok: _init.ok
	terraform apply -auto-approve
	@touch $@
