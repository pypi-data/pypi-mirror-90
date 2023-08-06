import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


# def get_requirements(fname):
#     "Takes requirements from requirements.txt and returns a list."
#     with open(fname) as fp:
#         reqs = list()
#         for lib in fp.read().split("\n"):
#             # Ignore pypi flags and comments
#             if not lib.startswith("-") or lib.startswith("#"):
#                 reqs.append(lib.strip())
#         return reqs


# install_requires = get_requirements("requirements.txt")

setuptools.setup(
    name="notion_writer",
    version="0.0.4",
    author="Puri Phakmongkol",
    author_email="puripmk@gmail.com",
    description="A top level unofficial API for Notion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suakow/notion_writer",
    install_requires=[
        'beautifulsoup4',
        'bs4',
        'cached-property',
        'commonmark',
        'dictdiffer',
        'notion==0.0.27',
        'python-slugify',
        'requests',
        'tzlocal',
        'urllib3',
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)