=======
tuxmake
=======

-----------------------------------------
A thin wrapper for building Linux kernels
-----------------------------------------

:Manual section: 1
:Author: Antonio Terceiro, 2020

SYNOPSIS
========

tuxmake [OPTIONS] [KEY=VALUE ...] [targets ...]

DESCRIPTION
===========

tuxmake helps you build Linux kernels in a repeatable and consistent way. It
supports multiple ways of configuring the kernel, multiple architectures,
toolchains, and can build multiple targets.

Any **KEY=VALUE** pairs given in the command line are passed to make as is.
e.g. **LLVM=1**, **W=3**, etc.

You can specify what **targets** to build in the command line.  If none
are provided, tuxmake will build a default set of targets: config, kernel,
modules and DTBs (if applicable). Other build options, such as target
architecture, toolchain to use, etc can be provided with command line options.

OPTIONS
=======
..
    Include the options from --help
.. include:: cli_options.rst


ENVIRONMENT VARIABLES
=====================

* `TUXMAKE`: defines default options for tuxmake. Those options can be
  overridden in the command line.
* `TUXMAKE_DOCKER_RUN`: defines extra options for `docker run` calls made
  by the docker runtime.
* `TUXMAKE_PODMAN_RUN`: defines extra options for `podman run` calls made
  by the podman runtime.
* `TUXMAKE_IMAGE`: defines the image to use with the selected container runtime
  (docker, podman etc).  The same substitutions described in `--image`
  apply.
* `TUXMAKE_IMAGE_REGISTRY`: defines an container image registry to get any
  container image from. This string, and a slash character ("/"), gets
  prepended to the image name, regardless of it being provided via
  `$TUXMAKE_IMAGE`, `--image`, or determined automatically by tuxmake.
* `TUXMAKE_IMAGE_TAG`: defines an container image tag to use.  If
  used, a colon character (":") and this string get appended to the image name
  that was informed with `$TUXMAKE_IMAGE`, `--image`, or determined
  automatically by tuxmake.

..
    END OF ENVIRONMENT VARIABLES

SEE ALSO
========

The full tuxmake documentation: <https://docs.tuxmake.org/>
