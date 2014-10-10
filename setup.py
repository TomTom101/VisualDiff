try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Visual comparison of automatically generated screenshots. ',
    'author': 'Thomas Brandl',
    'url': 'https://github.com/TomTom101/VisualDiff',
    'download_url': 'https://github.com/TomTom101/VisualDiff',
    'author_email': 'thomas.brandl@native-instruments.de',
    'version': '0.1',
    'scripts': ['vdcapture.py', 'vdcompare.py'],
    'name': 'visualdiff'
}

setup(**config)