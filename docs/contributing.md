Any kind of contribution is more than welcomed! There are several ways you can contribute:

- Opening [GitHub issues](https://github.com/y-sunflower/bumplot/issues) to list the bugs you've found
- Implementation of new features or resolution of existing bugs
- Enhancing the documentation

## Setting up your environment

### Install for development

- Fork the repository to your own GitHub account.

- Clone your forked repository to your local machine (ensure you have [Git installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)):

```bash
git clone https://github.com/github_user_name/bumplot.git
cd bumplot
git remote add upstream https://github.com/y-sunflower/bumplot.git
```

- Create a new branch:

```bash
git checkout -b my-feature
```

- Set up your Python environment (ensure you have [uv installed](https://docs.astral.sh/uv/getting-started/installation/)):

```bash
uv sync --all-extras --dev
uv pip install -e .
```

## Code

You can now make changes to the package and start coding!

### Run the test

- Test that everything works correctly by running:

```bash
make test
```

### Preview documentation locally

```bash
make preview
```

## Push changes

- Commit and push your changes:

```bash
git add -A
git commit -m "description of what you did"
git push
```

- Navigate to your fork on GitHub and click the "Compare & pull request" button to open a new pull request.

Congrats! Once your PR is merged, it will be part of `bumplot`.

<br>
