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

.PHONY : clean
clean :
	@make -C www clean
