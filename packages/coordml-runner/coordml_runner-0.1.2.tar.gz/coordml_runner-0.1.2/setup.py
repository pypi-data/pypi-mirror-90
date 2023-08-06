import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="coordml_runner",
    version="0.1.2",
    author="Yichen Xu",
    author_email="yichen.xu@monad.email",
    description="Python CoordML Runner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coordml/runner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['aiohttp', 'pyyaml', 'parse', 'gpustat'],
    entry_points={
        'console_scripts': ['cm_runner=coordml_runner.cli:main']
    }
)
