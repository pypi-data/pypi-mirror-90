import setuptools

setuptools.setup(
    name="RhythmCount",
    version="0.0",
    author="Nina Velikajne, Miha Moškon",
    author_email="nv6920@studnet.uni-lj.si, miha.moskon@fri.uni-lj.si",
    description="Python package for cosinor based rhytmometry in count data",
    url="https://github.com/ninavelikajne/RhythmCount",
    packages=setuptools.find_packages(),
    download_url = 'https://github.com/ninavelikajne/RhythmCount/archive/v0.0.tar.gz',
    keywords = ['cosinor', 'rhytmometry', 'regression', 'count data'],
    install_requires=[
          'pandas',
          'numpy',
          'matplotlib',
          'statsmodels',
          'scipy'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)