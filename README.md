# GesTerm - Gestural macros for a better command line experience

## Files / table of contents for the project

- `imports.py`: Basic file importing some barebones libraries required. Not used in final implementation.
- `gesterm.py`: Final iteration of the project. Contains all the logic and code necessary for gesture detection, command execution, and operating system alerts (macOS).
- `requirements.txt`: A `pip3 freeze` of my working Python 3 environment at the time of submission. Please run `python3 -m pip install -r requirements.txt` or `pip3 install -r requirements.txt` before running the system.
- `{user-training, studio-demo, implementation-demo, discrete-timewarp}.py`: These are all deprecated files that serve no purpose for the system as it is now. Refer to these as needed for my thought process during initial project stages.
- `{deploy, cleanup}.sh`: Deprecated shell scripts that aided in initializing and refreshing GesTerm every 15 seconds and cleanup once the user decides to exit. No longer necessary or functional, as `gesterm.py` now takes in arguments.

The folder `LeapSDKPy3` is *crucial* to running the system, as GesTerm depends on the Leap Motion SDK ported over to Python 3.7.

## Running the system.

Documented in the writeup PDF as well. Run

```
{pip3 install -r requirements.txt} OR {python3 -m pip install -r requirements.txt}
python3 gesterm.py swipe ‘cmd1’ circle ‘cmd2’
```

to get started with GesTerm. Provide your own commands for `cmd1` and `cmd2`.


## Building a `python3` wrapper around LeapSDK on macOS Mojave

Note that this is for a Python 3.7 wrapper around LeapSDK, which natively supports Python 2. *Note that this assumes an already installed Python 3.7, preferably one that has been installed through* `brew`. *You should also have System Integrity Protection (SIP) disabled!*

To do so:
1. Find `swig-rel-2.0.9.zip` inside the `dependencies` folder and extract it.
2. Compile and build the extracted contents from source and run `sudo make install`. Verify the version with `swig -version`.
3. Copy `Leap.h`, `LeapMath.h`, `Leap.i`, and `libLeap.dylib` into one folder.
4. Run `link.sh` in the same folder from Step 4. `link.sh` can be found in the `LeapSDKPy3` folder. This shell script creates aliases for Python based on your macOS installation.

## Building a GRT wrapper from C++ to `python3`

The Gesture Recognition Toolkit (GRT) is written and is based in C++. To get an integrative environment that will run with the Leap Motion SDK, we need to wrap it around Python 3.7. I based my own installation around [this tutorial](http://www.morethantechnical.com/2018/08/09/take-a-swig-out-of-the-gesture-recognition-toolkit-grt/). You'll note that the author still has an outstanding pull request on his Github repo for his `python3`-wrapped GRT.
 
To do so:
1. Download the GRT repo and checkout the pull request from the article above. Google/StackOverflow will show you how to download PRs onto a repo.
2. Run `sudo rm -rf /usr/local/share/swig` to completely purge `swig 2.0.9` (we need `swig 3.0` to build the GRT wrapper).
3. `brew install swig` to get `swig v3`.
4. Make and install the GRT wrapper from source, similar to what was done with LeapSDK:
```
cd dependencies/grt/build/
mkdir tmp && cd tmp
make -j
cd python
python3 hello_world_example.py ../../../data/IrisData.grt
```

## Test success

To see that the packages did indeed work, launch an instance of `python3` and try `import Leap; import GRtT`. Congrats!
