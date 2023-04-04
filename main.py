from pcemulator import Folder, FileSystem, Pc, Terminal
import pygame
from pygame import display, font
import jsonpickle

WHITE = (255,255,255)
BLACK = (0,0,0)


try:
    save =open("SaveData.json","r")
    encodedDict = save.read()
    decodedDict =jsonpickle.decode(encodedDict)
    pc =decodedDict["pc"]
except:
    pc=Pc.defaultPc()

terminal = pc.addTerminal()

pygame.init()
screen =display.set_mode((1080,720))
font = pygame.font.Font('freesansbold.ttf', 16)
yVal =0

CommandLines=[]
inputText=''

while True:
    screen.fill(BLACK)
    
    yVal=0
    #Past Inputs
    for pastClText in CommandLines:
        displayText=pastClText
        text =font.render(displayText,True,WHITE)
        textRect=text.get_rect()
        textRect.topleft=(0,yVal)
        screen.blit(text,textRect)

        textRect.topleft=(0,yVal)
        yVal+=16
    #Current Input
    displayText=terminal.cwd.name + ">" +inputText
    text =font.render(displayText,True,WHITE)
    textRect =text.get_rect()
    textRect.topleft=(0,yVal)
    screen.blit(text,textRect)
    display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if pygame.K_RETURN == event.key:
                CommandLines.append(displayText)
                result=terminal.parseCommand(inputText)
                if result!=None:
                    CommandLines.append(result)
                inputText=""

            elif pygame.K_BACKSPACE == event.key:#TODO maybe an issue with windows?
                inputText = inputText[0:-1]

            else:
                inputText +=event.dict["unicode"]

        if event.type == pygame.QUIT:
            save = open("SaveData.json","w")
            decodedDict={"pc":pc}
            encodedDict=jsonpickle.encode(decodedDict)
            save.write(encodedDict)
            save.close()
            pygame.quit()
            quit()
