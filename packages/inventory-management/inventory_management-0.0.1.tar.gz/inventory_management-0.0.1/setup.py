from pathlib import Path
import os

from setuptools import find_packages, setup  # type: ignore


def read(file_name: str):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


# Read the contents of README file
source_root = Path(".")

# Read the requirements
with (source_root / "requirements.txt").open(encoding="utf8") as f:
    requirements = f.readlines()

with (source_root / "requirements-test.txt").open(encoding="utf8") as f:
    test_requirements = f.readlines()

with (source_root / "requirements-dev.txt").open(encoding="utf8") as f:
    dev_requirements = f.readlines()

meta: dict = {}
exec(read("src/inventory_management/__meta__.py"), meta)

extras_requires = {
    "dev": dev_requirements,
    "test": test_requirements,
}


setup(
    name=meta["name"],
    version=meta["version"],
    license=meta["license"],
    url=meta["url"],
    description="",
    author=meta["author"],
    author_email=meta["author_email"],
    package_data={"inventory_management": ["py.typed"]},
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requirements,
    include_package_data=True,
    tests_require=test_requirements,
    extras_require=extras_requires,
    python_requires=">=3.8",
    long_description="",
    long_description_content_type="text/x-rst",
    zip_safe=False,
)
