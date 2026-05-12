from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="airgent-play2",
    version="0.1.0",
    description="Airgent Play 2 — Give your AI agents a voice via AirPlay 2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Airgent Play2 contributors",
    url="https://github.com/rockeverm3m/airgent-play2",
    packages=find_packages(),
    python_requires=">=3.12",
    install_requires=[
        "pyatv>=0.17.0",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "airgent-play2=airgent_play2.core:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Home Automation",
    ],
)
