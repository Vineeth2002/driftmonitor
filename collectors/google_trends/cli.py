"""Small wrapper to expose the collector as a module-level CLI."""
from .collector import main_cli

if __name__ == "__main__":
    main_cli()
