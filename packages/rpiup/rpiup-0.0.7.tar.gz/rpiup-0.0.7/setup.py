import os
import glob
import setuptools

USERNAME = 'beasteers'
NAME = 'rpiup'


setuptools.setup(
    name=NAME,
    version='0.0.7',
    description='',
    long_description=open('README.md').read().strip(),
    long_description_content_type='text/markdown',
    author='Bea Steers',
    author_email='bea.steers@gmail.com',
    url='https://github.com/{}/{}'.format(USERNAME, NAME),
    packages=setuptools.find_packages(),
    package_data={
        NAME: [
            os.path.relpath(f, NAME) for f in glob.glob(
                os.path.join(os.path.dirname(__file__), 'rpiup/boot-files/**/*'), recursive=True)
        ]},
    entry_points={'console_scripts': ['{name}={name}:cli'.format(name=NAME)]},
    install_requires=['fire'],
    extras_require={
        'monitor': ['flask', 'sqlitedict', 'PyYAML'],
    },
    license='BSD 3-Clause Clear License',
    keywords='raspberrypi raspberry pi os firstboot setup boot partition install iot fleet')
