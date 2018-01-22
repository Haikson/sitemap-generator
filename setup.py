from distutils.core import setup
from setuptools import find_packages, setup

EXCLUDE_FROM_PACKAGES = ['tests',]


def get_version(major=0, minor=0, build=0):
    return '%s.%s.%s' % (major, minor, build)


setup(
    name='sitemap-generator',
    version=get_version(
        major=0,
        minor=5,
        build=2,
    ),
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    url='https://github.com/Haikson/sitemap-generator',
    license='GPL3',
    author='Kamo Petrosyan',
    author_email='kamo@haikson.com',
    description='web crawler and sitemap generator.',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['lxml', 'requests'],
    requires=['lxml', 'requests']
)