# See:
# https://docs.python.org/2/distutils/setupscript.html
# http://docs.cython.org/src/reference/compilation.html
# https://docs.python.org/2/extending/building.html
# http://docs.cython.org/src/userguide/source_files_and_compilation.html
# http://www.ewencp.org/blog/a-brief-introduction-to-packaging-python/
# http://stackoverflow.com/questions/12966216/make-distutils-in-python-automatically-find-packages
# http://blog.ionelmc.ro/2014/05/25/python-packaging/
# http://blog.ionelmc.ro/2014/06/25/python-packaging-pitfalls/
# To add a commandline entry point: http://www.scotttorborg.com/python-packaging/command-line-scripts.html
# Also see pyroma and checkmanifest tools.
#
# To test, use `python setup.py develop`
# To package, use `python setup.py sdist --formats=gztar,zip bdist_wininst --plat-name=win32` and then try to `python setup.py install` and check if everything runs correctly.
# Then to upload to pypi, do `python setup.py register sdist --formats=gztar,zip bdist_wininst --plat-name=win32 upload`
try:
    from setuptools import setup, find_packages
    from setuptools import Extension
except ImportError:
    from distutils.core import setup, find_packages
    from distutils.extension import Extension

import os, sys

try:
    # Test if Cython is installed
    if '--nocython' in sys.argv:
        # Skip if user does not want to use Cython
        sys.argv.remove('--nocython')
        raise(ImportError('Skip Cython'))
    # If Cython is installed, transpile the optimized Cython module to C and compile as a .pyd to be distributed
    from Cython.Build import cythonize
    print("Cython is installed, building creedsolo module")
    extensions = [
                Extension('unireedsolomon.cff', [os.path.join('unireedsolomon', 'cff.pyx')]),
                Extension('unireedsolomon.cpolynomial', [os.path.join('unireedsolomon', 'cpolynomial.pyx')]),
             ]
except ImportError:
    # Else Cython is not installed (or user explicitly wanted to skip)
    if '--native-compile' in sys.argv:
        # Compile pyd from pre-transpiled creedsolo.c
        print("Cython is not installed, but the creedsolo module will be built from the pre-transpiled creedsolo.c file using the locally installed C compiler")
        sys.argv.remove('--native-compile')
        extensions = [
                Extension('unireedsolomon.cff', [os.path.join('unireedsolomon', 'cff.c')]),
                Extension('unireedsolomon.cpolynomial', [os.path.join('unireedsolomon', 'cpolynomial.c')]),
             ]
    else:
        # Else run in pure python mode (no compilation)
        print("Cython is not installed or is explicitly skipped using --nocython, no creedsolo module will be built")
        extensions = None


setup(
    name = "unireedsolomon",
    version = "1.0.4",
    description = "Universal errors-and-erasures Reed Solomon codec (error correcting code) in pure Python with extensive documentation",
    author = "Andrew Brown, Stephen Larroque",
    author_email = "lrq3000@gmail.com",
    platforms = ["any"],
    license = "MIT",
    url = "https://github.com/lrq3000/unireedsolomon",
    #packages = ["unireedsolomon"],
    #py_modules = ["rs", 'polynomial', 'ff', '_compat'],
    long_description = open("README.rst", "r").read(),
    long_description_content_type = "text/x-rst",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Cython",
        "Topic :: Communications",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Recovery Tools",
    ],
    keywords = 'error correction erasure reed solomon repair file network packet',
    ext_modules = extensions,
    test_suite='nose.collector',
    tests_require=['nose'],
    packages = find_packages(exclude=['build', 'docs', 'presentation'])
)