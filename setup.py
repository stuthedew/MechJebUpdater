from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='mechjeb_updater',
      version='0.1',
      description='Syncs ksp-avc compatible fork and updates version file',
      long_description=readme(),
      url='https://github.com/stuthedew/mechjeb_updater',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Topic :: System :: Installation/Setup',
      ],
      author='Stuart Feichtinger',
      author_email='stuart.feichtinger@gmail.com',
      keywords='Kerbal MechJeb MechJeb2',
      license='MIT',
      packages=['mechjeb_updater'],
      install_requires=[
          'requests',
      ],
      scripts=['bin/updateMechJeb'],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
