# pystonkslib

Stonks are cool - and if you want to do your own analysis, you have to pull all the data.

## Installation

```bash
pip install pystonkslib
```

## CI/CD

This CI/CD assumes that there are two variables set for the upload of your pypy packages:

`TWINE_PASSWORD`
`TWINE_USERNAME`

For the initial CI/CD, this is set to upload to testpypy rather than the actual pypy server.  If tags are used, it will push to production pypy.  This should let you differentiate between testing your package upload and actually publishing it to the pypy index.
