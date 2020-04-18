import pygame
import time
import random

pygame.init()

#color define
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,190,0)
purple = (255,0,155)
yellow = (255,255,0)
y = (0,155,155)
snakegreen = (10,200,0)
orangebrown = (255,203,12)
yellowishgreen = (195,255,0)
pink = (255,0,100)
darkpurple = (185,0,140)
darkblue= (0,0,165)
darkred=(240,0,0)
grey = (180,195,180)
lightpink = (255,99,242)
orange = (255,99,11)
yellowb = (255,230,13)
whiteyellow=(253,255,212)
brown=(240,150,73)
fieldgreen=(9,210,16)
darkgreen=(46,46,82)
tankcol=(0,0,62)
coldiff=(112,146,190)

display_h = 700
display_w = 700
blocksize = 10
barrierw = 20
mainTankx = display_w* 0.9
mainTanky = display_h *0.9

tankw = 40
tankh = 20
turrentw = 3
wheelw = 5
#groundy = 0.9 * display_h + tankh + 5

exploso = pygame.mixer.Sound("explosion2.wav")
hitoso = pygame.mixer.Sound("explosion3.wav")

# time control
clock = pygame.time.Clock()

gameExit = False
gameOver = False
paused = False

gameDisplay = pygame.display.set_mode((display_h,display_w))
pygame.display.set_caption('Bori-Tanks')

#snakeimg = pygame.image.load('snakehead.png')
#starthead = pygame.image.load('snahead.png')
#startapple = pygame.image.load('snakeappl2.jfif')
#icon = pygame.image.load('snahead22.png')
#appleimg = pygame.image.load('snakeappl2py.jpg')
#appleimg2 = pygame.image.load('ssnakeapp1py.jpg')
#pygame.display.set_icon(icon)

#font
szfont = 'small'
tinyfont = pygame.font.SysFont("comicsansms",20)
smallfont = pygame.font.SysFont("comicsansms",25)
midfont = pygame.font.SysFont("comicsansms",50)
bigfont = pygame.font.SysFont("comicsansms",85)

buttcol = black

def barrier(xloc,yranh):

    #print((xloc,yranh))
    pygame.draw.rect(gameDisplay,brown,[xloc,display_h-yranh,barrierw,yranh] )

def explosion(x,y,size=30):
    pygame.mixer.Sound.play(exploso)
    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        startexp = (x,y)

        colorfire = [yellow, orangebrown]

        mag = 1
        while mag < size:
            expptx = startexp[0]+random.randrange(-1*mag,mag)
            exppty = startexp[1] + random.randrange(-1 * mag, mag)

            pygame.draw.circle(gameDisplay,colorfire[random.randrange(0,2)],(expptx,exppty),random.randrange(2,5))
            mag+=1

            pygame.display.flip()
            clock.tick(50)

        explode = False


def  fireshell(xy,tankx,tanky,turpos,firpow,xloc,yranh,etankx,etanky):
    groundy = 0.9 * display_h + tankh + 5
    fire = True
    damage=0
    startshell = list(xy)
    #print("fired!!",xy)
    xshel = startshell[0]
    yshel = startshell[1]

    while fire:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #print(xshel,yshel)
        pygame.draw.circle(gameDisplay,green,(xshel,yshel),4)

        xshel -= (12 - turpos) * 2
        yshel += int((((xshel - xy[0])*0.015/(firpow/50))**2) - (turpos+turpos/(12-turpos)))
        #print(xshel,yshel)

        if yshel > groundy:
            # print("last:",xshel,yshel)
            hitx = int((xshel * groundy) / yshel)
            hity = int(groundy)
            if etankx + 5 > hitx > etankx - 5:
                print('hit critic')
                pygame.mixer.Sound.play(hitoso)
                damage = 10
            elif etankx + 10 > hitx > etankx - 10:
                print('hit hard')
                pygame.mixer.Sound.play(hitoso)
                damage = 8
            elif etankx + 15 > hitx > etankx - 15:
                print('hit 3')
                pygame.mixer.Sound.play(hitoso)
                damage = 5
            elif etankx + 20 > hitx > etankx - 20:
                print('hit 4')
                pygame.mixer.Sound.play(hitoso)
                damage = 3
            elif etankx + 25 > hitx > etankx - 25:
                print('hit 5')
                pygame.mixer.Sound.play(hitoso)
                damage = 1
            #print("impact:", hitx,hity)
            if yshel > groundy:
                # print("last:",xshel,yshel)
                hitx = int((xshel * groundy) / yshel)
                hity = int(groundy)
                explosion(hitx, hity)

            fire = False

        checkx1 = xshel <= xloc+barrierw
        checkx2 = xshel >= xloc
        checky1 = yshel <= groundy
        checky2 = yshel >= display_h-yranh

        if checkx1 and checkx2 and checky1 and checky2:
           # print("last:", xshel, yshel)
            hitx = int((xshel))
            hity = int(yshel)
            #print("impact:", hitx, hity)
            explosion(hitx, hity)
            fire = False

        pygame.display.flip()
        clock.tick(1000)

    return damage

