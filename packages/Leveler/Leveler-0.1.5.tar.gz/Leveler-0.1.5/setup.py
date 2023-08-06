from setuptools import setup, find_packages

setup(name='Leveler',
      version='0.1.5',
      description='Simple and small package to build levels of support and resistance',
      long_description='Simple and small package to build levels of support and resistance',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='algotrading trading support resistance levels',
      url='https://github.com/FuturFuturFutur/leveler.git',
      author='Futur',
      author_email='yaroviy.yaroslav@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'cython',
          'numpy',
          'pandas',
          'zigzag',
          'sklearn'
      ],
      include_package_data=True,
      zip_safe=False)
