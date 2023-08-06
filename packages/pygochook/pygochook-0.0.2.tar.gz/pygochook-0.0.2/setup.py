import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygochook", # Replace with your own username
    version="0.0.2",
    author="Lars Heinen",
    author_email="larsheinen@gmail.com",
    description="A simple python package to send messages to Google Chats via Webhooks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lars147/pygochook",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "aiohttp>=3.7"
    ]
)