def  fireshellenem(xy,tankx,tanky,turpos,firpow,xloc,yranh,ptankx,ptanky,leve='easy'):
    groundy = 0.9 * display_h + tankh + 5
    currpow = 1
    powfound = False
    damage=0
    while not powfound:
        currpow+=1
        if currpow > 100:
            powfound = True
        #print(currpow)

        fire = True
        startshell = list(xy)
        xshel = startshell[0]
        yshel = startshell[1]
        while fire:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            #pygame.draw.circle(gameDisplay, green, (xshel, yshel), 4)

            xshel += (12 - turpos) * 2
            yshel += int((((xshel - xy[0]) * 0.015 / (currpow / 50)) ** 2) - (turpos + turpos / (12 - turpos)))
            if yshel > groundy:
                hitx = int((xshel * groundy) / yshel)
                hity = int(groundy)
                #explosion(hitx, hity)'
                if ptankx+15> hitx > ptankx-15:
                    print('target acquired')
                    powfound=True
                fire = False

            checkx1 = xshel <= xloc + barrierw
            checkx2 = xshel >= xloc
            checky1 = yshel <= groundy
            checky2 = yshel >= display_h - yranh

            if checkx1 and checkx2 and checky1 and checky2:
                hitx = int((xshel))
                hity = int(yshel)
                #explosion(hitx, hity)
                fire = False

    fire = True
    startshell = list(xy)
    xshel = startshell[0]
    yshel = startshell[1]
    while fire:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #print(xshel,yshel)
        pygame.draw.circle(gameDisplay,green,(xshel,yshel),4)

        if leve == 'easy':
            diff = 0.20
        elif leve == 'medium':
            diff = 0.15
        elif leve == 'hard':
            diff = 0.09

        gunpow = random.randrange(int(currpow*(1-diff)),int(currpow*(1+diff)))

        xshel+= (12 - turpos)*2
        yshel += int((((xshel - xy[0])*0.015/(gunpow/50))**2) - (turpos+turpos/(12-turpos)))
        #print(xshel,yshel)
        if yshel > groundy:
            # print("last:",xshel,yshel)
            hitx = int((xshel * groundy) / yshel)
            hity = int(groundy)
            if ptankx  + 5 > hitx > ptankx  - 5:
                print('hit critic')
                pygame.mixer.Sound.play(hitoso)
                damage = 10
            elif ptankx  + 10 > hitx > ptankx  - 10:
                print('hit hard')
                pygame.mixer.Sound.play(hitoso)
                damage = 8
            elif ptankx  + 15 > hitx > ptankx  - 15:
                print('hit 3')
                pygame.mixer.Sound.play(hitoso)
                damage = 5
            elif ptankx + 20 > hitx > ptankx - 20:
                print('hit 4')
                pygame.mixer.Sound.play(hitoso)
                damage = 3
            elif ptankx + 25 > hitx >ptankx - 25:
                print('hit 5')
                pygame.mixer.Sound.play(hitoso)
                damage = 1
            #print("impact:", hitx,hity)
            if yshel > groundy:
                # print("last:",xshel,yshel)
                hitx = int((xshel * groundy) / yshel)
                hity = int(groundy)
                explosion(hitx, hity)

            fire = False


        checkx1 = xshel <= xloc+barrierw
        checkx2 = xshel >= xloc
        checky1 = yshel <= groundy
        checky2 = yshel >= display_h-yranh

        if checkx1 and checkx2 and checky1 and checky2:
            #print("last:", xshel, yshel)
            hitx = int((xshel))
            hity = int(yshel)
            #print("impact:", hitx, hity)
            explosion(hitx, hity)
            fire = False

        pygame.display.flip()
        clock.tick(500)
    return damage

