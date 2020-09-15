import wolframalpha
import wikipedia
import wx
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
#print (rate)                        #printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
#print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, pos=wx.DefaultPosition,size = wx.Size(450, 100),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX |
                          wx.CLIP_CHILDREN, title="PyDA")
        panel  = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
        label="Hello I am PyDA - a Python Digital Assistant . How can I help you today?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt =wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt ,0, wx.ALL ,5)
        panel.SetSizer(my_sizer)
        self.Show()
        engine.say("Hello I am Pyda, a Python Digital Assistant . How can I help you today?")
        engine.runAndWait()

    def OnEnter (self, event):
        ipt = self.txt.GetValue()
        ipt = ipt.lower()
        if ipt=="":
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
            try:
                self.txt.SetValue(r.recognize_google(audio))
            except sr.UnknownValueError:
                engine.say("Sorry, I could not hear you correctly. Please say it again?")
                engine.runAndWait()
            except sr.RequestError:
                engine.say("The text engine could not request results. The service may be temporarily down. please try later.")
                engine.runAndWait()
        else:        
            try:
                app_id = "TA94X9-T9QJEGVV55"
                client = wolframalpha.Client(app_id)

                res = client.query(ipt)
                answer = next(res.results).text

                print (answer)
                engine.say("Your answer is" + answer)
                engine.runAndWait()
                
            except:
                wikipedia.set_lang("en")
                engine.say("Searching Wikipedia now for" + ipt)
                engine.runAndWait()
                try:
                    answer = wikipedia.summary(ipt, sentences = 2)
                    print (answer)
                    engine.say(answer+ "Does this sound good?")
                    engine.runAndWait()
                except:
                    engine.say("Sorry, I couldn't really find anything related to your search for " + ipt + ". Would you like to try again?")
                    engine.runAndWait()

if __name__=="__main__":
    app =wx.App(True)
    frame =MyFrame()
    app.MainLoop()


engine.stop()
