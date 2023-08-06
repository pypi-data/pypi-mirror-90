from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='wmempy',
    version='0.1.0',
    description='WinApi Memory Access Application',
    long_description=long_description,
    author='Petr Ančinec',
    author_email='ancinpet@fit.cvut.cz',
    keywords='click,winapi,openprocess',
    license='MIT License',
    url='https://github.com/fitancinpet/WMemPy',
    packages=['wmempy'],
    install_requires=['pywin32', 'click>=6', 'numpy==1.19.3'],
    setup_requires=['pytest-runner', 'pywin32', 'click>=6', 'numpy==1.19.3'],
    tests_require=['pytest', 'pywin32', 'click>=6', 'numpy==1.19.3', 'flexmock', 'sphinx'],
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: Microsoft',
        'Topic :: Software Development :: Libraries'
    ],
    entry_points={
        'console_scripts': [
            'wmempy=wmempy.wmem_cli:main',
        ],
    },
    zip_safe=False
)
