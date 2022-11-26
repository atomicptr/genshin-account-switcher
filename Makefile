.PHONY: build

build:
	python setup.py bdist_wheel

install: build
	python -m pip install dist/genshin_account_switcher-*.whl --force-reinstall

clean:
	rm -rf build dist genshin_account_switcher.egg-info

upload: clean build
	python -m twine upload dist/genshin_account_switcher-*.whl