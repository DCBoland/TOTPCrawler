TOTPCrawler
===========

A scrapy crawler for historical UK charts

Produces charts.json containing the weekly charts - Year, Week, Date and a list of track IDs in chart order
Produces tracks.json containing each unique track - TrackID, artist, title

TODO:
- Handle missing charts errors (ok to ignore)
- Ensure track ordering maintained!

Usage:
scrapy crawl TOTP --loglevel ERROR

(Error log level used as debug logs will slow down crawl massively.)
