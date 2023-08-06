import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django_hockeydata_api',
    version='0.0.4',
    description='A Django package for simple use of Hockeydata Javascript API',
    url='https://git.wgdnet.de/cwiegand/django_hockeydata_api.git',
    author='Christian Wiegand',
    license='BSD',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'django',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
)
