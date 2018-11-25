default:

compile:
	python3 setup.py sdist bdist_wheel

testupload: compile
	twine upload --repository testpypi dist/*

devinstall:
	pipenv install --dev

clean:
	rm -rf dist build goto_cd.egg-info

test:
	pipenv run py.test

coverage:
	pipenv run py.test --cov=goto --cov-report=html

install-test-package:
	pip install --user --index-url "https://test.pypi.org/simple/" goto-cd

upload-new-distribution:
	twine upload dist/*

