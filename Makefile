lint:
	dotenv-linter src/app/.env.ci
	flake8 src
	cd src && mypy

test:
	mkdir -p src/app/static
	cd src && ./manage.py compilemessages
	cd src && pytest --dead-fixtures
	cd src && pytest -x
