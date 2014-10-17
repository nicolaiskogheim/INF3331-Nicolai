INF3331-Nicolai [![Build Status](https://magnum.travis-ci.com/UiO-INF3331/INF3331-Nicolai.svg?token=d2hAWhNm6p8PZiqU2hNi&branch=master)](https://magnum.travis-ci.com/UiO-INF3331/INF3331-Nicolai)
===============

##Instructions

### Installing
To run tests and coverage you need to install
py.test and pytest-cov.
`pip install -U pytest pytest-cov`

### Running tests
To run all the tests run
```sh
py.test
```
from the root folder.


To run tests for one mandatory only, `cd` into
desired directory and run `py.test` there
like so
```sh
cd oblig01
py.test
```

To get coverage reports, run py.test with the
`--cov` flag and specify which folder to gather
coverage data from
```sh
cd oblig02
py.test --cov PreTeX/
```

If you are using py.test and want covering on your
own code, then you would only need to do what you
did here, install pytest-cov and use the flag together
with path(s) to folder(s).
NB: If your tests is in the folder you're running
coverage on, then they will be reported as well,
but this does not affect the reporting of your program.
