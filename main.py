from PIL import Image, ImageFilter

"""Right now this code works in encoding messages using all three colors per pixel, but it does not handle
new lines very well, I also want to explore how to import the message from an external .txt file"""


#pixel manipulation?


#in each row, there are 6 pixels whose least significant bit of their r,g,b values will
# correlate to the bit combination of an ascii char


def encodeMessage(image_filename, hidden_message ):
    img = Image.open( image_filename )
    print hidden_message
    #img[0] is column
    #img[1] is row

    # check if there are enough pixels in the image to store the message (each char is 7 bits, and we need the null termination)
    #we use the LSB of all three colors for each pixel

    if 3 * img.size[0] * img.size[1] >= 7 * (len(hidden_message) + 1):
        pixel_map = img.load()

        #converts the message into a lengthy string consisting of only the binary equivalent
        binary_string = ""
        for i in range(len(hidden_message)):
            bin_to_add = bin(ord(hidden_message[i]))[2:]
            while len(bin_to_add) < 7: #some characters reduce to fewer than 7 bits, this throws off the encoding
                bin_to_add = '0' + bin_to_add
            binary_string += bin_to_add
        #be sure to add the null termination char
        binary_string += '0000000'


        k = 0 # k is to keep track of position in the message



        #for every row, go through each pixel, and cycle through each color in order R, G, B. Modify the least significant
        #bit to hold the binary data of the hidden message
        for j in range(img.size[1]):
            for i in range(img.size[0]):
                for p in range(3):

                    if k < len(binary_string):
                        if p == 0:
                            specific_bit = (ord(binary_string[k]) & int('0000001', 2)) | (pixel_map[i,j][0] - pixel_map[i,j][0] % 2)
                            pixel_map[i,j] = (specific_bit, pixel_map[i, j][1], pixel_map[i,j][2])
                        elif p == 1:
                            specific_bit = (ord(binary_string[k]) & int('0000001', 2)) | (pixel_map[i,j][1] - pixel_map[i,j][1] % 2)
                            pixel_map[i,j] = (pixel_map[i, j][0], specific_bit, pixel_map[i, j][2])
                        elif p == 2:
                            specific_bit = (ord(binary_string[k]) & int('0000001', 2)) | (pixel_map[i,j][2] - pixel_map[i,j][2] % 2)
                            pixel_map[i,j] = (pixel_map[i, j][0], pixel_map[i,j][1], specific_bit)
                        k += 1


        img.save('encoded.bmp')
        img.close()
    else:
        print "image is too small to contain the message"


def decodeMessage( image_filename ):
    img = Image.open( image_filename )

    # extracting the hidden message
    if img.size[0] * img.size[1] >= 5:  #needs to be at least 2 chr worth of bitys available, 14/3=4.66 so need at leaft 5 pixels total


        #cycle through every pixel in every row, extracting the LSB of each pixel in this order R, G, B
        #from there, once we have 7 bits extracted, check to see if that chr is the NULL termination
        #if not, decode into a normal chr and add to a string


        revealed_line = ''
        specific_bit = 0
        bit_count = 0
        time_to_break = False
        pixel_map = img.load()


        output_file = open("hidden_message_revealed.txt", 'w')

        for j in range(img.size[1]):
            if time_to_break != True:
                for i in range(img.size[0]):
                    if time_to_break != True:
                        for k in range(3):
                            specific_bit = specific_bit << 1
                            bit_count += 1
                            if k == 0:
                                specific_bit += int('0000001', 2) & (pixel_map[i, j][0])
                            elif k == 1:
                                specific_bit += int('0000001', 2) & (pixel_map[i, j][1])
                            elif k == 2:
                                specific_bit += int('0000001', 2) & (pixel_map[i, j][2])
                            if bit_count == 7:
                                if specific_bit == int('0000000', 2):#if the most recently extracted chr is the null termination
                                    output_file.write(revealed_line)
                                    time_to_break = True
                                    break
                                elif specific_bit == int('0001010', 2): #if the extracted char is the command LF, newline
                                    print revealed_line
                                    output_file.write(revealed_line + '\n')
                                    revealed_line = ''
                                    specific_bit = 0
                                    bit_count = 0
                                else:
                                    print chr(specific_bit)
                                    revealed_line += chr(specific_bit)
                                    specific_bit = 0
                                    bit_count = 0
                                    continue
                    else:
                        break
            else:
                break

    img.close()
    output_file.close()



#main function
print "Enter 1 to encode a single line message into the image (type it yourself now, don't copy/paste any EOL)"
print "Enter 2 to encode a .txt file into the image (must be only 7 bit ascii, otherwise unexpected behavior)"
print "Enter 3 to decode (decoding must be an .bmp that this program made)"
selection = input("Selection: ")

if selection == 1:
    filename = input("Enter the filepath of the image to encode a message into (result will be saved as a .bmp file): ")
    message = input("Enter the message you wish to encode in the image:")
    encodeMessage(filename, message)
elif selection == 2:
    filename = input("Enter the filepath of the image to encode a message into (result will be saved as a .bmp file): ")
    text_doc = input("Enter the filepath of the .txt file")
    with open(text_doc, 'r') as my_file:
        message = my_file.read().replace('\n', chr(int('0001010', 2)))
    my_file.close()
    encodeMessage(filename, message)


elif selection == 3:
    filename = input("Enter the filepath of the image that has a coded message in it (must be a .bmp file)")
    decodeMessage(filename)
