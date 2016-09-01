ToMC
====

Tools of Mass Creation

NOTE: Currently server functionality achieved only on Linux.

The server must have the ports 8098, 8099 and 9001 open to be able to host a
game.

You may need to make the server scripts found in the Extra_python_modules executable by doing 'chmod a+x HTTPServerstuff.py'

Tools of Mass Creation is a game on the Blender game engine. Reshape the forms you create. Build worlds with these forms. Connect the worlds.

The networking should work on your machine out of the box.
If you wish to test it with a friend, head inside the .blend into the GlobalDictIni.py text file and change the variable gD['ServerIP'] to the host machine IP address.

Create a server through the menu presented at game start. 

Create cubes by pressing U
Save the world by pressing J
Load the world by pressing L 

Currently only presence of the correct objects works properly, they still need
to be moved to their respective locations and load the correct mesh 
deformations.

The cubes should be modifiable by moving your mouse over them

Launch another instance of the game and press "join" to connect to the server.


Use WASD and the spacebar to move around with your cube.