def power(level):

    screenmessage("your initial vel. : " + str(level)+"%",grey,0,-display_h/2+20,'tiny')

def Tanka(x,y,turpos):

    coltanka = tankcol
    coltanka2 = black
    x=int(x)
    y=int(y)
    rad=int(tankh/2)

    possiturr = [(x-28,y-0),(x-29,y-4),(x-28,y-6),(x-27,y-8),(x-25,y-10),
                 (x-22,y-12),(x-20,y-14),(x-18,y-15),(x-17,y-17),(x-16,y-19),
                 (x-16,y-21),(x-14,y-23)]

    pygame.draw.line(gameDisplay, coltanka, (x, y),possiturr[turpos], turrentw)
    pygame.draw.circle(gameDisplay,coltanka2,(x,y),rad)
   #pygame.draw.circle(gameDisplay, coltanka, (int(x-tankh/2), int(y+tankh)),int(rad/2))
   #pygame.draw.circle(gameDisplay, coltanka, (int(x+tankh/2), int(y+tankh)), int(rad/2))
    startx =12
    for i in range(6):
        pygame.draw.circle(gameDisplay, coltanka2, (x-startx,int(y+tankh)),wheelw)
        startx-=5
    pygame.draw.rect(gameDisplay, coltanka, (x - tankh, y, tankw, tankh))

    return possiturr[turpos]


def enemytank(x,y,turpos):

    coltanka = darkgreen
    coltanka2 = black
    x=int(x)
    y=int(y)
    rad=int(tankh/2)

    possiturr = [(x+28,y-0),(x+29,y-4),(x+28,y-6),(x+27,y-8),(x+25,y-10),
                 (x+22,y-12),(x+20,y-14),(x+18,y-15),(x+17,y-17),(x+16,y-19),
                 (x+16,y-21),(x+14,y-23)]

    pygame.draw.line(gameDisplay, coltanka, (x, y),possiturr[turpos], turrentw)
    pygame.draw.circle(gameDisplay,coltanka2,(x,y),rad)
   #pygame.draw.circle(gameDisplay, coltanka, (int(x-tankh/2), int(y+tankh)),int(rad/2))
   #pygame.draw.circle(gameDisplay, coltanka, (int(x+tankh/2), int(y+tankh)), int(rad/2))
    startx =12
    for i in range(6):
        pygame.draw.circle(gameDisplay, coltanka2, (x-startx,int(y+tankh)),wheelw)
        startx-=5
    pygame.draw.rect(gameDisplay, coltanka, (x - tankh, y, tankw, tankh))

    return possiturr[turpos]

def butthov(x,y,wx,hy,action,butcol, diff = 'easy'):
    cur = pygame.mouse.get_pos()
    #print(cur)
    click = pygame.mouse.get_pressed()
    #print(click)

    if x + wx > cur[0] > x and y + hy > cur[1] > y:
        col  = white
        if click[0] == 1:
            print("lefft-clicked")
        elif click[2] == 1:
            print("right-clicked")
        if click[0] == 1 or click[2]==1 and action!= None:
            if action == 'quit':
                pygame.quit()
                quit()
            elif action == 'play':
                gameloop(diff)
            elif action == 'controls':
                gamecontrol()
            elif action == 'home':
                gameintro()
            elif action == 'easy':
                diff = 'easy'
                gameloop(diff)
            elif action == 'medium':
                diff = 'medium'
                gameloop(diff)
            elif action == 'hard':
                diff = 'hard'
                gameloop(diff)
            elif action == 'replay':
               gameloop(diff)
    else:
        col = butcol
    return  col , diff

