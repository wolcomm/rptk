from setuptools import setup, find_packages

version = open('packaging/VERSION').read().strip()
requirements = open('packaging/requirements.txt').read().split("\n")
test_requirements = open('packaging/requirements-test.txt').read().split("\n")
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
        ],
        exclude=[]
    ),
    entry_points={
        'console_scripts': ['rptk=rptk.command_line:main']
    },
    include_package_data=True,

    url='https://github.com/wolcomm/rptk',
    download_url='https://github.com/wolcomm/rptk/%s' % version,

    install_requires=requirements,
    tests_require=test_requirements,
    test_suite='nose.collector'
)
