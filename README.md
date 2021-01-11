# Production service to predict password complexity

This is the production service to predict password complexity which was developed for the course about Production Machine Learning.

Python 3.8.5 is used.

## Notes

### git lfs

Note that `packages/app` is added as subtree: `git subtree add --prefix packages/app git@gitlab.com:production_ml/password_app.git master --squash`.
Unfortunately, git lfs doesn't support this subtree: https://github.com/git-lfs/git-lfs/issues/854.
The resolution is describe in one of the first commits in the page above: one need to cd to the subtree'd repo and then push files stored with lfs to the new repo. Running `git subtree add ...` after that will successfully fetch all lfs referenced data.

### git subtree

Updating subtree content is done via `git subtree pull --prefix packages/app git@gitlab.com:production_ml/password_app.git master --squash`