from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(name='liberty-parser',
      version='0.0.8',
      description='Liberty format parser.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='liberty parser',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
          'Programming Language :: Python :: 3'
      ],
      url='https://codeberg.org/tok/liberty-parser',
      author='T. Kramer',
      author_email='dont@spam.me',
      license='GPLv3',
      packages=find_packages(),
      install_requires=[
          'numpy==1.*',
          'sympy==1.6.*',
          'lark-parser==0.7.*'
      ],
      zip_safe=False)
