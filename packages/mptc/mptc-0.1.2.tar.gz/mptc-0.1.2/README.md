# mptc

Matt's Python Tool Chain

Functions:

tts(text, lang, slow, p, warnings) uses GTTS to create and play google text to speech in 1 line)
text: The text to say
lang: The language passed to gTTS
slow: When true it slows the speech down
p: Should it print the line also
warnings: if gTTS/playsound are not installed should it print a warning


ct(text,color,fe=5,p=False) colour text
text: The text you want to colour
colour: The colour (ansi code, eg: 1 = red 2 = green)
fe: font effect (ansi code)
p: should the function print the text


clear() clear output on all OS


loading_bar(c=10, dm="Done", tick=True, pct=0, s=1, p=False) coloured loading bar
c: colour
dm: Done Message
tick: whether to assign progress to a loop that ticks on a delay set by s
pct: the percentage of the bar you wish to create if not using tick
s: the delay of tick
p: should the function print the loading bar or not


load_wheel(string="Please wait ..", c=None, i=0, Anim, delay=.5, cm=False): loading widget
string:String to preceed the widget
c: ansi colour
i: which character of the animation to display
Anim: a list of characters that when played in sequence form an animation 
delay: built in delay in seconds
cm: string for after the widget


Premade Anims: spin, bubble, arrow

demo() demos the module

Classes:

Colour(r,g,b,a)
r: red
g: green
b: blue
a: alpha

Example:

purple = mptc.Colour(90,0,90,255)

print(purple.r)
or
print(purple.red)
both output 90

print(purple.g)
outputs 0
print(purple.b)
outputs 90

print(purple.a)
outputs 255

print(purple.combined)
outputs [90,0,90,255]

