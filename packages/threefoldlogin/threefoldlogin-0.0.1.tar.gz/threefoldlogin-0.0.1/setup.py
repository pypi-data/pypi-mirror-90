import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="threefoldlogin",
    version="0.0.1",
    author="Tobias Chielens",
    author_email="tobias.chielens@jimber.org",
    description="Python package for the threebot authenticator app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/threefoldtech/threefold-login-python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "mnemonic~=0.19",
        "pysodium~=0.7.5",
        "requests~=2.24.0"
    ]
)