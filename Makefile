.PHONY : update
update :
	@make -C www update

.PHONY : realupdate
realupdate :
	@make -C www realupdate

.PHONY : docs
docs :
	@make -C www docs

.PHONY : test
test :
	uv run pytest tests/

.PHONY : lint
lint :
	uv run ruff check .

# Bump the version across jemdoc (canonical __version__), pyproject.toml,
# and package.json. Usage: make bump-version VERSION=X.Y.Z
.PHONY : bump-version
bump-version :
	@if [ -z "$(VERSION)" ]; then echo "Usage: make bump-version VERSION=X.Y.Z"; exit 1; fi
	@python3 scripts/bump_version.py $(VERSION)
	@uv lock --quiet 2>/dev/null || true

.PHONY : clean
clean :
	@make -C www clean
