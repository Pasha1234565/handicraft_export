from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="handicraft_export",
	version="0.0.1",
	description="Export Readiness & Subcontracting for Handicrafts — ERPNext v15",
	author="Your Company",
	author_email="info@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
