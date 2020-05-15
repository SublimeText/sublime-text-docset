source_link := https://www.sublimetext.com/docs/index.html
local_path := ./www.sublimetext.com
local_index := $(local_path)/docs/index.html
built_path := ./sublime-text.docset

.PHONY: all
all: clean download pre-build build post-build

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
	find $(local_path) -iname '*.html' -exec sed -i -e '/<header>/,/<\/header>/d' {} \;
	python prefix_methods.py

.PHONY: fix-css
fix-css:
	$(shell for f in $$(ls $(local_path)/*.css\?*); do mv "$$f" "$${f%\?*}"; done )

build:
	dashing build

.PHONY: post-build
post-build:
	find $(built_path) -iname '*.html' -exec \
		sed -i -Ee 's#(<a [^>]+></a><a [^>]+></a>)(<td[^>]*>)#\2\1#g' {} \;

.PHONY: clean
clean:
	-rm -r $(local_path)

.PHONY: clean-more
clean-more: clean
	-rm -r $(built_path)
