import speech_recognition as sr

recognizer = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic,duration=0.2)
            print("Speak Anything :")
            audio = recognizer.listen(mic)
        
            text = recognizer.recognize_google(audio)
            
            if "left" in text:
                print("You said : {}".format(text))
                print("action: turning left")
            elif "right" in text:
                print("You said : {}".format(text))
                print("action: turning right")
            elif "brake" in text:
                print("You said : {}".format(text))
                print("action: stopping")
            elif "go" in text:
                print("You said : {}".format(text))
                print("action: go")
            elif "accelerate" in text:
                print("action: accerelating")
            else:
                print("You said : {}".format(text))

    except:
            print("Sorry could not recognize what you said")
            recognizer = sr.Recognizer()
            continue
    