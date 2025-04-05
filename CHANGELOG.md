CHANGELOG
=========


All system changes are documented below

## Version 2.2.2 - (04/04/2025)

### Added:

- Interactiveness and icons for Makefile
- `first-contribution.yml` to greet new contributors (*everyone is welcome :)! *)
- Icons for `SECURITY.md` and `README.md` for a new look.

### Changed:

- Excluded flags `B404`, `B311` and `B603` from bandit scans since they were unnecessary
and just cluttering the security page

*this was just a small update, i'm looking forward to updating more*

## Version 2.2.1 - (04/03/2025)

### Added:
- New clear function test in `test_minor.py`.
- added safety checks and scanning in each push
- `.safety-project.ini` file for safety scans

### Fixed:

- fixed checks not working in windows
- "WebRequestHandler has no attribute clear" error fixed (clear_screen was the function, i forgot :])


## Version 2.2.0 - (03/31/2025)

### Added:
- `test_minor.py` for testing minor functions, you can always add other minor functions to that file, but for now, it only tests the `reset` and `normalize` functions
- `test_checker.py` for testing the website checker

### Changed:
- Added both new files to the Makefile `test` command
- Updated `SECURITY.md` file, so yeah, things below version `2.0.0` are not supported

# Version 2.0.0 - (03/29/2025)

### Changed:
- Refractored `main.py` code for better readibility and maintenance.
- Updated script version to 2.0.0 since this is a breaking change.

### Added:
- added unit tests in `tests/test_poke.py` directory.
- added a unit test workflow.
- new Makefile command for the unit tests.


## Version 1.0.3 - (03/15/2025)

### bug fixes:
- fixed cookie printing on both get and post method
- sadly, i had to remove the whois command and module off the code, since it was causing errors and i didn't find documentation




## Version 1.0.1 - (03/13/2025)


### bug fixes:
- fixed bug on Makefile where linting wouldn't work
- added a small variable change in `main.py`
- changed `safety check` to `safety scan` (deprecated)

### additional:
- added `SECURITY.md` file for version transparecy and a VERSION file for current version
- Created a `VERSION` file to track the current version.
- `CODEOWNERS` file for reviewing changes
- added new types of forms for better organizing requests, problems or changes:
  - **bug report form**
  - **support form**
  - **feature request form**
  - **pull request form**
- along with a `config.yml` for proper usage
  
- `labeler.yml` for automating labeling in pull requests and save people time
- added permissions on specified workflows for security reasons:
  - `stale.yml`
  - `mend-release.yml`
  - `cache-cleanup.yml`
- Integrated `auto-reponse.yml` for improved interactions
- and also deleted `changelog-generator.yml` because it was annoying me whenever i was updating the `CHANGELOG.md` file

------------------------

