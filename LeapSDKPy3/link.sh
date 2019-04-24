sudo ln -s /usr/local/Cellar/python/3.7.3/Frameworks/Python.framework/Versions/3.7 /Library/Frameworks/Python.framework/Versions/3.7

clang++ -arch x86_64 -I /Library/Frameworks/Python.framework/Versions/3.7/include/python3.7m LeapPython.cpp libLeap.dylib /Library/Frameworks/Python.framework/Versions/3.7/lib/libpython3.7.dylib -shared -o LeapPython.so
