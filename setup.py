from setuptools import find_packages, setup
from version import VERSION

EXCLUDE_FROM_PACKAGES = ['tests',]

def get_long_description():
    long_description = ""
    with open("README.rst", "r") as fh:
        long_description = fh.read()
    return long_description

def get_requirements():
    requirements = []
    with open('requirements.txt', 'r') as df:
        requirements = df.readlines()
    return [requirement.strip() for requirement in requirements]


setup(
    name='sitemap-generator',
    version=VERSION,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    url='https://github.com/Haikson/sitemap-generator',
    license='GPL3',
    author='Kamo Petrosyan',
    author_email='kamo@haikson.com',
    description='web crawler and sitemap generator.',
    long_description=get_long_description(),
    long_description_content_type="text/x-rst",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=get_requirements(),
    requires=get_requirements()
)