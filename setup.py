from setuptools import find_packages, setup

setup(
    name="empatia",
    version="0.0.1",
    description="Support system for decision making in air quality management",
    author="CONAE-Empatia team",
    author_email="",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "modapsclient",
        "numpy",
        "pandas",
        "requests",
        "scikit-learn",
        "tqdm",
    ],
    entry_points="""
        [console_scripts]
        empatia=empatia.cli:main
    """,
)
