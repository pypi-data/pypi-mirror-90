# autobean

[![travis](https://travis-ci.com/SEIAROTg/autobean.svg)](https://travis-ci.com/SEIAROTg/autobean)
[![pypi](https://img.shields.io/pypi/v/autobean)](https://pypi.org/project/autobean/)
[![codecov](https://codecov.io/gh/SEIAROTg/autobean/branch/master/graph/badge.svg)](https://codecov.io/gh/SEIAROTg/autobean)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/SEIAROTg/autobean.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/SEIAROTg/autobean/context:python)
[![Maintainability](https://api.codeclimate.com/v1/badges/65e79b66e57139ed8bd0/maintainability)](https://codeclimate.com/github/SEIAROTg/autobean/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/65e79b66e57139ed8bd0/test_coverage)](https://codeclimate.com/github/SEIAROTg/autobean/test_coverage)
[![license](https://img.shields.io/github/license/SEIAROTg/autobean.svg)](https://github.com/SEIAROTg/autobean)

A collection of plugins and scripts that help automating bookkeeping with [beancount](http://furius.ca/beancount/).

## components

* [autobean.share](autobean/share): Manages shared accounts / transactions / postings with simple annotations and reuses joint ledgers among multiple parties.
* [autobean.xcheck](autobean/xcheck): Cross-checks against external ledgers.
* [autobean.narration](autobean/narration): Generates transaction narration from posting narration and posting narration from comments.
* [autobean.include](autobean/include): Includes external beancount ledgers without disabling their plugins.
* [autobean.truelayer](autobean/truelayer): Imports transactions from banks via [TrueLayer](https://truelayer.com/), an bank API aggregator.
* [autobean.sorted](autobean/sorted): Checks that transactions are in non-descending order in each file.
