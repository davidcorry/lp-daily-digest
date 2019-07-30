# lp-daily-digest

The goal of this project is to recreate Little Printer's daily printout, something that combines info from a few different sources and automatically sends it to a Little Printer connected to [Nord's Sirius server][nord-sirius]. The initial work on this will be for personal use (i.e. single user, no custom config), but ideally this will expand to allow multiple users and a customizable output.

Right now, the modules I'd like to include are:

* News headlines (via the [NYT API][]?)
* Weather info (via [Dark Sky][]?)
* Some kind of tiny puzzle

I'd like this to be as low-impact to my server as possible, and I'm going to try to structure this so that creating a new module is very simple and straightforward. It'll all have to be built-in modules, which means it'll be a less flexible than I remember the old Berg Cloud site to work, but that shouldn't be too big of a problem.

I'll be using [Flask][] and [Jinja][] to create the HTML that gets sent to the printer, mostly for its simplicity and my own familiarity with it.

[nord-sirius]: http://littleprinter.nordprojects.co
[NYT API]: https://developer.nytimes.com/apis
[Dark Sky]: https://darksky.net/dev
[Flask]: https://palletsprojects.com/p/flask/
[Jinja]: https://palletsprojects.com/p/jinja/
