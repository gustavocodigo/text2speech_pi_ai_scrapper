# text2speech_pi_ai_scrapper
This is a python project that converts text to AI speech !

this is a example of generated audio file:<br>

https://github.com/gustavocodigo/text2speech_pi_ai_scrapper/blob/main/audio-2023-08-29-19-00-46-file.mp3


# Install:

```
git clone https://github.com/gustavocodigo/text2speech_pi_ai_scrapper
cd text2speech_pi_ai_scrapper
pip install -r requirements.txt
```





download chrome selenium drivers at:

https://chromedriver.chromium.org/downloads


**Make sure to choose the version of your installed google chrome**
you can check the version typing the command:

For **linux**:
```
google-chrome --version
```

For **windows** check on google chrome manually.

**after getting the driver paste it in a folder called driver:**

![image](https://github.com/gustavocodigo/text2speech_pi_ai_scrapper/assets/108258194/ca2d856b-a448-47b1-aff9-cee761e495b0)




![image](https://github.com/gustavocodigo/text2speech_pi_ai_scrapper/assets/108258194/0400cb6e-06b0-40f8-be72-aba8dcf1c341)

 for windows users replace these lines:
 to the current drive path:

![image](https://github.com/gustavocodigo/text2speech_pi_ai_scrapper/assets/108258194/44d2d8ba-ba00-4267-93dc-26f831ace17b)

and maybe change the paths characters **/** to \\\


**Folders**
make sure to create an empty folder called
**audios** where the sounds will be stored.


also escape the correct folder for windows as commented before.

# Running the script 


run it with the command:

```
python3 main.py
```


The project will listen on port 5000

then open your browser and type http://localhost:5000
to access the interface:

![image](https://github.com/gustavocodigo/text2speech_pi_ai_scrapper/assets/108258194/03750e45-1891-423b-91d1-e395245d5a07)


![image](https://github.com/gustavocodigo/text2speech_pi_ai_scrapper/assets/108258194/332f74bd-ff3d-4302-88ba-a0ee9443d02a)

**you can type text then click in generate**

the audio will be displayed on the screen, that you can play directly and they are saved in the folder
```
audios
```
![image](https://github.com/gustavocodigo/text2speech_pi_ai_scrapper/assets/108258194/26be59cb-059c-4090-bb7b-c5b952d3fd26)





# Using as api

GET to 
https://localhost:5000/generate_mp3?text={text}

**OBS** the text length limit is **1000** for each text you enter.


return for sucess statusCode **200**
for error it will return **404** as status code.
In case of **Success** it will return the body:
```
{"id": "audio-2023-08-29-19-16-34-file.mp3"}
```


access the file generated:

https://localhost:5000/read_file?path={id}

status code is **200**

for error it will return status code **404**.

in case of **Sucess** it will return

a MP3 file media file as response



# Warning

This project is new so expect bugs, for bugs you should open an issue.




also you can set it to be stored in another folder.
