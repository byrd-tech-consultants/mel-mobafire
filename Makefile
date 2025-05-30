# BBCode Preprocessor Makefile
# Processes .bbc files and outputs clean .txt files

# Directories
SRC_DIR := src
BUILD_DIR := build
CLEAN_DIR := $(BUILD_DIR)/clean

# Python script
PREPROCESSOR := bbcode_preprocessor.py

# Find all .bbc files in source directory
BBC_FILES := $(wildcard $(SRC_DIR)/*.bbc)
# If you have .bbcode files instead, use this line:
# BBC_FILES := $(wildcard $(SRC_DIR)/*.bbcode)

# Generate corresponding .txt files in clean directory
TXT_FILES := $(patsubst $(SRC_DIR)/%.bbc,$(CLEAN_DIR)/%.txt,$(BBC_FILES))
# If using .bbcode files, use this line instead:
# TXT_FILES := $(patsubst $(SRC_DIR)/%.bbcode,$(CLEAN_DIR)/%.txt,$(BBC_FILES))

# Default target
.PHONY: all
all: $(TXT_FILES)

# Rule to process .bbc files into .txt files
$(CLEAN_DIR)/%.txt: $(SRC_DIR)/%.bbc $(PREPROCESSOR) | $(CLEAN_DIR)
	@echo "Processing: $< -> $@"
	python3 $(PREPROCESSOR) --remove-tabs "$<" "$@"

# Create directories if they don't exist
$(CLEAN_DIR):
	@mkdir -p $(CLEAN_DIR)

# Clean build directory
.PHONY: clean
clean:
	@echo "Cleaning build directory..."
	rm -rf $(BUILD_DIR)

# Clean and rebuild everything
.PHONY: rebuild
rebuild: clean all

# Show what files will be processed
.PHONY: list
list:
	@echo "Source files found:"
	@for file in $(BBC_FILES); do echo "  $$file"; done
	@echo ""
	@echo "Will generate:"
	@for file in $(TXT_FILES); do echo "  $$file"; done

# Install/check dependencies
.PHONY: check
check:
	@echo "Checking dependencies..."
	@python3 --version || (echo "Error: Python not found" && exit 1)
	@test -f $(PREPROCESSOR) || (echo "Error: $(PREPROCESSOR) not found" && exit 1)
	@echo "✓ All dependencies found"

# Watch for changes (requires inotify-tools on Linux)
.PHONY: watch
watch:
	@echo "Watching for changes in $(SRC_DIR)..."
	@while inotifywait -e modify,create,delete $(SRC_DIR)/*.bbc 2>/dev/null; do \
		echo "Changes detected, rebuilding..."; \
		$(MAKE) all; \
	done

# Help target
.PHONY: help
help:
	@echo "BBCode Preprocessor Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all      - Process all .bbc files to .txt (default)"
	@echo "  clean    - Remove build directory"
	@echo "  rebuild  - Clean and build everything"
	@echo "  list     - Show files that will be processed"
	@echo "  check    - Check if dependencies are available"
	@echo "  watch    - Watch for file changes and auto-rebuild"
	@echo "  help     - Show this help message"
	@echo ""
	@echo "Directory structure:"
	@echo "  $(SRC_DIR)/     - Source .bbc files"
	@echo "  $(BUILD_DIR)/   - Build output"
	@echo "  $(CLEAN_DIR)/   - Clean .txt files"