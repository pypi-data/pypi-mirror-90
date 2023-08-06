from setuptools import setup, find_packages

'''
Upgrade line
'''
#python setup.py sdist bdist_wheel
#python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


setup(
    name='adnar-scraper',
    version='0.1.92',
    description='adnar-scraper',
    author              = 'Mabus Kang',
    author_email        = 'discoverious@naver.com',
    url                 = 'https://github.com/discoverious/adnar-scraper',
    download_url        = 'https://github.com/discoverious/adnar-scraper/archive/0.0.tar.gz',
    install_requires    =  [],
    packages            = find_packages(exclude = []),
    keywords            = ['AdnarScraper'],
    python_requires     = '>=3.6',
    package_data        = {},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)