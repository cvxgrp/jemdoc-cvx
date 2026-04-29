JEMDOC ?= $(realpath ../jemdoc)

DOCS=index syntax contact download revision using menu stuff extra example modelines htmlchanges latex tables

HDOCS=$(addsuffix .html, $(DOCS))
PHDOCS=$(addprefix html/, $(HDOCS))

.PHONY : update
update : $(PHDOCS)
	@echo -n 'Copying to (hidden) server...'
	@rsync -a --delete --copy-unsafe-links *.jemdoc html/* dist eqs ~/jemdoc/stage/
	@echo ' done.'

.PHONY : extra
extra :
	cp ~/.vim/syntax/jemdoc.vim dist/

.PHONY : docs
docs : html $(PHDOCS) html/jemdoc-cvx.css html/fonts

html :
	mkdir -p html

html/%.html : %.jemdoc MENU jemdoc.conf
	$(JEMDOC) -o $@ -c jemdoc.conf $<

# Copy the default theme stylesheet and its fonts next to the rendered html
# so that local previews (open html/index.html in a browser) work without
# extra setup. The CI deploy in .github/workflows/docs.yml stages these
# directly from css/ for the same reason.
html/jemdoc-cvx.css : ../css/jemdoc-cvx.css | html
	cp $< $@

html/fonts : ../css/fonts | html
	rm -rf $@
	cp -r $< $@

example.jemdoc : exampleIN.jemdoc procexample.py
	@echo 'making exampleIN'
	@./procexample.py

.PHONY : realupdate
realupdate : $(PHDOCS)
	@echo -n 'Copying to (hidden) server...'
	@rsync -a --delete --copy-unsafe-links *.jemdoc html/* dist ~/jemdoc/stage/
	@echo ' done.'
	@echo 'Copying to moa...'
	rsync -a --delete --copy-unsafe-links *.jemdoc ~/jemdoc/stage/ moa:/var/www/jemdoc/
	@echo ' done.'

.PHONY : clean
clean :
	-rm -f html/*.html
