import setuptools

setuptools.setup(
    name="router-status",
    version='1.0.0.b2',
    author="Steve Beaumont",
    author_email="steve.b@hi2.me.uk",
    description="A utility to extract status information from domestic Broadband routers "
                "such as WAN IP address, downstream rate, uptime, noise margin and the like.",
    url="https://gitlab.com/hi2meuk/router-status",
    packages=['router_status', 'router_status/models'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.8',
)
