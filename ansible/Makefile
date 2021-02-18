ARTIFACTS = \
  _check.ok \
  _system.ok


.PHONY: all clean

all: _system.ok
	@:

clean:
	rm -f $(ARTIFACTS)

_check.ok:
	scripts/check.sh
	@touch $@

_system.ok: playbooks/system.yml _check.ok
	ansible-playbook $<
	@touch $@
