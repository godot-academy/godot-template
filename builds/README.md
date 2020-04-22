# Building

This builds directory contains a number of PowerShell scripts that can be used to build and deploy your game.
This significantly improves the process by automating both the project export and a potential itch.io upload. It utilizes itch.io's butler application to do so.

> This is currently only enabled on ***Windows***! Although, this could likely be easily ported to other build platforms.

## Installing Dependencies

### Godot
You should already have [Godot](https://godotengine.org/) installed at this point, but if not you can install the latest version that is compatible with the project. You could even install the headless/editorless version if this is going to be ran on a build-only pipeline. Make sure that the Godot application has been added to the system `PATH`.

The Godot application is used by [build.ps1](./build.ps1) to export the project.

### Butler
You can install the itch.io butler aplication via the [instructions here](https://itch.io/docs/butler/). This application can be used to automatically create patches and upload the project. You'll need to add butler to the system `PATH` as well. Butler is used by [deploy.ps1](deploy.ps1).

#### Credentials
Before you can run butler, you'll need to collect your credentials. See [Running butler from CI builds](https://itch.io/docs/butler/login.html) for specific details, but basically it follows like this:

1. Generate an API key on your game's itch.io page
    - You can also simply log into the butler application and have one generated automatically
2. Copy your API key from the user profile filepath
    - `%USERPROFILE%\\.config\\itch\\butler_creds`
3. Place this file copy into the builds directory
    - `\builds\butler_creds`

These credentials will be read by the deployment script and fed into butler.

>> TODO: Have the build script reference these credentials directly somehow?

***Make sure you never commit this file to VCS!***
In general don't share it with anyone, and don't re-use it across multiple accounts. The `butler_creds` credentials subdirectory should be already included in  `.gitignore`.

# Build and Deploy
Once credentials have been set up, you can build and upload the game with a single click (okay maybe two).
1. Right-Click on [build_and_deploy.ps1](./build_and_deploy.ps1)
2. Select `Run With Powershell`

And you're set! The game will automatically be exported and uploaded to itch.io!

> TODO: Create batch files and/or shell scripts for this

## Two-Step
In most cases it would be a good idea to manually confirm the build as a sanity check. You can simply execute the [build.ps1](./build.ps1) script in the same way to build all of the exports.

Once you've verified, you can either re-run the whole process or simply run [deploy.ps1](./deploy.ps1), which will upload the builds.

# Debugging HTML5 Builds
Also included in this builds directory is a simple Python HTTP server script. If you have either [Python 2.7 or 3.X installed](https://www.python.org/downloads/) you can run this script, which will create a simple server and host the html5 build. Make sure Python is added to your system `PATH` and you are currently in the same directory of the script!

`PS ...\builds> python .\html5.py`

Once it's running you can visit [localhost:8000](http://localhost:8000) to run the build. To close the server, you can hit Ctrl-C or Ctrl-Z in the prompt.

> You can also execute the `html5.ps1` script on Windows

# Andoird Builds
##### https://docs.godotengine.org/en/latest/getting_started/workflow/export/exporting_for_android.html

Follow the instructions in the link above for getting android builds setup. However, I will list out my steps just in case there are any issues.

## Installing Required Software

1. Install Andoid SDK
    1. https://developer.android.com/studio/
    1. Standard Installation
1. Install [OpenJDK](https://github.com/ojdkbuild/ojdkbuild)
    1. Go to the [Releases](https://github.com/ojdkbuild/ojdkbuild/releases) page
    1. I'm using 12.0.1.12
    1. For Windows I used the [.msi](https://github.com/ojdkbuild/ojdkbuild/releases/download/12.0.1-1/java-12-openjdk-12.0.1.12-1.windows.ojdkbuild.x86_64.msi)
    1. Standard Installation
1. Create Debug.keystore
    1. Only neccesary if you don't already have one
    1. `keytool -keyalg RSA -genkeypair -alias androiddebugkey -keypass android -keystore debug.keystore -storepass android -dname "CN=Android Debug,O=Android,C=US" -validity 9999`
    1. Store this securely on your device, in `~/.android`
1. Android Debug Bridge (adb)
    1. Looks like the best way to install this is to complete Android Studio installation

## Configuring the Godot Editor

1. Go to Editor->Editor Settings
1. Select the Export->Android category
1. Set the three required paths
    1. Android Debug Bridge (adb)
        - `~\AppData\Local\Android\Sdk\platform-tools\adb.exe`
        - Might be slightly different on other OS
    1. jarsigner
        - This was installed by the JDK
        - If you also used OpenJDK, it'll be installed under there
        - For example: `C:\Program Files\ojdkbuild\java-12-openjdk-12.0.1-1\bin\jarsigner.exe`
    1. The debug.keystore
        - `~\\.android\debug.keystore`

## Remote Debugging

Since I don't always want to have my device plugged into USB all the time, I can set up a wireless bridge to make debugging easier. Although for an older version, [these instructions](http://codetuto.com/2016/06/godot-engine-remote-debug-live-edit/) made it easier to do. Basically, you do the following:

1. Plug in your device like normal, run a build
1. Check that Android Debug Bridge (adb) can find your device
    1. Run the command `adb devices` to see if you are recognized
        - I had to add adb.exe to my PATH
    1. Find the IP address of your device
        - Android: `Settings->System->About phone->Status`
    1. Set adb debug port to 5555
        - `adb tcpip 5555`
    1. Disconnect your device from USB
    1. Connect adb wirelessly to your phone's IP_ADDRESS
        - `adb connect IP_ADDRESS:5555`
1. Run the debug export of your project in Godot (Icon in the top-right corner next to play)

### Recovering Connection
- Relaunching Godot will recover the connection but it takes a minute for everything to be initialized
- Rebooting the device loses the connection (and probably losing WIFI, etc)
    - You'll need to repeat the steps to reconnect
        - Connect USB -> `adb tcpip` -> `adb connect ...`
        - Maybe I'll make a quick plugin for this...
    - [Some more information](https://stackoverflow.com/questions/29514151/how-to-automatically-adb-connect-to-a-device-over-wifi)
- If you don't reboot, it usually only takes an `adb connect ...` command
