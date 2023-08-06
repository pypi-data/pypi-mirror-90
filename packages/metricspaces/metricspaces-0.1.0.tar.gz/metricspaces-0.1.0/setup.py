import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metricspaces",
    version="0.1.0",
    author="Donald R. Sheehy",
    author_email="don.r.sheehy@gmail.com",
    description="A package for computing wiht metric spaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donsheehy/metricspaces",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
        install_requires =[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        metricspaces=metricspaces.cli:cli
    '''
)
