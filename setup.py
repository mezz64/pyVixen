# Copyright (c) 2017 John Mihalic <https://github.com/mezz64>
# Licensed under the MIT license.

# Used this guide to create module
# http://peterdowns.com/posts/first-time-with-pypi.html

# git tag 0.1 -m "0.1 release"
# git push --tags origin master
#
# Upload to PyPI Live
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi


from distutils.core import setup
setup(
    name='pyVixen',
    packages=['pyvixen'],
    version='0.0.1',
    description='Provides a python api to interact with the Vixen 3.2+ Web API.',
    author='John Mihalic',
    author_email='mezz64@users.noreply.github.com',
    url='https://github.com/mezz64/pyVixen',
    download_url='https://github.com/mezz64/pyvixen/tarball/0.0.1',
    keywords=['vixen', 'lights', 'vixenlights', 'led', 'christmas', 'api wrapper', 'homeassistant'],
    classifiers=[],
    )
