# rm -rf ./dist
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository pypi dist/*
#
# more info here:
# https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi

import setuptools

setuptools.setup(name = 'gallery_get',
    version = '1.8.17',
    author = 'Rego Sen',
    author_email = 'regosen@gmail.com',
    url = 'https://github.com/regosen/gallery_get',
    description = 'Gallery downloader - supports many galleries and reddit user histories',
    long_description = open("README.rst","r").read(),
    long_description_content_type = "text/markdown",
    license = 'MIT',
    keywords = 'gallery downloader reddit imgur imgbox 4chan xhamster eroshare vidble pornhub xvideos imagebam alphacoders',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        'Topic :: Multimedia :: Graphics',
    ],
)