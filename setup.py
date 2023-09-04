import setuptools

setuptools.setup(
    name="recommender_system",
    version="0.0.0",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    description="Industrial and Scientific Product Recommender System."
)
