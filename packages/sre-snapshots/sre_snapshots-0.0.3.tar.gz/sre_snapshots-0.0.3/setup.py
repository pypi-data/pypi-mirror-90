from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='sre_snapshots',
      version='0.0.3',
      description='Download search snapshots from MongoDB',
      url='',
      author='James Wolman',
      author_email="James.Wolman@found.co.uk",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['sre_snapshots'],
      install_requires=requirements,
      include_package_data=True,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Development Status :: 1 - Planning",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Programming Language :: Python :: 3.7"
      ],
      zip_safe=False)
