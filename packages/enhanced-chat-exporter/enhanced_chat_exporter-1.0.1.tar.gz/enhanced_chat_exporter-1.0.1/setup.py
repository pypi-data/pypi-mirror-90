from setuptools import setup, find_packages

with open("README.rst") as fh:
    long_description = fh.read()

setup(
    name="enhanced_chat_exporter",
    version="1.0.1",
    author="chicc",
    description="A enhanced Discord chat exporter for Python Discord bots based on mahtoid's chat_exporter.",
    long_description=long_description,
    url="https://github.com/ChickenDevs/EnhancedDiscordChatExporterPy",
    packages=find_packages(),
    package_data={'': [r'chat_exporter/chat_exporter_html/*.html']},
    include_package_data=True,
    license="GPL",
    install_requires=["discord", "requests", "pytz", "grapheme", "emoji", "Pillow"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords="chat exporter",
)
