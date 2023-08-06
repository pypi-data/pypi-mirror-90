
from os import system, name
import os
import time
import sys

os.system("color")

end = "\033[0m"
bubble = ["•", "°", "o", "0", "O", "@"]
spin = ["|", "/", "-", "\\", "|", "/", "-", "\\"]
arrow = [">==", "=>=", "==>", "==="]


try:
	from gtts import gTTS
	tts_enabled = True
except:
	tts_enabled = False

try:
	from playsound import playsound
	playsound_enabled = True
except:
	playsound_enabled = False

try:
	import gi
	gi_enabled = True
except:
	gi_enabled = False
	playsound_enabled = False


def tts(text, lang='en', slow=False, p=False, warnings=True):
        if tts_enabled and playsound_enabled:
                speech = gTTS(text=str(text), lang=lang, slow=slow)
                out = speech.save("Temp.Mp3")
                playsound("Temp.Mp3")
                os.remove("Temp.Mp3")
        else:
                if not tts_enabled:
                        if warnings: print("gTTS not installed")
                if not playsound_enabled:
                        if warnings: print("playsound not installed")
                if not gi_enabled:
                        if warnings: print("gi not found")



class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class Colour:
        red = 255
        r = red
        green = 255
        g = green
        blue = 255
        b = blue
        alpha = 255
        a = alpha
        combined = [r,g,b,a]
        c = combined

        def __init__(self, r, g, b, a):
                self.red = r
                self.r = self.red
                self.green = g
                self.g = self.green
                self.blue = b
                self.b = self.blue
                self.alpha = a
                self.a = self.alpha
                self.combined = [r,g,b,a]
                self.c = self.combined
                


def ct(text, color, fe=5, p=False):
	start = "\033["
	end = "\033[0m"
	start = start + "38;" + str(fe) + ";" + str(color)

	text = start + "m" + str(text) + end

	if p: print(text)
	return text


def clear(): 

	if name == 'nt':

		_ = system('cls')

	else:

		_ = system('clear')


def loading_bar(c=10, dm="Done", tick=True, pct=0, s=1, p=False):

	x = ct(" ", str(c) + ";7", 5)
	z = ""
	if tick != True:
		for k in range(0, int((55/100) * pct)):
			z = z + x
		if pct == 100:
			percent = ct(dm, str(c) + ";7", 9)
		else:
			percent = ct(str(pct) + "%", 7, 7)
		o = z + percent
		if p: print(o)
		return o
	for y in range(0, 56):
		if y != 56:
			z = z + x
	
		u = 55/100
		i = str(round(y/u))
		if y == 55 and dm != "":
			percent = ct(dm, str(c) + ";7", 9)
		else:
			percent = ct(i + "%", 7, 7)
		o = z + percent + end
		print("\r" + o, end="")
		sys.stdout.flush()
		if s == 0:
			continue
		time.sleep(s)
	return o



def load_wheel(string="Please wait ..", i=0, c=None, Anim=["|", "/", "-", "\\", "|", "/", "-", "\\"], delay=.5, cm=False):
	
	i = i%len(Anim)
	wheel = string+Anim[i]
	if c != None:
		wheel = ct(wheel, c)
	if cm != False:
		wheel = wheel + cm
	print("\r" + wheel, end="")

	time.sleep(delay)


def get_files_in_dir(d="Input", filetypes=[], only=False):

	if os.path.exists(d):
		if only == False:
			pics = []
			vids = []
			others = []
			for file in os.listdir(d):
				if file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".jpg"):
					pic = (os.path.join(d, file))
					pics.append(pic)
				elif file.endswith(".gif"):
					vid = (os.path.join(d, file))
					vids.append(vid)
				else:
					other = (os.path.join(d, file))
					others.append(other)

		else:
			files = []
			for file in os.listdir(d):
				for ft in filetypes:
					if file.endswith(ft):
						cf = (os.path.join(d, file))
						files.append(cf)
		if only == False:
			out = {"Pics": pics, "Vids": vids, "Others": others}
		else:
			out = {"Files": files}

	else:
		out = None
	return out


def demo(**kwargs):
	demo = [False, False, False, False, False, False, False]
	for key, value in kwargs.items():
		if key in ["lb","LB","loading_bar"] and value:
			demo[0]=True
		if key in ["ct","CT","colour_text"] and value:
			demo[1]=True
		if key in ["fe", "FE", "font_effects"] and value:
			demo[2] = True
		if key in ["rl", "RL", "re_line"] and value:
			demo[3] = True
		if key in ["lw", "LW", "load_wheel"] and value:
			demo[4] = True
		if key in ["gf", "GF", "get_files_in_dir"] and value:
			demo[5] = True
		if key in ["tts", "TTS"] and value:
			demo[6] = True

	if demo[0]:
		loading_bar(1,1,False,50)
		for c in range(0,254):
			loading_bar(c,str(c),True,0,0)
		print(loading_bar(255, str(255), True, 0,0))
	if demo[1]:
		for c in range(0,256):
			x=ct(c,c,5)
			print("\r"+x,end="")
			time.sleep(0.01)
		print(ct(255,255,5))
	if demo[2]:
		for c in range(0,256):
			x=ct("TextTextTextTextTextText","10;"+str(c),5)
			print("\r"+x+" Font effect "+str(c), end="")
			time.sleep(0.01)
		print(x + " Font effect " + str(c))
	if demo[3]:
		for x in range(0,100):
			print("\r" + str(loading_bar(2,"complete",False,x)),end="")
			time.sleep(0.01)
		print(loading_bar(2, "complete", False, 100))
	if demo[4]:
		for x in range(0,50):
			load_wheel("Demo wheel... ", i=x, delay=0.1, Anim=bubble, c=2)
		load_wheel("Demo wheel... ", i=50, delay=0.1, Anim=bubble, c=2, cm=" Complete")
		print()
	if demo[4]:
		print(get_files_in_dir("Test", [".zip"], True))
		print(get_files_in_dir("Test", [""], False))
		print(get_files_in_dir("FolderThatDoesntExist", [""], True))
	if demo[5]:
		line1="Hook into google text to speech easily"
		line2="Have her say whatever the fuck you want with a super simple function"
		print(line1)
		tts(line1)
		print(line2)
		tts(line2)



demovar = False
if __name__ == "__main__":
	if demovar:
		demo(lb=True, ct=True, fe=True, rl=True, lw=True, gf=True, tts=True)


