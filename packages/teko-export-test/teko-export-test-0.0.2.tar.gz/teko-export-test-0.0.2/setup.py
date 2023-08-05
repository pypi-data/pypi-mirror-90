import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    fh.close()

setuptools.setup(
    name="teko-export-test",
    version="0.0.2",
    author="dungntc",
    author_email="dungntc@vnpay.vn",
    description="export test case file and test cycle file for teko-tool push to jira",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)
