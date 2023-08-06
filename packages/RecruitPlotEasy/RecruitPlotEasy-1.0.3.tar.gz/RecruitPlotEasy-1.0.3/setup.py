import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RecruitPlotEasy",
    version="1.0.3",
    author="Kenji Gerhardt",
    author_email="kenji.gerhardt@gmail.com",
    description="An interactive readmapping visualization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KGerhardt/RecruitPlotEasy",
    packages=setuptools.find_packages(),
    python_requires='>=3'
)