import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

import softlakelib.__init__ as ini


setuptools.setup(
    name="softlake",
    version=ini.__version__,
    author="Massimiliano Cannata",
    author_email="massimiliano.cannata@gmail.com",
    description="Primary Production: library to estimate primary production in lakes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ist-supsi.gitlab.io/softlake/",
    packages=setuptools.find_packages(),
    install_requires=[
        'matplotlib',
        'pandas',
        'scipy',
        'numpy',
        'scipy',
        'PyYAML'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# install_requires=[
#         'datetime','dateutil','osgeo','pandas','numpy','scipy'
#         'requests','StringIO','os','io','pyspatialite','copy','isodate',
#         '__future__','json','math','calendar'
#     ]

# packages=setuptools.find_packages(),