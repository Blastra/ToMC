WoMC
====

Weapons of Mass Creation

NOTE: Currently server functionality achieved only on Linux.

You may need to make the server scripts found in the Extra_python_modules executable by doing 'chmod a+x HTTPServerstuff.py'

A game on the Blender game engine. Reshape the forms you can create. Build worlds with these forms. Connect the worlds.

Networking layer is functional, not complete. To make it work on your system, change the server IP and target IP in the
text file GlobalDictIni.py inside the .blend file.

If you wish to test it with a friend, head to HTTPFastread.py  and change line 11 to match the IP of the machine that
is hosting the game.

Create a server by pressing S
Activate the HTTP components of the server by pressing U

Create cubes by pressing I
Save the world data (needs to be done before accepting an incoming connection) by pressing J

In a new game window, activate client mode by mouseover-clicking the green text, entering some text and pressing
the enter key. Sometimes enter needs to be pressed down for a while :D

Load the world data you have downloaded onto the scene by pressing L

Use WASD to move around with your cube.
