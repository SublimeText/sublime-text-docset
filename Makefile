submodule_path := SublimeText_Documentation
local_path := $(submodule_path)/www.sublimetext.com
local_index := $(local_path)/docs/index.html
docset := sublime-text.docset
dashing_json := $(local_path)/dashing.json
built_path := $(local_path)/$(docset)

.PHONY: all
all: clean pre-build build

.PHONY: fix
pre-build: fix-html

.PHONY: fix-html
fix-html:
	python fix_html.py

build:
	yq -j . dashing.yml > $(dashing_json)
	cd $(local_path) \
	&& dashing build

.PHONY: clean
clean:
	[ -d "$(built_path)" ] && rm -r $(built_path) || true
	[ -f "$(dashing_json)" ] && rm $(dashing_json) || true
	git restore $(submodule_path) --recurse-submodules
