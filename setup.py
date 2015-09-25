from setuptools import setup

setup(
    name='frostbite-rcon-utils',
    version='2.0.0',
    author='Edvin Erikson',
    author_email='edvin@rocketblast.com',
    url='https://github.com/edvinerikson/frostbite-rcon-utils-python',
    download_url='https://github.com/edvinerikson/frostbite-rcon-utils-python',
    license='MIT',
    description="A library that takes care of the encoding and decoding of packets sent to or " +
                "from a Battlefield server (or any other server that uses their protocol).",
    platforms=('Windows', 'Linux', 'Mac OS X'),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='tests',
    packages=['frostbite_rcon_utils'],
    keywords = 'rcon battlefield frostbite protocol encode decode',
)
