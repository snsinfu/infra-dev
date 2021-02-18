ARTIFACTS = \
  _check.ok \
  _system.ok \
  _wireguard.ok \
  _wireguard_clients.ok


.PHONY: all clean

all: _wireguard_clients.ok
	@:

clean:
	rm -f $(ARTIFACTS)

_check.ok:
	scripts/check.sh
	@touch $@

_system.ok: playbooks/system.yml _check.ok
	ansible-playbook $<
	@touch $@

_wireguard.ok: playbooks/wireguard.yml _system.ok
	ansible-playbook $<
	@touch $@

_wireguard_clients.ok: playbooks/wireguard_clients.yml _wireguard.ok
	ansible-playbook $<
	@touch $@
