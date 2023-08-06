def say(text):
    import pyttsx3 as pt
    a = pt.init()
    a.setProperty('rate', 150)
    a.say(text)
    a.runAndWait()


