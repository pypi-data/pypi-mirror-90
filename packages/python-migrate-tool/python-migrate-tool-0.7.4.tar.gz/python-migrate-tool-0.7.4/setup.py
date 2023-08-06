
from setuptools import (
    find_packages,
    setup,
)

setup(
    name='python-migrate-tool',
    # *IMPORTANT*: Don't manually change the version here. Use the 'bumpversion' utility.
    version='0.7.4',
    description="""PlatON alaya python tool""",
    # long_description_markdown_filename='README.md',
    author='shinnng',
    author_email='shinnng@outlook.com',
    url='https://github.com/AlayaNetwork/python-migrate-tool',
    include_package_data=True,
    install_requires=[
        "toolz>=0.9.0,<1.0.0;implementation_name=='pypy'",
        "cytoolz>=0.9.0,<1.0.0;implementation_name=='cpython'",
        "eth-hash[pycryptodome]>=0.2.0,<1.0.0",
        "pypiwin32>=223;platform_system=='Windows'", 'collections2'
    ],
    setup_requires=['setuptools-markdown'],
    python_requires='>=3.6,<4',
    license="MIT",
    zip_safe=False,
    keywords='platon',
    packages=find_packages(),
    package_data={'':['*.md']},
    scripts=['testfile.py'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
