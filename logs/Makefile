.PHONY: clean
timestamp := $(shell date +%Y-%m-%d-%H-%M-%S)
new_directory := ./$(timestamp)

# be cautious when using this
clean:
	@read -p "Are you sure you want to delete all files as specified? [y/N] " confirm && [ "$$confirm" = "y" ]

	find learn-rules/ -type f ! -name '.gitignore' -print -delete
	find pirel/ -type f ! -name '.gitignore' -print -delete
	rm -fv pirel.log

# make backup name=debug-03
backup:
	# Ensure the 'name' variable is provided
	@if [ -z "$(name)" ]; then \
		echo "Error: 'name' variable is not set. Use 'make backup name=<name>'."; \
		exit 1; \
	fi

	# Create the directory specified by the variable 'name' if it doesn't already exist
	mkdir -p $(name)

	cp -rv learn-rules $(name)
	cp -rv pirel $(name)
	cp pirel.log $(name)

	rm $(name)/learn-rules/.gitignore
	rm $(name)/pirel/.gitignore

	# zip and move to archive directory
	zip -r $(name).zip $(name)
	mv $(name).zip archive/
	rm -rf $(name)

# make restore_backup name=/path/to/backup.zip/in/archive
restore_backup:
	# Ensure the 'name' variable is provided
	@if [ -z "$(name)" ]; then \
		echo "Error: 'name' variable is not set. Use 'make backup name=<name>'."; \
		exit 1; \
	fi

	# Ensure the backup directory exists before attempting to restore
	if [ -f "archive/$(name).zip" ]; then \
		# Restore all files from the backup directory to their original locations \
		cp archive/$(name).zip .; \
		unzip $(name).zip; \
		rm $(name).zip; \
		cd $(name) && find . -type f -exec cp --parents {} ../ \; ; \
		cd .. && rm -rf $(name); \
	else \
		echo "Backup file 'archive/$(name).zip' does not exist. Cannot restore."; \
	fi

# alias
restore: restore_backup

format_json:
	@directory="pirel"; \
	total=$$(find $$directory -type f -name '*.json' | wc -l); \
	count=0; \
	echo "Total JSON files to format: $$total"; \
	find $$directory -type f -name '*.json' | while read -r file; do \
		count=$$(($$count + 1)); \
		echo "Formatting $$count/$$total: $$file"; \
		jq . "$$file" > "$$file.tmp" && mv "$$file.tmp" "$$file"; \
	done

	@directory="learn-rules"; \
	total=$$(find $$directory -type f -name '*.json' | wc -l); \
	count=0; \
	echo "Total JSON files to format: $$total"; \
	find $$directory -type f -name '*.json' | while read -r file; do \
		count=$$(($$count + 1)); \
		echo "Formatting $$count/$$total: $$file"; \
		jq . "$$file" > "$$file.tmp" && mv "$$file.tmp" "$$file"; \
	done
