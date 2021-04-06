from setuptools import setup, find_packages

long_description = """Experimental package to explore portfolio construction with an optimizer"""

setup(name='pct',
      version='0.1',
      description='Portfolio construction tool',
      author='Yevgeniy Yermoshin',
      author_email='yev.developer@gmail.com',
      license='Apache 2.0',
      long_description=long_description,
      keywords=['pandas', 'data', 'analysis', 'fixed income', 'stocks', 'bond', 'equities', 'portfolio construction', 'portfolio optimization'],
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
