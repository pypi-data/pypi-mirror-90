from setuptools import setup

setup(name='dataanalyser',
	version='0.1.3',
	description='Automates Exploratory Data Analysis',
	author = 'shalu Tyagi',
	author_email='shalu.tyagi03@gmail.com',
	packages=['dataanalyser'],
    license="MIT",
    classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
    ],
	install_requires=['pandas',
					'seaborn',
					'numpy',
					'scipy',
					'matplotlib',
					'python-dateutil','setuptools'],
    entry_points="""
        [console_scripts]
        contacts=app:cli
        """,
        )