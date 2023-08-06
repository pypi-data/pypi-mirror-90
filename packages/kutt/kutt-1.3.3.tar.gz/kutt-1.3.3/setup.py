from setuptools import setup

setup(
    name='kutt',
    version='1.3.3',
    description='API wrapper and CLI for kutt.it',
    author='Amirali Esfandiari',
    author_email='amiralinull@gmail.com',
    url='http://github.com/amirali/kutt',
    py_modules=['kutt'],
    install_requires=['fire', 'requests', 'toml'],
    packages=['kutt'],
    package_dir={'kutt': 'kutt'},
    python_requires='>=3',
    classifiers=[
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        ],
    entry_points = '''
        [console_scripts]
        kutt=kutt.cli:main
    ''',
)
