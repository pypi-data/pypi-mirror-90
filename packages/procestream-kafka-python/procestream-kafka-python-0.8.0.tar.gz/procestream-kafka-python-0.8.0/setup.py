import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="procestream-kafka-python", # Replace with your own username
    version="0.8.0",
    author="Nipun Balan Thekkummal",
    author_email="dev@technipun.com",
    description="Kafka stream processing microservice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nipunbalan/procstream-kafka-python",
    packages=setuptools.find_packages(exclude=("test",)),
    include_package_data=True,
    install_requires=["kafka-python", "tweepy","elasticsearch"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)