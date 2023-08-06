from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='distributions_wk',
      version='0.1',
      description='Gaussian distributions by wk',
      packages=['distributions'],
      zip_safe=False)
