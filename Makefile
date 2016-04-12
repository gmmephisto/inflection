.PHONY: sources srpm rpm clean

DIST    ?= epel-6-x86_64

PROGRAM := inflection
PACKAGE := python-$(PROGRAM)
VERSION := $(shell rpm -q --qf "%{version}\n" --specfile $(PACKAGE).spec | head -1)
RELEASE := $(shell rpm -q --qf "%{release}\n" --specfile $(PACKAGE).spec | head -1)


sources: clean
	@git archive --format=tar --prefix="$(PROGRAM)-$(VERSION)/" \
		$(shell git rev-parse --verify HEAD) | gzip > "$(PROGRAM)-$(VERSION).tar.gz"

srpm: sources
	@mkdir -p srpms/
	rpmbuild -bs --define "_sourcedir $(CURDIR)" \
		--define "_srcrpmdir $(CURDIR)/srpms" $(PACKAGE).spec

rpm:
	@mkdir -p rpms/$(DIST)
	/usr/bin/mock -r $(DIST) \
		--rebuild srpms/$(PACKAGE)-$(VERSION)-$(RELEASE).src.rpm \
		--resultdir rpms/$(DIST) --no-cleanup-after

copr: srpm
	@copr-cli build --nowait miushanov/pyaddons \
		srpms/$(PACKAGE)-$(VERSION)-$(RELEASE).src.rpm

clean:
	@rm -rf .venv/ build/ dist/ *.egg* .eggs/ rpms/ srpms/ *.tar.gz *.rpm
