import re

from setuptools import find_packages, setup

with open('README.rst', encoding='utf8') as f:
    long_description = f.read()

with open('brawlstats/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='brawlstats',
    version=version,
    description='An easy-to-use wrapper for the Brawl Stars API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/SharpBit/brawlstats',
    author='SharpBit',
    author_email='sharpbit3618@gmail.com',
    license='MIT',
    keywords=['brawl stars, brawlstats, supercell'],
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5.3',
    project_urls={
        'Source Code': 'https://github.com/SharpBit/brawlstats',
        'Issue Tracker': 'https://github.com/SharpBit/brawlstats/issues',
        'Documentation': 'https://brawlstats.readthedocs.io/',
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Natural Language :: English'
    ]
)
