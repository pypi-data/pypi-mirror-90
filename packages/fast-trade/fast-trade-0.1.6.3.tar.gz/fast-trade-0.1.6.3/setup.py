import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="fast-trade",
    version="0.1.6.3",
    description="Analyze and backtest algorithmic trading strategies ohlcv data quickly and easily.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jrmeier/fast-trade",
    py_modules=["fast_trade"],
    keywords=[
        "backtesting",
        "currency",
        "ta",
        "pandas",
        "finance",
        "numpy",
        "analysis",
        "technical analysis",
    ],
    author="Jed Meier",
    author_email="fast_trade@jedm.dev",
    license="GNU AGPLv3",
    python_requires=">=3",
    entry_points={"console_scripts": ["ft = fast_trade.cli:main"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
    packages=find_packages(include=["fast_trade"]),
    include_package_data=True,
    install_requires=[
        "cycler==0.10.0",
        "finta==1.2",
        "kiwisolver==1.3.1",
        "matplotlib==3.3.3",
        "numpy==1.19.4",
        "pandas==1.2.0",
        "Pillow==8.1.0",
        "pyparsing==2.4.7",
        "python-dateutil==2.8.1",
        "pytz==2020.5",
        "six==1.15.0",
    ],
)
