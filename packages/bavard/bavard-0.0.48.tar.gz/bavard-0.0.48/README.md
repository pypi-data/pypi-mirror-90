# bavard-nlu

## Local Development

### Install Dependencies

```
pip3 install -e .
pip3 install -r requirements-test.txt
```

### Testing Locally

The tests for this repo consist of functional tests for catching bugs/code regressions, and validation tests for catching model performance regressions. The validation tests take much longer to execute. Both are run in CI. To run just the functional tests:

```
python3 -m unittest discover test/functional
```

### The Package CLI

There is a convenience CLI for training, evaluating, predicting, tuning, and interacting with NLU and dialogue policy models. To see the CLI documentation:

```
python3 -m bavard --help
```

You can also view the documentation for a sub-command for example:

```
python3 -m bavard nlu evaluate  --help
```

## Releasing The Package

Releasing the package is automatically handled by CI, but three steps must be taken to trigger a successful release:

1. Increment the `VERSION` variable in `setup.py` to the new desired version (e.g. `VERSION="1.1.1"`)
2. Commit and tag the repo with the **exact same** value you populated the `VERSION` variable with (e.g. `git tag 1.1.1`)
3. Push the commit and tag to remote. These can be done together using: `git push --atomic origin <branch name> <tag>`

CI will then release the package to pypi with that version once the commit and tag are pushed.
