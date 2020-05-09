source_link := https://www.sublimetext.com/docs/index.html
local_path := ./www.sublimetext.com
local_index := $(local_path)/docs/index.html
built_path := ./sublime-text.docset

.PHONY: all
all: clean download fix build fix-build

.PHONY: download
download:
	-wget \
		--convert-links \
		--recursive \
		--page-requisites \
		--no-parent \
		--no-clobber \
		"$(source_link)"
	# When /docs/ stops 3XXing to /docs/3/index.html, this and several
	#  lines in 'fix' can be removed
	-wget \
		--convert-links \
		--output-document=$(local_index) \
		"$(source_link)"

.PHONY: fix
fix: fix-html fix-css
	-rm -r $(local_path)/docs/3

.PHONY: fix-html
fix-html:
	sed -i -e 's/\(href="\)https:\/\/www.sublimetext.com\/docs\//\1/g' $(local_index)
	sed -i -e 's/\(href="\)https:\/\/www.sublimetext.com\/\(.*\.css\)/\1..\/\2/g' $(local_index)
	find $(local_path) -iname '*.html' -exec sed -i -e '/<header>/,/<\/header>/d' {} \;

.PHONY: fix-css
fix-css:
	$(shell for f in $$(ls $(local_path)/*.css\?*); do mv "$$f" "$${f%\?*}"; done )

build:
	dashing build

.PHONY: fix-build
fix-build:
	find $(built_path) -iname '*.html' -exec \
		sed -i -Ee 's#(<a [^>]+></a><a [^>]+></a>)(<td[^>]*>)#\2\1#g' {} \;

.PHONY: clean
clean:
	-rm -r $(local_path)

.PHONY: clean-more
clean-more: clean
	-rm -r $(built_path)
