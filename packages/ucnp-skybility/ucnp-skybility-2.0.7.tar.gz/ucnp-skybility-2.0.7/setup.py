import setuptools

long_description = ""
with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(
    name="ucnp-skybility",
    version="2.0.7",
    author="skybility ha team",
    url="https://gitlab.skybilityha.com/experiments/ucnp",
    author_email="support@skybilityha.com",
    description="this is a client to ucnp server for linux platform only",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "pyperclip==1.8.0",
        "python-engineio==3.13.2",
        "python-socketio==4.6.0",
        "requests==2.24.0",
        "wxPython>=4.0.3",
        "pypubsub==4.0.3",
        "pinyin==0.4.0",
        "psutil==5.5.0"
        ],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        ],
    python_requires=">=3.5",
    scripts=['client/ucnp_start']
    )
