import setuptools

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="raisin",
    version="0.0.14",
    author="Robin RICHARD (robinechuca)",
    author_email="raisin@ecomail.fr",
    description="Simple parallel, distributed and cluster computing",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://framagit.org/robinechuca/raisin",
    packages=setuptools.find_packages(),
    install_requires=["pycryptodomex", "cloudpickle"], # ces paquets serons installes d'office
    extras_require={
        "calculation": ["sympy", "giacpy", "numpy"],
        "tools": ["psutil>=5.1", "regex", "cloudpickle"],
        "graphical": ["tkinter", "matplotlib"],
        "security": ["pycryptodomex"]
        },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",

        "Natural Language :: French",

        # "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        # "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        ],
    keywords=["parallel", "distributed", "cluster computing"],
    python_requires=">=3.6",
    project_urls={
        "Source Repository": "https://framagit.org/robinechuca/raisin/-/tree/master/raisin",
        # "Bug Tracker": "https://github.com/engineerjoe440/ElectricPy/issues",
        # "Documentation": "https://engineerjoe440.github.io/ElectricPy/",
        # "Packaging tutorial": "https://packaging.python.org/tutorials/distributing-packages/",
        },
    include_package_data=True,
)
