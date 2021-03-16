#!/bin/sh
#installs the dependencies NewSlides requires, like kivy. Assumes python3 is present on system
sudo apt update
sudo apt install pkg-config libgl1-mesa-dev libgles2-mesa-dev \ libgstreamer1.0-dev \ gstreamer1.0-plugins-{bad,base,good,ugly} \ gstreamer1.0-{omx,alsa} libmtdev-dev \ xclip xsel libjpeg-dev
sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
python3 -m pip install kivy[base] kivy_examples
python3 pip install fpdf
echo "Dependencies installed"

#Creates desktop shortcut
#!/bin/bash
printf "\nName=NewSlides\nIcon=/home/"$USER"/NewSlides-main/NewSlides/images/newSlidesIcon.png\nExec=/usr/bin/python3 /home/"$USER"/NewSlides-main/NewSlides/NewSlides.py\nType=Application\nEncoding=UTF-8\nVersion=1.0\nTerminal=false\nCategories=Office;" >> newSlides.desktop

#moves files to the home directory and provides an icon
mv ~/Downloads/NewSlides-main/newslides.desktop ~/.local/share/applications
mv ~/Downloads/NewSlides-main ~/
echo "Operation successful! Thank you for installing New Slides!" 
