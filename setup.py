import setuptools

setuptools.setup(
    name="superdad",
    version="0.0.1",
    author="xy.zhang",
    description="Superdad Stock Market Analyzer",
    long_description='',
    long_description_content_type="text/markdown",
    license='MIT',
    include_package_data=True,
    zip_safe=True,
    url="",
    packages=setuptools.find_packages(exclude=['docs', 'tests', 'protos']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['requests', 'pika', 'sqlalchemy'],
    test_requires=['pytest'],
    entry_points={'console_scripts': [
        'superdad = superdad.commands:cli',
    ]}
)
