import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gsheet-alpa",
    version="0.0.10",
    author="Albert Pang",
    author_email="alpaaccount@mac.com",
    description="Package for working with Google Sheet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/alpaalpa/gsheet/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'gspread',
        'gspread_dataframe',
        'numpy',
        'oauth2client',
        'pandas'
    ],
    python_requires='>=3.6',
)
