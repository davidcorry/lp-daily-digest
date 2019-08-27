# lp-daily-digest

The goal of this project is to recreate Little Printer's daily printout, something that combines info from a few different sources and automatically sends it to a Little Printer connected to [Nord's Sirius server][nord-sirius]. The initial work on this will be for personal use (i.e. single user, no custom config), but ideally this will expand to allow multiple users and a customizable output.

Right now, I've written these modules (found in [lp\_daily\_digest/modules/](lp_daily_digest/modules/)):

* A simple "Hello World" module as a template and example
* News headlines (via the [NYT API][]) - pulls the 5 top stories
* Weather info (via [Dark Sky][])

Some goals for future modules:

* Calendar info (with [icalevents][])
* Some kind of tiny puzzle - sudoku?

I've also working on incorporating old Little Printer projects. Right now, I've included:

* [Amazing][] maze generator

A Github search brings up more old projects that could be ported or incorporated. So far I've found:

* [On This Day][]
* [Paper Pets][]
* NASA [APOD][]
* [Your Fortune][]
* [Constellatio][]

I'd like this to be as low-impact to my server as possible, and I'm going to try to structure this so that creating a new module is very simple and straightforward. It'll all have to be built-in modules for now, which means it'll be a less flexible than I remember the old Berg Cloud site to work. I have some ideas on how I can incorporate external modules, but it's super low on the priority list as long as I'm the only one using this.

I'll be using [Flask][] and [Jinja][] to create the HTML that gets sent to the printer, mostly for its simplicity and my own familiarity with it.

[nord-sirius]: http://littleprinter.nordprojects.co
[NYT API]: https://developer.nytimes.com/apis
[Dark Sky]: https://darksky.net/dev
[icalevents]: https://github.com/irgangla/icalevents
[On This Day]: https://github.com/alfo/onthisday
[Amazing]: https://github.com/knolleary/amazing
[Paper Pets]: https://github.com/bfirsh/paperpets
[APOD]: https://github.com/idleberg/Little-Printer-APOD
[Your Fortune]: https://github.com/technowizard12/your_fortune_lp
[Constellatio]: https://github.com/albyr/constellatio
[Flask]: https://palletsprojects.com/p/flask/
[Jinja]: https://palletsprojects.com/p/jinja/
