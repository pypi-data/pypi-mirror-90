"""Nox configuration for pupygrib."""

import glob
import os
import sys

import nox
from nox.command import CommandFailed

nox.options.sessions = [
    "format",
    "imports",
    "lint",
    "manifest",
    "typing",
    "doctest",
    "unittest",
    "coverage",
]

python_sources = ["noxfile.py", "src/pupygrib", "setup.py", "tests"]
numpy_versions = [
    "1.12.1",
    "1.13.3",
    "1.14.6",
    "1.15.4",
    "1.16.6",
    "1.17.5",
    "1.18.5",
    "1.19.4",
]


@nox.session
def requirements(session):
    """Compile all requirement files"""
    session.install("pip-tools")

    def pipcompile(outputfile, *inputfiles):
        session.run(
            "pip-compile",
            "--quiet",
            "--allow-unsafe",
            "--output-file",
            outputfile,
            *inputfiles,
            *session.posargs,
            env={"CUSTOM_COMPILE_COMMAND": "nox -s requirements"},
        )

    pipcompile("requirements/test.txt", "requirements/test.in")
    pipcompile("requirements/dev.txt", "requirements/dev.in")
    pipcompile("requirements/ci.txt", "requirements/ci.in")


@nox.session
def format(session):
    """Check the source code format with Black"""
    session.install("black ~= 20.8b1")
    session.run("black", "--check", "--quiet", *python_sources)


@nox.session
def imports(session):
    """Check the source code imports with isort"""
    session.install("isort ~= 5.6.4")
    session.run("isort", "--check", *python_sources)


@nox.session
def lint(session):
    """Check the source code with flake8"""
    session.install("flake8 ~= 3.8.4")
    session.run("flake8", *python_sources)


@nox.session
def manifest(session):
    """Check that the MANIFEST.in is up-to-date"""
    session.install("check-manifest ~= 0.45")
    session.run("check-manifest")


@nox.session
def typing(session):
    """Run a static type check with mypy"""
    session.install("mypy == 0.790")
    session.install("-r", "requirements/test.txt")
    session.install("-e", ".")
    session.run("mypy", "src/pupygrib", "tests")


@nox.session
def doctest(session):
    """Check the code examples in the documentation"""
    session.install("-r", "requirements/test.txt")
    session.install(f"numpy ~= {numpy_versions[-1]}")
    session.install("-e", ".")
    session.run("pytest", "--doctest-glob=*.md", *glob.glob("*.md"))


@nox.session
def coverage(session):
    """Check unit test coverage"""
    session.install("-r", "requirements/test.txt")
    session.install(f"numpy ~= {numpy_versions[-1]}")
    session.install("-e", ".")
    session.run("pytest", "--cov=pupygrib", "tests", *session.posargs)


def get_junit_prefix(numpy):
    pyversion = f"py{sys.version_info.major}{sys.version_info.minor}"
    npversion = f"np{''.join(numpy.split('.')[:2])}"
    return f"tests_{pyversion}_{npversion}"


@nox.session
@nox.parametrize("numpy", numpy_versions)
def unittest(session, numpy):
    """Run the unit tests"""
    session.install("-r", "requirements/test.txt")
    try:
        session.install("--only-binary", "numpy", f"numpy ~= {numpy}")
    except CommandFailed:
        session.skip("No numpy wheel for this python version")
    if "CI" in os.environ:
        session.install("--find-links", "dist", "--no-deps", "--pre", "pupygrib")
        junitprefix = get_junit_prefix(numpy)
        ciargs = ["--junit-xml", f"{junitprefix}.xml", "--junit-prefix", junitprefix]
    else:
        session.install("-e", ".")
        ciargs = []
    session.run("pytest", "tests", *ciargs, *session.posargs)
