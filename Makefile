# Sublime Text
st_submodule := sublime-text
st_site := $(st_submodule)/www.sublimetext.com
st_site_index := $(st_site)/docs/index.html
st_docset := sublime-text.docset
st_built_path := $(st_site)/$(st_docset)

# Sublime Merge
sm_submodule := sublime-merge
sm_site := $(sm_submodule)/www.sublimemerge.com
sm_site_index := $(sm_site)/docs/index.html
sm_docset := sublime-merge.docset
sm_built_path := $(sm_site)/$(sm_docset)

.PHONY: all
all: clean pre-build build

.PHONY: fix
pre-build: fix-html

.PHONY: fix-html
fix-html:
	python fix_html.py

build:
	yq -j . sublime-text-dashing.yml > $(st_site)/dashing.json
	cd $(st_site) \
	&& ~/go/bin/dashing build
	yq -j . sublime-merge-dashing.yml > $(sm_site)/dashing.json
	cd $(sm_site) \
	&& ~/go/bin/dashing build

.PHONY: clean
clean:
	[ -d "$(st_built_path)" ] && rm -r $(st_built_path) || true
	[ -f "$(st_site)/dashing.json" ] && rm $(st_site)/dashing.json || true
	[ -d "$(sm_built_path)" ] && rm -r $(sm_built_path) || true
	[ -f "$(sm_site)/dashing.json" ] && rm $(sm_site)/dashing.json || true
	git restore --recurse-submodules $(st_submodule) $(sm_submodule)
