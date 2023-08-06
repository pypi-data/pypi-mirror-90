from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name="imgflip",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author="axju",
    author_email="moin@axju.de",
    description="api to imgflip",
    long_description=readme(),
    long_description_content_type='text/x-rst',
    url="https://github.com/axju/imgflip",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['imgflip'],
    install_requires=[
        'requires'
    ],
    entry_points={
        'console_scripts': ['imgflip=imgflip.cli:main'],
    },
)
