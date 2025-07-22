from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="MULTI-AI-AGENT",
    version="1.0.0",
    author="Shivam Kumar Srivastava",
    packages=find_packages(),
    install_requires = requirements,
)