#score show
def scoreshow(score):
    text = smallfont.render("ScOrE: "+str(score), True, grey)
    gameDisplay.blit(text,(0,0))

#controls
def gamecontrol():
    buttcol = y
    txtcol = black
    gdiff='easy'
    gamcon = True
    while gamcon == True:

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameintro()
        gameDisplay.fill(y)
        screenmessage('ConTroLs', white, y_displace=-280, szfont='big')
        screenmessage('Fire ->> space_bar',yellowishgreen, y_displace=-120, szfont='small')
        screenmessage("Move Turret ->> Up and Down arrows",red, y_displace=-90, szfont='small')
        screenmessage('Move Tank ->> Left and Right arrows',yellowishgreen, y_displace=-60, szfont='small')
        screenmessage('Pause ->> shift ',red, y_displace=-30, szfont='small')
        #screenmessage('the more enemies you destroy, the harder they get', white, y_displace=120, szfont='small')
        # screenmessage('hit the enemy tanks before they destroy you: ',white,y_displace=110,szfont='small')
        # screenmessage("Press 'Space_bar' to play or 'Q' to quit ",orangebrown,y_displace=190,szfont='small')
        screenmessage("Press 'alt' to pause ", red, y_displace=10, szfont='small')
        screenmessage("Press 'esc' to return HOME ",yellowishgreen, y_displace=40, szfont='small')

        buttcol1,gdiff = butthov(70, 620, 80, 40, 'home',buttcol)
        buttcol2,gdiff = butthov(289, 620, 105, 40, 'play',buttcol)
        buttcol3,gdiff = butthov(550, 620, 80, 40, 'quit',buttcol)

        pygame.draw.rect(gameDisplay, buttcol1, (70, 620, 80, 40))
        pygame.draw.rect(gameDisplay, buttcol2, (289, 620, 105, 40))
        pygame.draw.rect(gameDisplay, buttcol3, (550, 620, 80, 40))

        textonbutton("Home", txtcol, 70, 620, 80, 30, 'small')
        textonbutton("play", txtcol, 300, 620, 80, 30, 'small')
        textonbutton("quit", txtcol, 550, 620, 80, 30, 'small')

        pygame.display.flip()
        clock.tick(5)

#paused
def pause(gamecol):
    paused = True
    #gameDisplay.fill(gamecol)
    screenmessage("PAUSED!!!",orangebrown, y_displace=-150, szfont='big')
    screenmessage("Press 'alt' to continue or 'q' to Quit...",
                  orangebrown, y_displace=100, szfont='small')
    pygame.display.flip()

    while paused:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_LALT or event.key == pygame.K_RALT:
                    paused = False

    clock.tick(5)

