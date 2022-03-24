from setuptools import setup, find_packages

setup(
    name='websearchdict',
    version='0.0.1',
    description=("A Dictionary API based on web searches "
                 "(mainly just google search haha)"),
    long_description="""\
        Since there are a lack of Dictionary APIs, I was forced to attempt
        to create my own.  I am simply supplying the source code, not a
        service or product.  If you've searched as hard as the rest of us
        for a good Dictionary API, hopefully this can help! 😄
    """,
    author='nickumia',
    install_requires=[
        'lxml',
        'requests',
        'selenium'
    ],
    packages=find_packages(include=[
        'websearchdict',
        'websearchdict.*'
    ])
)
