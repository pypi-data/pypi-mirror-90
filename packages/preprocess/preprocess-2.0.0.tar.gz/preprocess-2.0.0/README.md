# preprocess.py: a portable multi-language file preprocessor

Download the latest preprocess.py packages from
https://github.com/doconce/preprocess.git.

|                 |                                           |
| --------------- | ----------------------------------------- |
| Home            | https://github.com/doconce/preprocess.git |
| License         | MIT (see `LICENSE.txt`)                   |
| Platforms       | Windows, Linux, Mac OS X, Unix            |
| Current Version | 2.0.0                                     |
| Dev Status      | Fairly mature                             |
| Requirements    | Python >= 2.7 or Python >= 3.4            |
| Dependencies    | [python-future](http://python-future.org) |
| Author          | Trent Mick                                |

## Install Notes

Preprocess can be installed via pip:
```
pip install preprocess
```

or with the following:

```
pip install https://github.com/doconce/preprocess/archive/master.zip
```

There's also a conda package on the conda-forge channel. To enable the conda-forge channel and install preprocess, run
```
conda config --add channels conda-forge
conda install preprocess
```
### Dependencies
`preprocess.py` version 1.2 depends on [python-future](http://python-future.org). This dependency is handled automatically by pip and conda.

## Why preprocess.py?

There are millions of templating systems out there (most of them
developed for the web). This isn't one of those, though it does share
some basics: a markup syntax for templates that are processed to give
resultant text output.  The main difference with `preprocess.py` is
that its syntax is hidden in comments (whatever the syntax for comments
maybe in the target filetype) so that the file can still have valid
syntax. A comparison with the C preprocessor is more apt.

`preprocess.py` is targetted at build systems that deal with many
types of files. Languages for which it works include: C++, Python,
Perl, Tcl, XML, JavaScript, CSS, IDL, TeX, Fortran, PHP, Java, Shell
scripts (Bash, CSH, etc.) and C#. Preprocess is usable both as a
command line app and as a Python module.

Here is how is works: All preprocessor statements are on their own
line. A preprocessor statement is a comment (as appropriate for the
language of the file being preprocessed). This way the preprocessor
statements do not make an unpreprocessed file syntactically incorrect.

Here is a simple example from Python code in some file `myapp1.p.py`:

```
    def myfunc():
        """
        Function for computing fundamental arithmetics.
    # #if EXTENSIVE_DOC
    # #include "../myfunc_doc.txt"
    # #endif
        """
        return 1 + 1
```
Running

```
    preprocess myapp1.p.py > myapp1.py
```
yields

```
    def myfunc():
        """
        Function for computing fundamental arithmetics.
        """
        return 1 + 1
```
in `myapp1.py` since `EXTENSIVE_DOC` is not defined, but

```
    preprocess -DEXTENSIVE_DOC myapp1.p.py > myapp1.py
```
defines `EXTENSIVE_DOC` and the file `../myfunc_doc.txt` is copied
by the `#include` statement, resulting in the output

```
    def myfunc():
        """
        Function for computing fundamental arithmetics.
        This function takes
        the expression "1 + 1"
        and returns its result.
        """
        return 1 + 1
```
if the file `../myfunc_doc.txt` contains the text

```
        This function takes
        the expression "1 + 1"
        and returns its result.
```

Here is another example where a variable defined on the command
line is a list:

```
    preprocess -DFEATURES=macros,scc myapp2.p.py
```
The code to the left is transformed to the code to the right:

```
    ...                                     ...
    # #if "macros" in FEATURES
    def do_work_with_macros():              def do_work_with_macros():
        pass                                    pass
    # #else
    def do_work_without_macros():
        pass
    # #endif
    ...                                     ...
```
Or, with a JavaScript file,

```
    ...                                     ...
    // #if "macros" in FEATURES
    function do_work_with_macros() {        function do_work_with_macros() {
    }                                       }
    // #else
    function do_work_without_macros() {
    }
    // #endif
    ...                                     ...
```

Preprocess has proved useful for
build-time code differentiation in the
[Komodo](http://www.activestate.com/Komodo) build system -- which
includes source code in Python, JavaScript, XML, CSS, Perl, and C/C++.
Preprocess is also a key tool in the [DocOnce](https://github.com/hplgit/doconce) documentation system.

The `#if` expression (`"macros" in FEATURES` in the example) is Python
code, so it has Python's full comparison richness.  A number of
preprocessor statements are implemented:

```
    #define VAR [VALUE]
    #undef VAR
    #ifdef VAR
    #ifndef VAR
    #if EXPRESSION
    #elif EXPRESSION
    #else
    #endif
    #error ERROR_STRING
    #include "FILE"
    #include "FILE" fromto: from-regex@to-regex
    #include "FILE" fromto_: from-regex@to-regex
```
Run `pydoc preprocess` to see more explanation.

As well, preprocess can do in-line substitution of defined variables.
Although this is currently off by default because substitution will occur
in program strings (and actually anywhere), which is not ideal.


## Getting Started

Once you have the package installed, run `preprocess --help` for full usage
information:
```
    $ preprocess --help
    Preprocess a file.

    Command Line Usage:
        preprocess [<options>...] <infile>

    Options:
        -h, --help      Print this help and exit.
        -V, --version   Print the version info and exit.
        -v, --verbose   Give verbose output for errors.

        -o <outfile>    Write output to the given file instead of to stdout.
        -f, --force     Overwrite given output file. (Otherwise an IOError
                        will be raised if <outfile> already exists.
        -D <define>     Define a variable for preprocessing. <define>
                        can simply be a variable name (in which case it
                        will be true) or it can be of the form
                        <var>=<val>. An attempt will be made to convert
                        <val> to an integer so "-D FOO=0" will create a
                        false value.
        -I <dir>        Add an directory to the include path for
                        #include directives.

        -k, --keep-lines    Emit empty lines for preprocessor statement
                        lines and skipped output lines. This allows line
                        numbers to stay constant.
        -s, --substitute    Substitute defines into emitted lines. By
                        default substitution is NOT done because it
                        currently will substitute into program strings.

    Module Usage:
        from preprocess import preprocess
        preprocess(infile, outfile=sys.stdout, defines={}, force=0,
                   keepLines=0, includePath=[], substitute=0)

    The <infile> can be marked up with special preprocessor statement lines
    of the form:
        <comment-prefix> <preprocessor-statement> <comment-suffix>
    where the <comment-prefix/suffix> are the native comment delimiters for
    that file type.


    Examples
    --------

    HTML (*.htm, *.html) or XML (*.xml, *.kpf, *.xul) files:

        <!-- #if FOO -->
        ...
        <!-- #endif -->

    Python (*.py), Perl (*.pl), Tcl (*.tcl), Ruby (*.rb), Bash (*.sh),
    or make ([Mm]akefile*) files:

        # #if defined('FAV_COLOR') and FAV_COLOR == "blue"
        ...
        # #elif FAV_COLOR == "red"
        ...
        # #else
        ...
        # #endif

    C (*.c, *.h), C++ (*.cpp, *.cxx, *.cc, *.h, *.hpp, *.hxx, *.hh),
    Java (*.java), PHP (*.php) or C# (*.cs) files:

        // #define FAV_COLOR 'blue'
        ...
        /* #ifndef FAV_COLOR */
        ...
        // #endif

    Fortran 77 (*.f) or 90/95 (*.f90) files:

        C     #if COEFF == 'var'
              ...
        C     #endif


    Preprocessor Syntax
    -------------------

    - Valid statements:
        #define <var> [<value>]
        #undef <var>
        #ifdef <var>
        #ifndef <var>
        #if <expr>
        #elif <expr>
        #else
        #endif
        #error <error string>
        #include "<file>"
      where <expr> is any valid Python expression.
    - The expression after #if/elif may be a Python statement. It is an
      error to refer to a variable that has not been defined by a -D
      option or by an in-content #define.
    - Special built-in methods for expressions:
        defined(varName)    Return true if given variable is defined.

    Tips
    ----

    A suggested file naming convention is to let input files to
    preprocess be of the form <basename>.p.<ext> and direct the output
    of preprocess to <basename>.<ext>, e.g.:
        preprocess -o foo.py foo.p.py
    The advantage is that other tools (esp. editors) will still
    recognize the unpreprocessed file as the original language.
```

And, for module usage, read the preprocess.preprocess() docstring:
```
    pydoc preprocess.preprocess
```

## Change Log

### v2.0.0

Updated [preprocess on PyPi](https://pypi.org/project/preprocess/). The aim is to make it easier to install preprocess as a dependency of [DocOnce](https://github.com/doconce/doconce).
(By Alessandro Marin.)

### v1.2.2

Added `--substitute_include` and `-i` options for substitutions of defined variables (`-DVAR=value`) in `#include` statements (makes it possible to have variables in included filenames: `# #include "myfile_VAR.do.txt"`).
(By Hans Petter Langtangen.)

### v1.2.1

Added support for including just parts of a file (from a regex to a regex).
(By Hans Petter Langtangen.)

### v1.2.0

Used python-future and the futurize script to port the code to a common
Python 2/3 base. Preprocess now depends on python-future.
Moved code base to GitHub.
(By Hans Petter Langtangen.)

Note that v1.1.0 has moved from code.google.com to github.com: https://github.com/trentm/preprocess, but this version is does not (yet) feature the enhancements in v1.2.0 and later.

### v1.1.0

- Move to code.google.com/p/preprocess for code hosting.
- Re-org directory structure to assist with deployment to pypi and
  better installation with `setup.py`.
- Pulled the `content.types` file that assists with filetype
  determination into `preprocess.py`. This makes `preprocess.py` fully
  independent and also makes the `setup.py` script simpler. The
  `-c|--content-types-path` option can be used to specify
  addition content types information.

### v1.0.9

- Fix the 'contentType' optional arg for `#include`'s.
- Add cheap XML content sniffing.

### v1.0.8

- Allow for JS and CSS-style comment delims in XML/HTML. Ideally this
  would deal with full lexing but that isn't going to happen soon.

### v1.0.7

- Allow explicit specification of content type.

### v1.0.6

- Add ability to include a filename mentioned in a define: `#include VAR`.
  (Note: v1.2.2 has `-i` option for substituting into *parts* of the filename.)


### v1.0.5

- Make sure to use the *longest* define names first when doing
  substitutions. This ensure that substitution in this line:
  `FOO and BAR are FOOBAR`
  will do the right thing if there are "FOO" and "FOOBAR" defines.

### v1.0.4

- Add WiX XML file extensions.
- Add XSLT file extensions.

### v1.0.3

- TeX support (from Hans Petter Langtangen)

### v1.0.2

- Fix a bug with `-k|--keep-lines` and preprocessor some directives in
  ignored if blocks (undef, define, error, include): those lines were
  not kept. (bug noted by Eric Promislow)

### v1.0.1

- Fix documentation error for `#define` statement. The correct syntax
  is `#define VAR [VALUE]` while the docs used to say
  `#define VAR[=VALUE]`. (from Hans Petter Langtangen)
- Correct '! ...' comment-style for Fortran -- the '!' can be on any
  column in Fortran 90. (from Hans Petter Langtangen)
- Return a non-zero exit code on error.

### v1.0.0

- Update the test suite (it had been broken for quite a while) and add
  a Fortran test case.
- Improve Fortran support to support any char in the first column to
  indicate a comment. (Idea from Hans Petter Langtangen)
- Recognize '.f90' files as Fortran. (from Hans Petter Langtangen)
- Add Java, C#, Shell script and PHP support. (from Hans Petter
  Langtangen)

### v0.9.2

- Add Fortran support (from Hans Petter Langtangen)
- Ensure content.types gets written to "bindir" next to preprocess.py
  there so it can be picked up (from Hans Petter Langtangen).

### v0.9.1

- Fully read in the input file before processing. This allows
  preprocessing of a file onto itself.

### v0.9.0

- Change version attributes and semantics. Before: had a `_version_`
  tuple. After: `__version__` is a string, `__version_info__` is a tuple.

### v0.8.1

- Mentioned `#ifdef` and `#ifndef` in documentation (these have been there
  for a while).
- Add preprocess.exe to source package (should fix installation on
  Windows).
- Incorporate Komodo changes:
    - change 171050: add Ruby support
    - change 160914: Only attempt to convert define strings from the
      command-line to *int* instead of eval'ing as any Python
      expression: which could surprise with strings that work as
      floats.
    - change 67962: Fix `#include` directives in preprocessed files.

### v0.8.0

- Move hosting to trentm.com. Improve the starter docs a little bit.

### 0.7.0:

- Fix bug 1: Nested #if-blocks will not be properly handled.
- Add 'Text' type for .txt files and default (with a warn) unknown
  filetypes to 'Text'. Text files are defined to use to `#...`-style
  comments to allow if/else/.../endif directives as in
  Perl/Python/Tcl files.

### 0.6.1:

- Fix a bug where preprocessor statements were not ignored when not
  emitting. For example the following should _not_ cause an error:
```
    # #if 0
    # #error womba womba womba
    # #endif
```
- Fix a bug where multiple uses of preprocess.preprocess() in the
  same interpreter would erroneously re-use the same list of
  __preprocessedFiles. This could cause false detection of recursive
  `#include`'s.
- Fix `#include`, broken in 0.6.0.

### 0.6.0:

- substitution: Variables can now replaced with their defined value
  in preprocessed file content. This is turned OFF by default
  because, IMO, substitution should not be done in program strings.
  I need to add lexing for all supported languages before I can do
  *that* properly. Substitution can be turned on with the
  `--substitute` command-line option or the `subst=1` module interface
  option.
- Add support for preprocessing HTML files.

### 0.5.0:

- Add `#error`, `#define`, `#undef`, `#ifdef` and `#ifndef` statements.
- `#include` statement, `-I` command line option and `includePath`
  module interface option to specify an include path
- Add `__FILE__` and `__LINE__` default defines.
- More strict and more helpful error messages:
    - Lines of the form `#else <expr>` and `#endif <expr>` no longer
      match.
    - error messages for illegal `#if`-block constructs
    - error messages for use of `defined(BAR)` instead of
      `defined('BAR')` in expressions
- New "keep lines" option to output blank lines for skipped content
  lines and preprocessor statement lines (to preserve line numbers
  in the processed file).

### 0.4.0:

- Add `#elif` preprocessor statement.
- Add `defined()` built-in, e.g. `#if defined('FOO')`

### 0.3.2:

- Make `#if` expressions Python code.
- Change "defines" attribute of `preprocess.preprocess()`.
- Add `-f|--force` option to overwrite given output file.

### 0.2.0:

- Add content types for C/C++.
- Better module documentation.
- You can define *false* vars on the command line now.
- `python setup.py install` works.

### 0.1.0:

- First release.