def gameintro():
    global count
    count = 0
    buttcol = grey
    txtcol = black
    intro = True
    while intro == True:

        if count%2 == 0:
            maycol = orange
        elif  count%2 == 1:
            maycol = white

        gameDisplay.fill(grey)
        screenmessage('WeLcOmE', green, y_displace=-250, szfont='big')
        screenmessage('TO', red, y_displace=-150, szfont='big')
        screenmessage("TaNkS", y, y_displace=-60, szfont='big')
        screenmessage('the Plays are: ', orangebrown, y_displace=20, szfont='mid')
        screenmessage('hit the enemy tanks before they destroy you: ', white, y_displace=80, szfont='small')
        screenmessage('the more enemies you destroy, the harder they get', white, y_displace=120, szfont='small')
        # screenmessage('hit the enemy tanks before they destroy you: ',white,y_displace=110,szfont='small')
        screenmessage("-->Press 'Space_bar' to choose difficulty", red, y_displace=150, szfont='small')
        screenmessage("!!MaYHeM!!", maycol, y_displace=199, szfont='mid')

        buttcol1, gdiff = butthov(70, 620, 105, 40, 'controls', butcol=buttcol)
        buttcol2, gdiff = butthov(289, 620, 105, 40, 'play', butcol=buttcol)
        buttcol3, gdiff = butthov(550, 620, 80, 40, 'quit', butcol=buttcol)

        pygame.draw.rect(gameDisplay, buttcol1, (70, 620, 105, 40))
        pygame.draw.rect(gameDisplay, buttcol2, (289, 620, 105, 40))
        pygame.draw.rect(gameDisplay, buttcol3, (550, 620, 80, 40))

        textonbutton("controls", txtcol, 70, 620, 105, 30, 'small')
        textonbutton("play", txtcol, 300, 620, 80, 30, 'small')
        textonbutton("quit", txtcol, 550, 620, 80, 30, 'small')

        count += 1
        # print(count)
        pygame.display.flip()
        clock.tick(3)

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                   gdiff = choosediff(coldiff, black)
                   gdiff = gdiff
                   intro = False
                if event.key == pygame.K_q:
                    print('game quitted')
                    pygame.quit()
                    quit()

    return gdiff

def textonbutton(msg,color,butx,buty,butw,buth,szfont='small'):
     textlook,textrect = text_objects(msg,color,szfont)
     textrect.center = ((butx + (butw/2)),buty+(buth/2))
     gameDisplay.blit(textlook,textrect)


#text screen1
def text_objects(text,color,szfont):
    if szfont == 'small':
        textsurface =  smallfont.render(text,True,color)
    if szfont == 'mid':
        textsurface =  midfont.render(text,True,color)
    if szfont == 'big':
        textsurface =  bigfont.render(text,True,color)
    if szfont == 'tiny':
        textsurface =  tinyfont.render(text,True,color)
    return textsurface, textsurface.get_rect()

#text screen2
def screenmessage( msg,color,x_displace=0,y_displace=0,szfont='small'):
    textscreen, textrect = text_objects(msg,color,szfont)
    #screentext = font.render(msg,True,color)
    #gameDisplay.blit(screentext, [display_w/2,display_h/2])
    textrect.center = (display_w/2+x_displace, display_h/2+y_displace)
    gameDisplay.blit(textscreen,textrect)

# game over display
def gameoverdisplay(countcol,tdisp,diff):
    buttcol = grey
    txtcol = black
    gdiff='easy'
    gameDisplay.fill(countcol)
    screenmessage('GAME OVER', tdisp,y_displace=-250,szfont='big')
    screenmessage('R.I.Pieces', tdisp, y_displace=-10, szfont='mid')
    screenmessage('...SMH!!!...', tdisp, y_displace=150, szfont='big')

    buttcol1,gdiff = butthov(70, 620, 80, 40, 'home', buttcol,diff)
    buttcol2,gdiff = butthov(289, 620, 105, 40, 'replay', buttcol,diff)
    buttcol3,gdiff = butthov(550, 620, 80, 40, 'quit', buttcol,diff)

    pygame.draw.rect(gameDisplay, buttcol1, (70, 620, 80, 40))
    pygame.draw.rect(gameDisplay, buttcol2, (289, 620, 105, 40))
    pygame.draw.rect(gameDisplay, buttcol3, (550, 620, 80, 40))

    textonbutton("Home", txtcol, 70, 620, 80, 30, 'small')
    textonbutton("replay", txtcol, 300, 620, 80, 30, 'small')
    textonbutton("quit", txtcol, 550, 620, 80, 30, 'small')

    pygame.display.update()
    clock.tick(10)

    return gdiff


