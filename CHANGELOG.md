CHANGELOG
=========


All system changes are documented below

## Version 1.0.1

--------------------

bug fixes:
- fixed bug on Makefile where linting wouldn't work
- added a small variable change in `main.py`
- changed `safety check` to `safety scan` (deprecated)

additional:
- added `SECURITY.md` file for version transparecy and a VERSION file for current version
- `CODEOWNERS` file for reviewing changes
- added new types of forms for better organizing requests, problems or changes:
  - bug report form
  - support form
  - feature request form
  - pull request form
  along with a config.yml to make sure you can always use them
- `labeler.yml` for automating labeling in pull requests and save people time
- added permissions on specified workflows for security reasons:
  - `stale.yml`
  - `mend-release.yml`
  - `cache-cleanup.yml`
- `auto-reponse.yml` to make people not feel like they're going to be left hanging

------------------------

