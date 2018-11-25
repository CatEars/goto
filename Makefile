default:

compile:
	python3 setup.py sdist bdist_wheel

testupload: compile
	twine upload --repository testpypi dist/*

venvinstall:
	virtualevn --python python3

venv:
	source venv/bin/activate

clean:
	rm -rf dist build goto_cd.egg-info

test:

coverage:

installtest:
	pip install --index-url "https://test.pypi.org/simple/" goto-cd

upload-new-distribution:
	twine upload dist/*