def youwindisplay(countcol,tdisp,diff):
    buttcol = grey
    txtcol = black
    buttcol1=buttcol
    buttcol2 = buttcol
    buttcol3 = buttcol
    gameDisplay.fill(countcol)
    screenmessage('You Win', tdisp,y_displace=-250,szfont='big')
    screenmessage('blew his head off', tdisp, y_displace=-150, szfont='mid')
    screenmessage('...LmaO!!!...', tdisp, y_displace=150, szfont='big')

    buttcol1,gdiff = butthov(70, 620, 80, 40, 'home', buttcol,diff)
    buttcol2,gdiff = butthov(289, 620, 105, 40, 'replay', buttcol,diff)
    buttcol3,gdiff = butthov(550, 620, 80, 40, 'quit', buttcol,diff)

    pygame.draw.rect(gameDisplay, buttcol1, (70, 620, 80, 40))
    pygame.draw.rect(gameDisplay, buttcol2, (289, 620, 105, 40))
    pygame.draw.rect(gameDisplay, buttcol3, (550, 620, 80, 40))

    textonbutton("Home", txtcol, 70, 620, 80, 30, 'small')
    textonbutton("replay", txtcol, 300, 620, 80, 30, 'small')
    textonbutton("quit", txtcol, 550, 620, 80, 30, 'small')

    pygame.display.update()
    clock.tick(10)

    return gdiff

def choosediff(countcol,tdisp):
    buttcol = grey
    txtcol = black
    diffcon = True
    gdiff = 'easy'
    while diffcon == True:

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                pass

        gameDisplay.fill(countcol)
        screenmessage('Choose', tdisp,y_displace=-250,szfont='big')
        screenmessage('difficulty', tdisp, y_displace=-150, szfont='mid')
        #screenmessage('...LmaO!!!...', tdisp, y_displace=150, szfont='big')

        buttcol1,gdiff = butthov(70, 620, 80, 40, 'easy', buttcol)
        buttcol2,gdiff = butthov(289, 620, 105, 40, 'medium', buttcol)
        buttcol3,gdiff = butthov(550, 620, 80, 40, 'hard', buttcol)

        pygame.draw.rect(gameDisplay, buttcol1, (70, 620, 80, 40))
        pygame.draw.rect(gameDisplay, buttcol2, (289, 620, 105, 40))
        pygame.draw.rect(gameDisplay, buttcol3, (550, 620, 80, 40))

        textonbutton("easy", txtcol, 70, 620, 80, 30, 'small')
        textonbutton("medium", txtcol, 300, 620, 80, 30, 'small')
        textonbutton("hard", txtcol, 550, 620, 80, 30, 'small')

        pygame.display.update()
        clock.tick(10)
    return gdiff


def healthbars(playerhealth,enemyhealth):

    if playerhealth>70:
        colplayerhealth = green
    elif playerhealth<40:
        colplayerhealth = darkred
    else:
        colplayerhealth = orangebrown

    if enemyhealth>70:
        colenemyhealth = green
    elif enemyhealth<40:
        colenemyhealth = darkred
    else:
        colenemyhealth = orangebrown

    pygame.draw.rect(gameDisplay,colplayerhealth,(display_w-120,25,playerhealth,25))
    screenmessage(str(playerhealth)+'%',colplayerhealth,(display_w/2)-150,35-display_h/2,'tiny')
    pygame.draw.rect(gameDisplay, colenemyhealth, (20, 25, enemyhealth, 25))
    screenmessage(str(enemyhealth) + '%', colenemyhealth,(-display_w/2)+150, 35 - display_h / 2, 'tiny')

