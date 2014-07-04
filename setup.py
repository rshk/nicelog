from setuptools import setup, find_packages
import os

version = '0.1.6'

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst')) as fp:
    longdesc = [fp.read()]

with open(os.path.join(here, 'CHANGELOG.rst')) as fp:
    longdesc.append(fp.read())

longdesc = "\n\n".join(longdesc)

setup(
    name='nicelog',
    version=version,
    packages=find_packages(),
    url='http://github.com/rshk/nicelog',
    license='BSD',
    author='Samuele Santi',
    author_email='samuele@samuelesanti.com',
    description='Nice colorful formatters for Python logging.',
    long_description=longdesc,
    install_requires=[],
    # tests_require=tests_require,
    test_suite='tests',
    classifiers=[
        "License :: OSI Approved :: BSD License",
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        # "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",

        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    package_data={'': ['README.rst']},
    include_package_data=True,
    zip_safe=False)
