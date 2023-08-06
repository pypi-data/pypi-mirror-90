import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="log-util-huynhnt",
    version="1.0.7",
    author="Nguyen Thuc Huynh",
    author_email="huynhnt6995@gmail.com",
    description="Logging with logstash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fiop/hcc/camera-system/log-util",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ['python-dotenv', 'python3-logstash']
)