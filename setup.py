from setuptools import setup, find_packages
from codecs import open

version = open('packaging/VERSION').read().strip()
requirements = open('packaging/requirements.txt').read().split("\n")
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rptk',
    version=version,
    author='Workonline Communications',
    author_email='communications@workonkonline.co.za',
    description='Python tools for prefix filter list management operations',
    long_description=long_description,
    license='LICENSE',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    packages=find_packages(
        include=[
            'rptk',
            'rptk.*'
        ]
    ),
    entry_points={
        'console_scripts': ['rptk=rptk.command_line:main']
    },
    include_package_data=True,
    data_files=[('etc/rptk', ['rptk/rptk.conf'])],
    url='https://github.com/wolcomm/rptk',
    download_url='https://github.com/wolcomm/rptk/%s' % version,
    install_requires=requirements,
)
