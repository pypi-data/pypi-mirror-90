import os
from glob import glob
from setuptools import setup, find_packages

dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(dir, 'README.md')) as f:
    long_description = f.read()

setup(name='cerebellum_value_map',
      version='0.1.0',
      author='Shuo Han',
      description='Show colors on a cerebellum illustration.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='shan50@jhu.edu',
      url='https://github.com/shuohan/cerebellum-value-map',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy', 'svgwrite', 'matplotlib', 'pandas'],
      python_requires='>=3.7',
      include_package_data=True,
      scripts=glob('scripts/*'),
      classifiers=['Programming Language :: Python :: 3',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent'])
