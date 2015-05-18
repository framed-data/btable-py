from setuptools import setup, find_packages
setup(name="btable-py",
      version="0.1.0",
      packages=find_packages(),
      install_requires=[],
      author="Andrew Berls",
      author_email="andrew@framed.io",
      description="A binary serialization format for sparse, "
                  "labeled 2D numeric datasets",
      url="https://github.com/framed-data/btable-py",
      package_data={
          'btable': ['data/*.btable']
      })
