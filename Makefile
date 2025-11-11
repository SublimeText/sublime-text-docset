# Shared
out_folder := out
install_path_linux := ~/.local/share/Zeal/Zeal/docsets

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
all: clean pre-build build post-build

pre-build:
	python fix_html.py

build:
	# Shared
	mkdir -p $(out_folder)
	# Sublime Text
	yq -j . sublime-text-dashing.yml > $(st_site)/dashing.json
	cd $(st_site) && dashing build
	mv $(st_built_path) $(out_folder)
	# Sublime Merge
	yq -j . sublime-merge-dashing.yml > $(sm_site)/dashing.json
	cd $(sm_site) && dashing build
	mv $(sm_built_path) $(out_folder)

post-build:
	python fix_index.py

.PHONY: clean
clean:
	[ -d "$(out_folder)" ] && rm -r $(out_folder) || true
	[ -f "$(st_site)/dashing.json" ] && rm $(st_site)/dashing.json || true
	[ -f "$(sm_site)/dashing.json" ] && rm $(sm_site)/dashing.json || true
	git restore --recurse-submodules $(st_submodule) $(sm_submodule)

zip:
	cd $(out_folder) && tar -czvf $(st_docset).tgz $(st_docset)
	cd $(out_folder) && tar -czvf $(sm_docset).tgz $(sm_docset)

.PHONY: test
test:
	cd test && python -m unittest

install-linux:
	cp -r $(out_folder)/* $(install_path_linux)
