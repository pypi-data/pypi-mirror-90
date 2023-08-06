import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goldpot",
    version="0.0.3",
    author="Sebastian Senge",
    author_email="mail@sebastian-senge.de",
    description="A thin convenience layer on top of OpenAI's GPT-3 Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssenge/Goldpot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
