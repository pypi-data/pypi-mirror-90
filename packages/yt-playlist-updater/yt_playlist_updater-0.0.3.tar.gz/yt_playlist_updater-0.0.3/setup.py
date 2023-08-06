import setuptools

setuptools.setup(
    name="yt_playlist_updater",
    version="0.0.3",
    author="Mukul GUpta",
    author_email="blablamukul@gmail.com",
    description="Youtube playlist updater using voice recognition",
    url="https://github.com/blablamukul/yt-playlist-updater",
    py_modules = ["yt_playlist_updater"],
    package_dir={'':'src'},
    packages=setuptools.find_packages(),
    install_requires=["SpeechRecognition","pyttsx3","google-api-python-client","google-auth-oauthlib","google-auth-httplib2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    include_package_data=True,
    package_data={'':["*json"]}
)
