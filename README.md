# Hide-ASCII-in-.bmp

*DISCLAIMER* This is producing unexpected results when decoding a message that has a space. I swear I had this working last week.


A short python script that manipulates pixel data to hide a message written in 7-bit ASCII in a .bmp image file

After running, select encode or decode by typing in 1 or 2 respectively.

Next it asks you for the image file (encoding can be any image file that PIL can open). Has to be typed as a string.
I recommend using a file in the same folder as the .py file, I could not get it to work when entering a filepath.

Third, type out the message you want encoded. Right now only works with basic ASCII with no endline characters.
