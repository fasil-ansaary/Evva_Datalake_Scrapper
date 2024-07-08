from setuptools import setup
setup(
    name="evva_datalake_scrapper",
    version="0.1",
    description="Python package to scrape data for evva labs.",
    packages=[
        'controllers',
        'resources'
    ],
    install_requires=[
        'json',
        'pandas',
        'requests',
        'alive_progress',
        'beautifulsoup4',
        'logging',
        'csv',
        'selenium',
        'warnings',
        'geopy',
        'uszipcode',
    ]
)


"""
Virtual machine userId and passwords

Linux machine:
userId: evva-datalake-scrapper
password: Evva-datalake-scrapper1

Windows machine:
userId: @V2scrapperevva
password: v2-scrapper
"""