CHANGELOG
=========


All system changes are documented below

## Version 1.0.3

### bug fixes:
- fixed cookie printing on both get and post method
- sadly, i had to remove the whois command and module off the code, since it was causing errors and i didn't find documentation




## Version 1.0.1


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

