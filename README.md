# Hide-ASCII-in-.bmp

A short python script that manipulates pixel data to hide a message written in 7-bit ASCII in a .bmp image file. Does this by modifying the least significant bit of all three colors of each individual pixel. When the LSB of each color is each pixel is read in a sequence, the result will be binary data of ASCII text.

After running, select one of 3 modes, encode a single line that you type, read from a .txt file, or decode.

Next it asks you for the image file (encoding can be any image file that PIL can open, decoding has to be a .bmp, prefereably one this program created). Filename to be typed as a string with quotes"".
I recommend using a file in the same folder as the .py file, I could not get it to work when entering a filepath to another location.

If encoding, it prompts you to enter the message (option 1), again must be entered as a string. If selecting a .txt file, again, use one in the same folder as the python file, and enter it as a string.

If decoding, it only needs the image file.

It will produce either a .bmp file titled "encoded.bmp", or a .txt file titled "hidden_message_revealed.txt".

TODO
use tkinter to implement both a gui and open the file explorer to select files
maybe expand it to use a larger bit character encoding to allow more symbols
