TARGETS := ci build test verify image
.PHONY: $(TARGETS) $(TEST_TARGETS) validation-test clean help

$(TARGETS):
	@./scripts/entry.sh $@

validation-test: .dapper
	@./.dapper -f Dockerfile.test.dapper

clean:
	@./scripts/clean.sh

help:
	@echo "Usage:"
	@echo "    make build           - Build 'hangar' executable files in 'bin' folder"
	@echo "    make test            - Run hangar unit test"
	@echo "    make build-test      - Run hangar build test"
	@echo "    make validation-test - Run hangar validation test"
	@echo "    make clean           - Remove generated files"
	@echo "    make help            - Show this message"
