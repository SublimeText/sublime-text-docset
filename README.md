# [Sublime Text Docset][self]

[Dash][] and [Zeal][] docset for [Sublime Text][st]’s official
[documentation][st-docs].


## Installation

Download from GitHub Releases or build yourself with the instructions below.

- If you have a `sublime-text.docset.zip` from GitHub, extract it to a
folder called `sublime-text.docset`.
- If you build yourself, `sublime-text.docset` will be in the
`www.sublimetext.com` folder.

We hope to have a distribution channel [eventually][distribution].

### Install a local folder to Dash

1. Open Dash.
1. <kbd>Cmd</kbd>+<kbd>,</kbd>
1. Open the "Docsets" tab.
1. Click the <kbd>+</kbd>.
1. Choose "Add Local Docset".
1. Select the `sublime-text.docset` in the `www.sublimetext.com` folder.
1. Optionally change the keyword.

###  Install a local folder to Zeal

1. Find your docset folder ("Docset storage" in your Preferences)
1. Copy or symlink `sublime-text.docset` to that folder.


## Building

### Requirements

* `make`
* [`dashing`][dashing]
* `yq`
* `wget`
* Python 3.8+

### Steps

0. (Optional) Enter a Python virtual environment.
1.
   ``` sh
   pip install -r requirements.txt
   make
   ```


[self]: https://github.com/SublimeText/sublime-text-docset
[Dash]: https://kapeli.com/dash
[Zeal]: https://zealdocs.org
[st]: https://www.sublimetext.com/
[st-docs]: https://www.sublimetext.com/docs/index.html
[dashing]: https://github.com/technosophos/dashing#readme
[distribution]: https://github.com/SublimeText/sublime-text-docset/issues/12
