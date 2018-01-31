import setuptools

setuptools.setup(
    name="dovecot-acl-inherit",
    version="0.1.0",
    url="https://github/modulus-sa/dovecot-acl-inherit",

    author="Konstantinos Tsakiltzidis",
    author_email="ktsakiltzidis@modulus.gr",

    description="Adhoc command to delegate dovecot ACL files to mailboxes",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    entry_points={
        'console_scripts': [
            'dovecot-acl-inherit = dacli.__main__:main'
        ]
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
