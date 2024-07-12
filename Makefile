# Define variables
PNPM = pnpm
FLASK_APP = scripto
FLASK_ENV = development

# Default target: run the Flask app and tailwindcss_watch concurrently
all: .venv
	@$(MAKE) -j 2 run_flask tailwindcss_watch

# Run the Flask app in development mode
run_flask:
	flask run --debug

tailwindcss_watch:
	@$(PNPM) run tailwind_watch
