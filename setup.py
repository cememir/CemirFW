from setuptools import setup, find_packages

ver = "1.0.1"

setup(
    name='cemirfw',
    version=ver,
    packages=find_packages(),
    install_requires=[
        'tornado',
    ],
    author='Cem Emir Yüksektepe / Muslu Yüksektepe (musluyuksektepe@gmail.com)',
    author_email='cememir2017@gmail.com',
    description='CemirFW is a lightweight framework for building REST APIs using Tornado. It provides decorators to register routes for different HTTP methods (GET, POST, PUT, DELETE) and handles HTTP requests accordingly.',
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
