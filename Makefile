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
all: clean pre-build build post-build test

.PHONY: pre-build
pre-build:
	cd src && python fix_html.py

.PHONY: build
build:
	# Shared
	mkdir -p $(out_folder)
	cd src && python generate_dashing.py
	# Sublime Text
	cd $(st_site) && dashing build
	mv $(st_built_path) $(out_folder)
	# Sublime Merge
	cd $(sm_site) && dashing build
	mv $(sm_built_path) $(out_folder)

.PHONY: post-build
post-build:
	cd src && python fix_index.py

.PHONY: clean
clean:
	[ -d "$(out_folder)" ] && rm -r $(out_folder) || true
	[ -f "$(st_site)/dashing.json" ] && rm $(st_site)/dashing.json || true
	[ -f "$(sm_site)/dashing.json" ] && rm $(sm_site)/dashing.json || true
	git restore --recurse-submodules $(st_submodule) $(sm_submodule)

.PHONY: zip
zip:
	cd $(out_folder) && tar -czvf Sublime_Text.tgz $(st_docset)
	cd $(out_folder) && tar -czvf Sublime_Merge.tgz $(sm_docset)

.PHONY: test
test:
	cd test && python -m unittest

.PHONY: install-linux
install-linux:
	cp -r $(out_folder)/* $(install_path_linux)
