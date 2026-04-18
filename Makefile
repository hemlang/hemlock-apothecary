# hemlock-apothecary: Formulary SFT dataset generation and parity verification.

HEMLOCK_REPO ?= $(HOME)/Projects/hemlock
HEMLOCK      := $(HEMLOCK_REPO)/hemlock
HEMLOCKC     := $(HEMLOCK_REPO)/hemlockc
STDLIB_DIR   := hemlock/stdlib
SEED_FILES   := $(shell find $(STDLIB_DIR) -name '*.hml' 2>/dev/null | sort)

.PHONY: all formulary check-seeds clean help

all: formulary

formulary: check-seeds
	python3 generate_formulary.py

# Parity-first: every Formulary seed must produce byte-identical output under
# the interpreter and the compiled binary. Fails fast on any mismatch.
check-seeds:
	@if [ ! -x "$(HEMLOCK)" ] || [ ! -x "$(HEMLOCKC)" ]; then \
	  echo "error: $(HEMLOCK) or $(HEMLOCKC) not found or not executable."; \
	  echo "       Build them with: (cd $(HEMLOCK_REPO) && make all)"; \
	  exit 2; \
	fi
	@pass=0; fail=0; failed_files=""; \
	for f in $(SEED_FILES); do \
	  i=$$(timeout 15 $(HEMLOCK) $$f 2>&1); \
	  bin=$$(mktemp); \
	  timeout 20 $(HEMLOCKC) $$f -o $$bin >/dev/null 2>&1; \
	  if [ -x $$bin ]; then c=$$(timeout 15 $$bin 2>&1); else c="[compile failed]"; fi; \
	  rm -f $$bin; \
	  if [ "$$i" = "$$c" ]; then \
	    pass=$$((pass + 1)); \
	    printf "  [OK]       %s\n" "$$f"; \
	  else \
	    fail=$$((fail + 1)); \
	    failed_files="$$failed_files $$f"; \
	    printf "  [MISMATCH] %s\n" "$$f"; \
	    printf "    INTERP : %s\n" "$$(echo "$$i" | head -3 | tr '\n' '|')"; \
	    printf "    COMPILE: %s\n" "$$(echo "$$c" | head -3 | tr '\n' '|')"; \
	  fi; \
	done; \
	echo ""; \
	echo "  $$pass passed, $$fail failed"; \
	if [ $$fail -gt 0 ]; then exit 1; fi

clean:
	rm -f hemlock_apothecary_formulary.jsonl

help:
	@echo "Targets:"
	@echo "  formulary    Verify every stdlib seed under both backends, then generate"
	@echo "               hemlock_apothecary_formulary.jsonl"
	@echo "  check-seeds  Parity-check every hemlock/stdlib/**/*.hml (interp vs compiled),"
	@echo "               exit non-zero on any mismatch"
	@echo "  all          Alias for formulary"
	@echo "  clean        Remove generated JSONL"
	@echo ""
	@echo "Variables:"
	@echo "  HEMLOCK_REPO  Path to hemlock repo root (default: ~/Projects/hemlock)"
