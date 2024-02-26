from setuptools import setup, find_packages

setup(
    name='trio_mongodb',
    version='0.3.0',
    packages=find_packages(),
    install_requires=['trio', 'pymongo', 'hypercorn', 'httpx', 'starlette'],
    python_requires='>=3.8',
    author='obnoxious',
    author_email='obnoxious@dongcorp.org',
    description='Trio pymongo wrapper for async operations using threads or processes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/obnoxiousish/trio_mongodb',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
