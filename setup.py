import sys

from setuptools import setup, find_packages

if sys.version_info < (2, 7):
    sys.exit('Zipnish requires at least Python 2.7, please upgrade and try again.')


def read(filename):
    with open(filename) as f:
        return f.read()


install_requires = [
    'simplemysql', 'flask', 'sqlalchemy', 'flask_sqlalchemy',
]

setup(
    include_package_data=True,
    name='zipnish',
    version='0.1.2',
    description='zipnish',
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',     
        'Programming Language :: Python :: 2.7',
    ],
    author='Adeel Shahid, Per Buer, Marius Magureanu',
    author_email='marius@varnish-software.com',
    url='https://github.com/varnish/zipnish.git',
    license='Apache License 2.0',
    platforms='Linux',
    packages=find_packages(exclude=['logreader.test']),
    zip_safe=False,
    install_requires=install_requires,
    package_data={
        'logreader': ['default.cfg'],
    },
    entry_points={'console_scripts': ['zipnish-logreader = logreader.app:main',
                                      'zipnish-ui = ui.flask_app:main'],
                  },
    scripts=[]
)
