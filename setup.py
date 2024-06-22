# setup.py

from setuptools import setup, find_packages

from cemirfw import ver

setup(
    name='cemirfw',
    version=ver,
    packages=find_packages(),
    install_requires=[],
    author='Cem Emir Yüksektepe / Muslu Yüksektepe (musluyuksektepe@gmail.com)',
    author_email='cememir2017@gmail.com',
    description='Fast and Basic Async Python Framework...',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cememir/cemirfw',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
