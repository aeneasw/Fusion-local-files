# What it does
This Add-In for Fusion 360 adds two Buttons to the Menu bar:
![Preview](https://github.com/aeneasw/Fusion-local-files/blob/main/Preview.png?raw=true)

# The Buttons
- The left Button gives direct access to your local Filesystem to open files without the need of clicking "File -> Open -> Open from my PC".
- The right Button saves files locally. If you opened a file from your local hard drive the Add-In will remember the location of each opened file and when you hit this Button it will give you the option to overwrite the original file or save it with a new Name.

# What for?
This is for Users who do not want to use the cloud as there is a file limit for 10 editable files in personal license.

# How to install
- clone this repo and save it to:
  - Windows: %appdata%\Autodesk\Autodesk Fusion\API\AddIns.
  - Mac: ~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns

  It should look like this:
  ![Preview](https://github.com/aeneasw/Fusion-local-files/blob/main/fileExample.png?raw=true)

- in Fusion go to "Add-Ins" -> "Scripts and Add-Ins" -> Modules -> look In the list for the Add-in, it is called "Save". Select it, then select "Run on startup" and restart Fusion.

  It should look like this:
  ![Preview](https://github.com/aeneasw/Fusion-local-files/blob/main/fusionExample.png?raw=true)

