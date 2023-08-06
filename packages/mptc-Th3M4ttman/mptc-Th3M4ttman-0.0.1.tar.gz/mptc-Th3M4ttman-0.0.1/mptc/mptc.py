
from os import system, name
import os
import time
import sys

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


def tts(text, lang='en', slow=False):
	if tts_enabled and playsound_enabled:
		speech = gTTS(text=str(text), lang=lang, slow=slow)
		out = speech.save("Temp.Mp3")
		playsound("Temp.Mp3")
		os.remove("Temp.Mp3")
	else:
		if not tts_enabled:
			print("gTTS not installed")
		if not playsound_enabled:
			print("playsound not installed")



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


def re_line():
	print("\033[A \033[A")


def loading_bar(c=10, dm="Done", tick=True, pct=0, s=0.02):
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
		print(o)
		return 0
	for y in range(0, 56):
		if y != 56:
			z = z + x
	
		u = 55/100
		i = str(round(y/u))
		if y == 55 and dm != "":
			percent = ct(dm, str(c) + ";7", 9)
		else:
			percent = ct(i + "%", 7, 7)
		o = z + percent
		print(o)
		print("\033[A \033[A")
		if s == 0:
			continue
		time.sleep(s)
	print()


def load_wheel(string="Please wait ..", c=False, i=0, Anim=["|", "/", "-", "\\", "|", "/", "-", "\\"], delay=.5):
	
	i = i%len(Anim)
	if c == False:
		wheel = string+Anim[i]
	else:
		wheel = string + c
	re_line()
	print(wheel)
	
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
		loading_bar()
		print(end)
		for c in range(0,256):
			loading_bar(c,str(c),True,0,0)
			print(end)
	if demo[1]:
		for c in range(0,256):
			print(end)
			x=ct(c,c,5)
			print(x)
			print("")
			time.sleep(0.01)
			print(end)
	if demo[2]:
		for c in range(0,256):
			print(end)
			x=ct("TextTextTextTextTextText","10;"+str(c),5)
			print(x)
			print(end)
			print("font effect "+str(c))
			time.sleep(0.01)
	if demo[3]:
		for x in range(0,101):
			loading_bar(206,"complete",False,x)
			time.sleep(0.01)
			re_line()
		print()
	if demo[4]:
		for x in range(0,50):
			load_wheel("Demo wheel... ", i=x, delay=0.1, Anim=bubble, c=False)
		load_wheel("Demo wheel... ", i=x, delay=0.1, Anim=bubble, c="Complete")
	if demo[4]:
		print(get_files_in_dir("Test", [".zip"], True))
		print(get_files_in_dir("Test", [""], False))
		print(get_files_in_dir("FolderThatDoesntExist", [""], True))
	if demo[5]:
		tts("Hook into google text to speech easily")
		tts("Have her say whatever the fuck you want with a super simple function")


demovar = False
if __name__ == "__main__":
	if demovar:
		demo(lb=True, ct=True, fe=True, rl=True, lw=True, gf=True, tts=True)

