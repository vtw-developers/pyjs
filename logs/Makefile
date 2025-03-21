.PHONY: clean
timestamp := $(shell date +%Y-%m-%d-%H-%M-%S)
new_directory := ./$(timestamp)

# be cautious when using this
clean:
	@read -p "Are you sure you want to delete all files as specified? [y/N] " confirm && [ "$$confirm" = "y" ]

	# This command finds all files (excluding directories) starting from the current directory,
	# with a minimum depth of 2 (i.e., it skips the current directory and its immediate subdirectories).
	# It excludes files named '.gitignore' and prints the paths of the found files before deleting them.
	find . -mindepth 2 -type f ! -name '.gitignore' -print -delete

	rm -fv pirel.log

backup:
	# Create the directory specified by the variable 'new_directory' if it doesn't already exist
	mkdir -p $(new_directory)

	# Find all files (excluding '.gitignore') starting from the current directory, 
	# but not including files in the 'new_directory' path, and copy them to 'new_directory' 
	# while preserving their directory structure
	find . -mindepth 2 -type f ! -name '.gitignore' -not -path "$(new_directory)/*" -exec cp --parents {} $(new_directory) \;

	# Copy the file 'pirel.log' to 'new_directory'
	cp pirel.log $(new_directory)
