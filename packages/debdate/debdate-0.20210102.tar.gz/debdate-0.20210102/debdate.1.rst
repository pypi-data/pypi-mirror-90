=========
 debdate
=========

------------------------------------------------
 Convert Gregorian dates to Debian Regnal dates
------------------------------------------------

:Author:         valhalla@trueelena.org
:Date:           2017-07-14
:Copyright:      2017 Elena Grandi
:License:        Released under the terms of the Do What The Fuck You
                 Want To Public License, Version 2, as published by Sam
                 Hocevar. http://www.wtfpl.net/
:Manual section: 1

SYNOPSIS
========

debdate [-h] [-d DATE | -s SECONDS] {test} ...

DESCRIPTION
===========

``debdate`` is a fundamental tool for anybody who follows the debian
calendar where the years are named after the current stable release.

OPTIONS
=======

  -h, --help                       show this help message and exit
  -d DATE, --date DATE             A gregorian date
  -s SECONDS, --seconds SECONDS    A date as seconds from the Unix Epoch

EXAMPLES
========

``debdate``

Print the debian regnal date for today.

``debdate -d 2017-06-18``

Print the debian regnal date for the day of the release of Stretch.

``debdate -s 1497736800``

Print the same date as above.

``debdate -d 'Jul 18 2017'``

Print again the same date as above, passed in an illogical format.
Any string that is recognised as a valid date by dateutil can be used.

SEE ALSO
========

* date(1)
* ddate(1)
* https://dateutil.readthedocs.io/en/stable/
