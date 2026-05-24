# Autolab Write a Python program that writes "Hello world" to
# a file (e.g., called 'content.txt'). 
# It should also print the same text to the screen.
# script der printer hello world og gemmer som txt
print("hello world")
with open("hello_world.txt", "w") as file:
    file.write("hello world")
# slut

