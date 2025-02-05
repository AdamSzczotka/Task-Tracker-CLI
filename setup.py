from setuptools import setup, find_packages

setup(
    name="task_cli",
    version="1.0.0",
    description="A CLI application to manage tasks.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Adam Szczotka",
    author_email="adam.szczotka0@gmail.com",
    url="https://github.com/AdamSzczotka/Task-Tracker-CLI",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "task_cli=task_cli:main",
        ],
    },
    install_requires=open("requirements.txt").read().splitlines(),
    extras_require={"test": ["pytest"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
