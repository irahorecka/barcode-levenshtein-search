black: ## Black format every python file to line length 100
	find . -type f -name "*.py" | xargs black --line-length=100;
	find . -type f -name "*.py" | xargs absolufy-imports;
	make clean;

clean: ## Recursively remove pycache files.
	find . -type d -name "__pycache__" | xargs rm -r;
	find . -type f -name ".DS_Store" | xargs rm -r;
