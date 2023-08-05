from setuptools import setup
def readme():
    with open('README.rst') as f:
        return f.read()
setup(name='deepagi_cli_test',
      version='0.1.26',
      description='Testing CLI Commands',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='deepagi',
      url='',
      author='delan',
      author_email='',
      license='MIT',
      packages=['deepagi_cli_test'],
      install_requires=[
#           'markdown',
      ],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
        'console_scripts': ['deepagi_cli = deepagi_cli_test.commands:entry']
    },
      # scripts=['bin/deepagi_cli'],
      # data_files=[('templates')]
     )