import sys
from setuptools import setup


if sys.version_info < (2, 7):
    sys.exit('Zipnish requires at least Python 2.7, please upgrade and try again.')

setup_requires = []

install_requires = [
    'simplemysql',
]

setup(
    name='zipnish',
    version='0.1.0',
    description='zipnish',
    long_description='Micro-services monitoring tool based on Varnish Cache.',
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
    packages=['logreader', 'logreader.log'],
    zip_safe=False,
    install_requires=install_requires,
    setup_requires=setup_requires,
    package_data={
        'logreader': ['default.cfg']
    },
    entry_points={'console_scripts': ['logreader = logreader.app:main']},
    scripts=[]
)
