import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clarku_youtube_crawler",
    version="1.0.1.dev",
    maintainer="Cat Mai",
    maintainer_email="CMai@clarku.edu",
    description="Clark University, Package for YouTube crawler and cleaning data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/catxmai/clarku-youtube-crawler",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    dependency_links=['https://pypi.org/project/google-api-python-client/'],
    install_requires=[
        'configparser',
        'datetime',
        'pytz',
        'pandas',
        'youtube_transcript_api',
        'google-api-python-client'
    ],
    include_package_data=True,
    package_data={"clarku_youtube_crawler": ["US_CATE.json"]},
    python_requires='>=3.6',
)
