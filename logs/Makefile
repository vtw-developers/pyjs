.PHONY: clean

# be cautious when using this
clean:
	@read -p "Are you sure you want to delete all files as specified? [y/N] " confirm && [ "$$confirm" = "y" ]

	# This command finds all files (excluding directories) starting from the current directory,
	# with a minimum depth of 2 (i.e., it skips the current directory and its immediate subdirectories).
	# It excludes files named '.gitignore' and prints the paths of the found files before deleting them.
	find . -mindepth 2 -type f ! -name '.gitignore' -print -delete

	rm -fv pirel.log