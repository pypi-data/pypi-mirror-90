import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RecruitPlotEasy",
    version="1.0.1",
    author="Kenji Gerhardt",
    author_email="kenji.gerhardt@gmail.com",
    description="An interactive readmapping visualization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KGerhardt/RecruitPlotEasy",
    packages=setuptools.find_packages(),
    python_requires='>=3',
	entry_points={
        "console_scripts": [
			"get_sys=RecruitPlotEasy.RecruitPlotEasy:get_sys",
			"parse_to_mags_identical=RecruitPlotEasy.RecruitPlotEasy:parse_to_mags_identical",
			"detect_file_format=RecruitPlotEasy.RecruitPlotEasy:detect_file_format",
			"sqldb_creation=RecruitPlotEasy.RecruitPlotEasy:sqldb_creation",
			"add_sample=RecruitPlotEasy.RecruitPlotEasy:add_sample",
			"add_genes_to_db=RecruitPlotEasy.RecruitPlotEasy:add_genes_to_db",
			"assess_samples=RecruitPlotEasy.RecruitPlotEasy:assess_samples",
			"assess_MAGs=RecruitPlotEasy.RecruitPlotEasy:assess_MAGs",
			"extract_MAG_for_R=RecruitPlotEasy.RecruitPlotEasy:extract_MAG_for_R",
			"extract_genes_MAG_for_R=RecruitPlotEasy.RecruitPlotEasy:extract_genes_MAG_for_R",
			"get_contig_names=RecruitPlotEasy.RecruitPlotEasy:get_contig_names",
			"check_presence_of_genes=RecruitPlotEasy.RecruitPlotEasy:check_presence_of_genes",
        ]
    }
)