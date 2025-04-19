# typ (Test Your Program)

typ is a simple program for testing Python code.

When testing Python code, it is basically a wrapper around the standard
`unittest` module, but it provides the following bits of additional
functionality:

* Parallel test execution.
* Clean output in the style of the Ninja build tool.
* A more flexible mechanism for discovering tests from the
  command line and controlling how they are run:

  * Support for importing tests by directory, filename, or module.
  * Support for specifying tests to skip, tests to run in parallel,
    and tests that need to be run by themselves

* Support for producing traces of test times compatible with Chrome's
  tracing infrastructure ([trace_viewer](https://chromium.googlesource.com/catapult/+/HEAD/tracing)).
* Integrated test coverage reporting (including parallel coverage).
* Integrated support for debugging tests.
* Support for uploading test results automatically to a server
  (useful for continuous integration monitoring of test results).
* An abstraction of operating system functionality called the
  Host class. This can be used by other python code to write more
  portable and easily testable code by wrapping the multiprocessing,
  os, subprocess, and time modules.
* Simple libraries for integrating Ninja-style statistics and line
  printing into your own code (the Stats and Printer classes).
* Support for processing arbitrary arguments from calling code to
  test cases.
* Support for once-per-process setup and teardown hooks.

(These last two bullet points allow one to write tests that do not require
Python globals).

## History

`typ` originated out of work on the [Blink](www.chromium.org/blink) and [Chromium](www.chromium.org) projects, as a way to
provide a friendlier interface to the Python `unittest` module.

After version v0.11.0 (Sep 4 2017), `typ` was imported into the [Catapult](https://chromium.googlesource.com/catapult) project (one of the Chromium subprojects) and that repo became the source of truth for subsequent `typ` development. The `master` branch ends with that happening.

The history from catapult was reimported (using `git filter-repo`) onto a new `main` branch on 2025-04-18 (using revision [4bbdc693c](https://chromium.googlesource.com/catapult/+/4bbdc693cd3e14ce07921f4de7ec4f834d69a8d1);
the last change to the typ subdirectory was from [8010a1b2](https://chromium.googlesource.com/catapult/+/8010a1b2f59fe654ca2a5966902a5ebd38d00cb7)).

The first commit post-merge was tagged as v0.12.0.

## Work remaining

typ is still a work in progress, but it's getting close to being done.
Things remaining for 1.0, roughly in priority order:

* Implement a non-python file format for testing command line interfaces

* Write documentation

## Possible future work

* `MainTestCase.check()` improvements:

  * check all arguments and show all errors at once?
  * make multi-line regexp matches easier to follow?

* `--debugger` improvements:

  * make it skip the initial breakpoint?

* Support testing javascript, java, c++/gtest-style binaries?

* Support for test sharding in addition to parallel execution (so that
  `run-web-tests` can re-use as much of the code as possible)?

* Support for non-unittest runtest invocation (for `run-web-tests`,
  other harnesses?)
