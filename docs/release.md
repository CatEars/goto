Developer checklist on new major release

[ ] Make sure all unit tests pass
[ ] Make sure all bash tests pass
[ ] Make sure all zsh tests pass
[ ] Make sure Travis passes all above tests
[ ] Up affected version and compile
[ ] Make sure uploading to test pypi can install and then run bash/zsh tests

* At this point we are confident that the commit is an okay release, it is time to release it.

[ ] Create new coverage badge
[ ] Update changelog with included updates
[ ] Commit both above
[ ] Push and make sure that Travis still passes
[ ] Add tag to commit and push the tag, Travis should update PyPI
[ ] Make sure that PyPI page is updated
[ ] Make sure that PyPI goto-cd can be installed locally with newest version
[ ] Make sure that bash/zsh tests pass with newest version

