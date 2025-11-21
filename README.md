# [Sublime Text Docset][self]

[Dash][] and [Zeal][] docset for [Sublime Text][st]’s official
[documentation][st-docs].
There is also a small docset for [Sublime Merge][sm].


## Installation

### Install from a feed

This is likely more convenient because updates will be downloaded
to your application automatically.

#### Dash

Dash has built-in support for their user-contributed docsets.
Go to *Preferences* > *Downloads* > *User Contributed*
to search for "Sublime" and install the community-org maintained ones.

#### Zeal

Zeal does not have a direct search for user-contributed docsets,
but a [third-party website][zuc] repackages docset feeds
in a compatible format.
In Zeal, go to *Tools* > *Docsets&hellip;* > *Add feed*
and paste in the URL to the respective feed:

```none
https://zealusercontributions.vercel.app/api/docsets/Sublime_Text.xml
```
```none
https://zealusercontributions.vercel.app/api/docsets/Sublime_Merge.xml
```

### Install manually

Download from [GitHub Releases][releases]
or build yourself with the instructions below.

- If you have a `docset-bundle.zip` from GitHub, extract it somewhere.
- If you build yourself, `sublime-text.docset` will be in the
`out` folder.

#### Install a local folder to Dash

It may be possible to just double-click `sublime-text.docset`.
If that doesn't work:

1. Open Dash.
1. <kbd>Cmd</kbd>+<kbd>,</kbd>
1. Open the "Docsets" tab.
1. Click the <kbd>+</kbd>.
1. Choose "Add Local Docset".
1. Select `sublime-text.docset`.
1. Optionally change the keyword.
1. Repeat for `sublime-merge.docset`.

####  Install a local folder to Zeal

If you built yourself and you have default Linux folders,
just `make install-linux`.
Otherwise:

1. Find your docset folder ("Docset storage" in your Preferences).
1. Copy or symlink `sublime-text.docset` to that folder.
1. Repeat for `sublime-merge.docset`.


## Building

### Requirements

* `make`
* [`dashing`][dashing]
* Python 3.11+

### Steps

0. (Optional) Enter a Python virtual environment.
1. One time
   ```sh
   git submodule init
   pip install -r requirements.txt
   ```
1. Each build
   ```sh
   make
   ```


## Credits

- [Alex (Oleksii) Markov][malexer] made the first version of this docset.
- [Ali Ayas][maliayas] made the ST and SM docs scanners used here as submodules.
- Most recent development is [Michael B. Lyons][michaelblyons] and [FichteFoll][].
- Many thanks to [Sublime HQ][shq] for [letting us][permission] make this.


[self]: https://github.com/SublimeText/sublime-text-docset
[Dash]: https://kapeli.com/dash
[Zeal]: https://zealdocs.org
[st]: https://www.sublimetext.com/
[st-docs]: https://www.sublimetext.com/docs/index.html
[sm]: https://www.sublimemerge.com/
[zuc]: https://zealusercontributions.vercel.app
[releases]: https://github.com/SublimeText/sublime-text-docset/releases
[dashing]: https://github.com/technosophos/dashing#readme

[malexer]: https://github.com/malexer
[maliayas]: https://github.com/maliayas
[michaelblyons]: https://github.com/michaelblyons
[fichtefoll]: https://github.com/FichteFoll
[shq]: https://www.sublimehq.com
[permission]: https://github.com/SublimeText/sublime-text-docset/issues/10
