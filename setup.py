from setuptools import find_packages, setup

VERSION = '0.1.0'

setup(
    name='pyqtweb',  # package name
    version=VERSION,  # package version
    description='my package',  # package description
    packages=find_packages(),
    zip_safe=False,
    author='acorn',
    author_email='wty2580@126.com',
    keywords=['pyqt5', 'webview', 'python webview']
)
