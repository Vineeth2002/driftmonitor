# setup.py – minimal packaging so workflows can pip install -e .
from setuptools import setup, find_packages

setup(
    name="driftmonitor",
    version="0.0.1",
    description="DriftMonitor — lightweight AI safety & drift monitoring",
    packages=find_packages(include=["driftmonitor", "driftmonitor.*"]),
    install_requires=[
        "PyYAML>=6.0",
        "requests>=2.28",
        "jinja2>=3.0",
        "pandas>=2.0",
    ],
    include_package_data=True,
    zip_safe=False,
)
