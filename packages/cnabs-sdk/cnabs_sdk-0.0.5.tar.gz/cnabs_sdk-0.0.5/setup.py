__author__ = "Bo Pan"

from setuptools import setup, find_packages

with open("./cnabssdk/PackHelper.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='cnabs_sdk',
      version='0.0.5', 
      description='CNABS OPENAPI SDK',
      author='Bo Pan', 
      author_email='bo.pan@cn-abs.com',
      url='https://github.com/cnabs',
      packages= ["cnabssdk", "cnabssdk.common"], 
      long_description=long_description,
      long_description_content_type="text/markdown", 
      license="GPLv3", 
      classifiers=[
          "Programming Language :: Python :: 3", 
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent"],
      python_requires='>=3.3',
      install_requires=[
          "requests>=2.2.0",
          ]
      )