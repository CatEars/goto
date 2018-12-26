default:

# These are typically used by humans

compile:
	python3 setup.py sdist bdist_wheel

testupload: compile
	twine upload --repository testpypi dist/*

devinstall:
	pipenv install --dev

clean:
	rm -rf dist build src/goto_cd.egg-info htmlcov src/goto/**.pyc src/goto/__pycache__

test:
	pipenv run tox -e unit

coverage:
	pipenv run tox -e coverage


# I don't think I ever explain why I generate the coverage badge myself
coverage-badge:
	pipenv run tox -e coverage-badge
	pipenv run coverage-badge -o coverage.tmp.svg
	mv coverage.tmp.svg badges/coverage.svg

lint:
	pipenv run pylint src/goto --rcfile=pylintrc

live-tests: live-bash-tests live-zsh-tests live-py2-bash-tests live-py2-zsh-tests

# These are typically not used by humans
# I mean, you are free to do mostly what you want in life.
# I won't even try to personally stop you.
# But these are mostly robot stuff.
# So..
# Ya know...

# Tests the latest pypi version using bash
live-bash-tests:
	docker build . -f docker-tests/Dockerfile-live-bashtest -t goto_ubuntu_bashlivetest
	docker run -e SHELL=bash -e RCFILE=/root/.bashrc goto_ubuntu_bashlivetest

# Tests the latest pypi version using zsh
live-zsh-tests:
	docker build . -f docker-tests/Dockerfile-live-zshtest -t goto_ubuntu_zshlivetest
	docker run -e SHELL=zsh -e RCFILE=/root/.zshrc goto_ubuntu_zshlivetest

# Tests the latest pypi version using bash and python2
live-py2-bash-tests:
	docker build . -f docker-tests/Dockerfile-live-py2-bashtest -t goto_ubuntu_py2_bashlivetest
	docker run -e SHELL=bash -e RCFILE=/root/.bashrc goto_ubuntu_py2_bashlivetest

# Tests the latest pypi version using zsh and python2
live-py2-zsh-tests:
	docker build . -f docker-tests/Dockerfile-live-py2-zshtest -t goto_ubuntu_py2_zshlivetest
	docker run -e SHELL=zsh -e RCFILE=/root/.zshrc goto_ubuntu_py2_zshlivetest

zsh-tests: compile
	docker build . -f docker-tests/Dockerfile-zshtest -t goto_ubuntu_zshtest
	docker run -e SHELL=zsh -e RCFILE=/root/.zshrc goto_ubuntu_zshtest

bash-tests: compile
	docker build . -f docker-tests/Dockerfile-bashtest -t goto_ubuntu_bashtest
	docker run -e SHELL=bash -e RCFILE=/root/.bashrc goto_ubuntu_bashtest

full-tox-test: compile devinstall
	pipenv run tox -c tox.ini

install-test-package:
	pip3 install --user --index-url "https://test.pypi.org/simple/" --extra-index-url "https://pypi.org/simple/" goto-cd

upload-new-distribution:
	twine upload dist/*

