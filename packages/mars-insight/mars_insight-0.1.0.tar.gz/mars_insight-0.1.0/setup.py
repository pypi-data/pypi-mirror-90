import setuptools

setuptools.setup(
    name='mars_insight',
    version='0.1.0',
    description='Mars InSight weather service API client',
    author='Albert Wigmore',
    author_email='albertwigmore@googlemail.com',
    url='https://github.com/albertwigmore/mars-insight',
    projects_urls={
        'Documentation': '',
        'Source': 'https://github.com/albertwigmore/mars-insight',
        'Tracker': 'https://github.com/albertwigmore/mars-insight/issues'
    },
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'matplotlib',
        'numpy',
        'requests',
    ],
    extras_require={
        'dev': [
            'bandit',
            'flake8',
            'nox',
            'pylint',
            'pytest',
            'pytest-cov',
            'sphinx',
            'sphinx-press-theme',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license='MIT',
)