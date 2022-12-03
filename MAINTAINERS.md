# Maintainers' Notes

To release a new version:

1. Update CHANGELOG.md
2. Bump version
3. Test!
4. Add a tag and push it to upstream
5. Publish the release on github

## Updating CHANGELOG.md

Look through the list of [recently closed pull requests](https://github.com/RaRe-Technologies/sqlitedict/pulls?q=is%3Apr+is%3Aclosed).
For each pull-request, run:

```bash
release/summarize_pr.py {prid}
```

and copy-paste the result into CHANGELOG.md

## Bumping version

Do this in two places:

1. sqlitedict.py
2. setup.py

## Testing

Run:

```bash
pytest tests
```

All tests should pass.

## Tagging

Run:

```bash
git tag v{version}
git push origin --tags
```

The leading "v" is important, our CI will use that to identify the release.
Once the tag is uploaded to github, CI will take care of everything, including uploading the release to PyPI.

## Publishing on github

1. Go to https://github.com/RaRe-Technologies/sqlitedict/releases/new
2. Select the tag for the latest releases
3. Click on "autogenerate change log"
