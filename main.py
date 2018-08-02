from PIL import Image, ImageFilter

"""Right now this code works in encoding messages using all three colors per pixel, but it does not handle
new lines very well, I also want to explore how to import the message from an external .txt file"""


#pixel manipulation?


#in each row, there are 6 pixels whose least significant bit of their r,g,b values will
# correlate to the bit combination of an ascii char
#it will be the first pixel in the row (index[0]) followed by the pixel 10 over (index[10]) and so on, the last
#pixel at (index[50]) only the r value is used



#for every row in image, extract a single 7 bit ascii character
#for every pixel in the row, check the least significant bit of a single color in this order, [r,g,b,r,g,b,r,...]
#use these least significant bits to make a single 7 bit char, and it makes a string
def encodeMessage(image_filename, hidden_message ):
    img = Image.open( image_filename )
    print(img.format, img.size, img.mode)
    img.show()

    #img[0] is column
    #img[1] is row

    # check if there are enough pixels in the image to store the message (each char is 7 bits, and we need the null termination)
    #we use the LSB of all three colors for each pixel

    if 3 * img.size[0] * img.size[1] >= 7 * (len(hidden_message) + 1):
        pixel_map = img.load()

        #converts the message into a lengthy string consisting of only the binary equivalent
        binary_string = ""
        for i in range(len(hidden_message)):
            binary_string += bin(ord(hidden_message[i]))[2:]
        #be sure to add the null termination char
        binary_string += '0000000'
        print binary_string


        k = 0 # k is to keep track of position in the message

        print type(ord(binary_string[0]))
        print ord(binary_string[0])


        #for every row, go through each pixel, and cycle through each color in order R, G, B. Modify the least significant
        #bit to hold the binary data of the hidden message
        for j in range(img.size[1]):
            for i in range(img.size[0]):
                for p in range(3):

                    if k < len(binary_string):
                        if p == 0:
                            specific_bit = (ord(binary_string[k]) & int('0000001', 2)) | (pixel_map[i,j][0] - pixel_map[i,j][0] % 2)
                            pixel_map[i,j] = (specific_bit, pixel_map[i, j][1], pixel_map[i,j][2])
                            pixelColor = 'g'
                        elif p == 1:
                            specific_bit = (ord(binary_string[k]) & int('0000001', 2)) | (pixel_map[i,j][1] - pixel_map[i,j][1] % 2)
                            pixel_map[i,j] = (pixel_map[i, j][0], specific_bit, pixel_map[i, j][2])
                            pixelColor = 'b'
                        elif p == 2:
                            specific_bit = (ord(binary_string[k]) & int('0000001', 2)) | (pixel_map[i,j][2] - pixel_map[i,j][2] % 2)
                            pixel_map[i,j] = (pixel_map[i, j][0], pixel_map[i,j][1], specific_bit)
                            pixelColor = 'r'
                        k += 1


        img.show()
        img.save('encoded.bmp')
        img.close()
    else:
        print "image is too small to contain the message"


def decodeMessage( image_filename ):
    img = Image.open( image_filename )
    print(img.format, img.size, img.mode)
    img.show()

    # extracting the hidden message
    if img.size[0] * img.size[1] >= 5:  #needs to be at least 2 chr worth of bitys available, 14/3=4.66 so need at leaft 5 pixels total


        #cycle through every pixel in every row, extracting the LSB of each pixel in this order R, G, B
        #from there, once we have 7 bits extracted, check to see if that chr is the NULL termination
        #if not, decode into a normal chr and add to a string


        revealed_message = ''
        specific_bit = 0
        bit_count = 0
        time_to_break = False
        pixel_map = img.load()




        for j in range(img.size[1]):
            if time_to_break != True:
                for i in range(img.size[0]):
                    if time_to_break != True:
                        for k in range(3):
                            specific_bit = specific_bit << 1
                            bit_count += 1
                            if k == 0:
                                specific_bit += int('0000001', 2) & (pixel_map[i, j][0])
                                pixel_color = 'g'
                            elif k == 1:
                                specific_bit += int('0000001', 2) & (pixel_map[i, j][1])
                                pixel_color = 'b'
                            elif k == 2:
                                specific_bit += int('0000001', 2) & (pixel_map[i, j][2])
                                pixel_color = 'r'
                            if bit_count == 7:
                                if specific_bit == int('0000000', 2):#if the most recently extracted chr is the null termination
                                    print "Should break here"
                                    print revealed_message
                                    time_to_break = True
                                    break
                                else:
                                    print "Extracted a 7bit chr?"
                                    print specific_bit
                                    print chr(specific_bit)
                                    revealed_message += chr(specific_bit)
                                    specific_bit = 0
                                    bit_count = 0
                                    continue
                    else:
                        break
            else:
                break

        #it's actually only checking one color per pixel in the RGB rotation, oh well

    img.close()



#main function
selection = input("Enter 1 to encode, 2 to decode (decoding must be an .bmp that this program made) ")

if selection == 1:
    filename = input("Enter the filepath for the image you wish to encode a message into (result will be saved as a .bmp file): ")
    message = input("Enter the message you wish to encode in the image (needs to be fewer characters than the image height in pixels ")
    encodeMessage(filename, message)
elif selection == 2:
    filename = input("Enter the filepath of the image that has a coded message in it (must be a .bmp file)")
    decodeMessage(filename)
