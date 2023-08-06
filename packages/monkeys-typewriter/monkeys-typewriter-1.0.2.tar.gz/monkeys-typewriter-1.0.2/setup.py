from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='monkeys-typewriter',
      version=open('VERSION').read(),
      description="Monkey's Typewriter PEG parser",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Adam Green',
      author_email='adam@tryal.ai',
      donwload_url='https://github.com/tryal-ai/mnkytw/archive/1.0.1.tar.gz',
      url='https://tryal.ai/',
      packages=find_packages(),
      keywords=["PEG", "parser", "grammar"],
      python_requires='>=3.6',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)