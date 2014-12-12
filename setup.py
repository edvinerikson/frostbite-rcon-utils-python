from setuptools import setup

setup(
    name='frostbite-rcon-utils',
    version='0.0.1',
    author='Edvin Erikson',
    author_email='edvin@rocketblast.com',
    url='http://github.com/rocketblast/frostbite-rcon-utils',
    download_url='http://github.com/rocketblast/frostbite-rcon-utils',
    license='MIT',
    description="lightweight library for connecting to an frostbite based game (bf3, bf4, bfh, mohw, bc2)",
    platforms= ('Windows', 'Linux', 'Mac OS X'),
    classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7'
    ],
    packages=['rcon'],
    keywords = 'rocketblast rcon battlefield frostbite',
)