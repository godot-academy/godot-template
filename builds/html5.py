import runpy
import os
import subprocess

#Python script to create a simple HTPP server to serve your game
#This should be executed from it's parent folder, otherwise it won't work

#Try running it
os.chdir("./html5")
print("Attempting to run HTML5 Server...")
print("Use CTRL-C to close if the server is running...")

#Python 2
print("Try Python2")
subprocess.call("python -m SimpleHTTPServer")

#Python 3
print("Try Python3")
subprocess.call("python -m http.server")
    

print("Done...")