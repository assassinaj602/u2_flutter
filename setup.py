from setuptools import setup, find_packages

setup(
    name="u2-flutter",
    version="0.1.0",
    description="Flutter driver plugin for uiautomator2 - find and interact with Flutter widgets",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    author="assassinaj602",
    url="https://github.com/assassinaj602/u2_flutter",
    packages=find_packages(),
    install_requires=[
        "uiautomator2>=3.0.0",
        "websocket-client>=1.0.0",
        "requests>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
)
