ARTIFACTS = \
  _check.ok \
  _system.ok \
  _wireguard.ok \
  _wireguard_clients.ok \
  _internal_dns.ok \
  _internal_nfs.ok \
  _k3s_server.ok \
  _postgres.ok \
  _dev_users.ok \
  _monitoring.ok \
  _firewall.ok


.PHONY: all clean

all: _k3s_server.ok _dev_users.ok _monitoring.ok
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

_internal_dns.ok: playbooks/internal_dns.yml _system.ok _wireguard.ok
	ansible-playbook $<
	@touch $@

_internal_nfs.ok: playbooks/internal_nfs.yml _system.ok _wireguard.ok
	ansible-playbook $<
	@touch $@

_k3s_server.ok: playbooks/k3s_server.yml _wireguard.ok _internal_dns.ok _internal_nfs.ok
	ansible-playbook $<
	@touch $@

_postgres.ok: playbooks/postgres.yml _system.ok _wireguard.ok
	ansible-playbook $<
	@touch $@

_dev_users.ok: playbooks/dev_users.yml _system.ok _postgres.ok
	ansible-playbook $<
	@touch $@

_monitoring.ok: playbooks/monitoring.yml _system.ok
	ansible-playbook $<
	@touch $@

_firewall.ok: playbooks/firewall.yml _system.ok _wireguard.ok _wireguard_clients.ok
	ansible-playbook $<
	@touch $@
