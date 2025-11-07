submodule_path := SublimeText_Documentation
local_path := $(submodule_path)/www.sublimetext.com
local_index := $(local_path)/docs/index.html
built_path := $(local_path)/sublime-text.docset

.PHONY: all
all: clean pre-build build post-build

.PHONY: fix
pre-build: fix-html

.PHONY: fix-html
fix-html:
	python fix_html.py

build:
	yq -j . dashing.yml > $(local_path)/dashing.json
	cd $(local_path) \
	&& dashing build

.PHONY: post-build
post-build:
	find $(built_path) -iname '*.html' -exec \
		sed -i -Ee 's#(<a [^>]+></a><a [^>]+></a>)(<td[^>]*>)#\2\1#g' {} \;

.PHONY: clean
clean:
	git restore $(submodule_path) --recurse-submodules

.PHONY: clean-more
clean-more: clean
	rm -r $(built_path)
	rm $(local_path)/dashing.json
