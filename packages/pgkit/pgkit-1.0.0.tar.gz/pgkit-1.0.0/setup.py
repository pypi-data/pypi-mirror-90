from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='pgkit',
    version='1.0.0',
    description='A command-line to make postgresql operations easy',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GPL 3.0',
    packages=find_packages(),
    author='Sadegh Hayeri',
    author_email='hayerisadegh@gmail.com',
    keywords=['postgres', 'postgresql', 'pg', 'pgkit', 'pitr'],
    url='https://github.com/SadeghHayeri/pgkit',
    download_url='https://pypi.org/project/pgkit',
    include_package_data=True,
    entry_points={
        "console_scripts": ['pgkit = src.main:main']
    },
    install_requires=[
        'click==7.1.2',
        'Jinja2==2.11.2',
        'MarkupSafe==1.1.1',
        'tinydb==4.3.0',
    ]
)
