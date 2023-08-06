import setuptools

long_description = """
# Coldtype

### Programmatic display typography

More info available at: [coldtype.goodhertz.com](https://coldtype.goodhertz.com)
"""

setuptools.setup(
    name="coldtype",
    version="0.1.5",
    author="Rob Stenson / Goodhertz",
    author_email="rob@goodhertz.com",
    description="Functions for manual vectorized typesetting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/goodhertz/coldtype",
    #package_dir={"": "coldtype"},
    packages=[
        "coldtype",
        "coldtype.animation",
        "coldtype.animation.nle",
        "coldtype.color",
        "coldtype.midi",
        "coldtype.pens",
        "coldtype.renderer",
        "coldtype.text",
        "coldtype.fontgoggles",
        "coldtype.fontgoggles.compile",
        "coldtype.fontgoggles.font",
        "coldtype.fontgoggles.misc",
    ],
    entry_points={
        'console_scripts': [
            'coldtype = coldtype.renderer:main'
        ],
    },
    install_requires=[
        "fontPens",
        "defcon",
        "mido",
        "skia-pathops",
        "skia-python>=86.0",
        "easing-functions",
        "fonttools[woff,unicode,type1,lxml,ufo]",
        "freetype-py",
        "uharfbuzz>=0.12.0",
        "python-bidi",
        "ufo2ft",
        "unicodedata2",
        "numpy",
        "watchdog<=0.10.3", # https://github.com/gorakhargosh/watchdog/issues/702
        "noise",
        "PyOpenGL",
        "PyOpenGL-accelerate",
        "glfw",
        "SimpleWebSocketServer",
        "more-itertools",
        "docutils",
        "exdown",
        "srt",
        "timecode",
        #"rtmidi",
        #"pynput",
        #"pyaudio",
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
