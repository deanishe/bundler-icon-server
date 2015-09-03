# Iconserver extras #

This directory contains a few scripts for managing/testing the server and some TSV files for generating the JSON configuration files for some fonts.


## Scripts ##

`fill_cache.py` opens a whole bunch of pages on the local development server to fill the icon cache.

`generate.py` generates the `characters` mapping for a font's JSON configuration file from one of the TSV files in this directory.


## Notes  ##

Entypo and Entypo Social don't work well with the icon-generation code, so they are unused.

The Weather Icons package can be found in the [Iconpacks repo][iconpacks].

`weather_all.tsv` contains *all* the classes defined in the CSS, while `weather.tsv` ignores any duplicates (i.e. classes that prepend the same character).

Any classes using CSS transforms are ignored: correspondingly-rotated icons cannot be generated.



[iconpacks]: https://github.com/deanishe/bundler-icon-server-iconpacks