def gameloop(diff):

    fps = 10
    gameExit = False
    gameOver = False
    gamecol = whiteyellow
    mainTankx = display_w * 0.9
    mainTanky = display_h * 0.9
    tankmov = 0
    turpos = 0
    chtur = 0
    xloc = (display_w / 2) + random.randint(-0.3* display_w, 0.3 * display_w)
    yranh = random.randrange(display_h * 0.15, display_h * 0.30)
    groundy = 0.9 * display_h + tankh + 5
    firpow = 50
    powch = 0
    enemtanx = display_w * 0.1
    enemtany = display_h * 0.9
    playerhealth = 100
    enemyhealth = 100

    #game exit loop
    while gameExit == False:

         gameDisplay.fill(gamecol)
         healthbars(playerhealth,enemyhealth)
         gun = Tanka(mainTankx, mainTanky,turpos)
         enemgun = enemytank(enemtanx,enemtany,turpos)
         firpow += powch
         if firpow >= 100:
             firpow = 100
         if firpow <= 0:
             firpow =0
         power(firpow)
         barrier(xloc, yranh)

         pygame.draw.rect(gameDisplay, fieldgreen,
                          (0, groundy, display_w, display_h - groundy))


         fps+=0
         # KEYS
         for event in pygame.event.get():
             if event.type==pygame.QUIT:
                 gameExit = True
             #print(event)
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LEFT:
                     tankmov = -5
                 elif event.key == pygame.K_RIGHT:
                     tankmov = 5
                 elif event.key == pygame.K_UP:
                     chtur=1
                 elif event.key == pygame.K_DOWN:
                     chtur=-1
                 elif event.key == pygame.K_RALT or event.key == pygame.K_LALT :
                    pause(gamecol)
                 elif event.key == pygame.K_ESCAPE:
                    gameintro()
                 elif event.key == pygame.K_a:
                    powch = -1
                 elif event.key == pygame.K_d:
                    powch = 1
                 elif event.key == pygame.K_SPACE:
                    edamage = fireshell(gun, mainTankx, mainTanky, turpos, firpow,xloc,yranh, enemtanx, enemtany)
                    enemyhealth -= edamage
                    pdamage = fireshellenem(enemgun, enemtanx, enemtany, turpos,50, xloc, yranh,mainTankx,mainTanky,diff)
                    playerhealth -= pdamage

                    possmov =["f","r"]
                    movindex = random.randrange(0,2)

                    for i in range(random.randrange(0,10)):
                        if enemtanx > xloc-30 and enemtanx < 0 or edamage!= 0:
                            if possmov[movindex] == 'f':
                                enemtanx+=5
                            elif possmov[movindex] == 'r':
                                enemtanx-=5
                            elif enemtanx  < 20:
                                enemtanx += 5
                            elif enemtanx > xloc-30 :
                                enemtanx-= 5

                            gameDisplay.fill(gamecol)
                            healthbars(playerhealth, enemyhealth)
                            gun = Tanka(mainTankx, mainTanky, turpos)
                            enemgun = enemytank(enemtanx, enemtany, turpos)
                            firpow += powch
                            if firpow >= 100:
                                firpow = 100
                            if firpow <= 0:
                                firpow = 1
                            power(firpow)
                            barrier(xloc, yranh)

                            pygame.draw.rect(gameDisplay, fieldgreen,
                                             (0, groundy, display_w, display_h - groundy))
                            pygame.display.update()
                            clock.tick(fps)


             if event.type == pygame.KEYUP:
                 if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankmov = 0
                 elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    chtur= 0
                 elif event.key == pygame.K_a or event.key == pygame.K_d:
                     powch = 0

         if mainTankx-tankw/2<xloc+barrierw :
             mainTankx+=5
         if mainTankx>=display_w-5 :
             mainTankx-=5

         mainTankx += tankmov
         turpos += chtur

         if turpos > 11:
             turpos = 11
         elif turpos < 0:
             turpos = 0

         if playerhealth<1:
             gameoverdisplay(red, white, diff)
             #gameExit = True

         elif enemyhealth<1:
             youwindisplay(green, whiteyellow, diff)
             #gameExit = True


         clock.tick(fps)
         #time.sleep(.1)
         pygame.display.flip()

    print('\nGAME OVER')
    #pygame.display.flip()
    #time.sleep(2)
    pygame.quit()
    quit()


gameDisplay.fill(white)
pygame.display.flip()

diff=gameintro()
gameloop(diff)