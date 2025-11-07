source_link := https://www.sublimetext.com/docs/index.html
local_path := www.sublimetext.com
local_index := $(local_path)/docs/index.html
built_path := $(local_path)/sublime-text.docset

.PHONY: all
all: clean download pre-build build

.PHONY: download
download:
	-wget \
		--convert-links \
		--recursive \
		--page-requisites \
		--no-parent \
		--timestamping \
		"$(source_link)"

.PHONY: fix
pre-build: fix-html fix-css

.PHONY: fix-html
fix-html:
	python fix_html.py

.PHONY: fix-css
fix-css:
	$(shell for f in $$(ls $(local_path)/*.*\?*); do mv "$$f" "$${f%\?*}"; done )
	$(shell for f in $$(ls $(local_path)/**/*.*\?*); do mv "$$f" "$${f%\?*}"; done )

build:
	yq -j . dashing.yml > $(local_path)/dashing.json
	cd $(local_path) \
	&& dashing build

.PHONY: clean
clean:
	-rm -r $(local_path)

.PHONY: clean-more
clean-more: clean
	-rm -r $(built_path)
