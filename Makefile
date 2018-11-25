default:

# These are typically used by humans

compile:
	python3 setup.py sdist bdist_wheel

testupload: compile
	twine upload --repository testpypi dist/*

devinstall:
	pipenv install --dev

clean:
	rm -rf dist build goto_cd.egg-info

test:
	pipenv run tox -e unit

coverage:
	pipenv run tox -e coverage


# These are typically not used by humans

zsh-tests:
	echo "ZSH tests unimplemented"

bash-tests:
	echo "Bash tests unimplemented"

full-tox-test:
	pipenv run tox -c tox.ini

install-test-package:
	pip install --user --index-url "https://test.pypi.org/simple/" goto-cd

upload-new-distribution:
	twine upload dist/*

