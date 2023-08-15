from msilib.schema import Font
import os
import subprocess
from tkinter import *
from turtle import bgcolor
import pygame, sys, random
from pygame.locals import *
import mediapipe as mp
from videosource import WebcamSource
from video import threadVideo
win = Tk()
def run_texttospeech():
        import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_mesh_connections = mp.solutions.face_mesh_connections
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=3)


def run_game():
        WINDOWWIDTH = 400
        WINDOWHEIGHT = 560

        BIRDWIDTH = 30
        BIRDHEIGHT = 30
        G = 0.3
        SPEEDFLY = -4
        BIRDIMG = pygame.image.load('img/bird.png')

        COLUMNWIDTH = 60
        COLUMNHEIGHT = 500
        BLANK = 300
        DISTANCE = 300
        COLUMNSPEED = 1

        COLUMNIMG = pygame.image.load('img/column.png')

        BACKGROUND = pygame.image.load('img/background.png')

        pygame.init()
        FPS = 60
        fpsClock = pygame.time.Clock()

        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('monster on run')

        class Bird():
                def __init__(self):
                        self.width = BIRDWIDTH
                        self.height = BIRDHEIGHT
                        self.x = (WINDOWWIDTH - self.width)/2
                        self.y = (WINDOWHEIGHT- self.height)/2
                        self.speed = 0
                        self.suface = BIRDIMG

                def draw(self):
                        DISPLAYSURF.blit(self.suface, (int(self.x), int(self.y)))
    
                def update(self, mouseClick):
                        self.y += self.speed + 0.5*G
                        self.speed += G
                        if mouseClick == True:
                                self.speed = SPEEDFLY

        class Columns():
                def __init__(self):
                        self.width = COLUMNWIDTH
                        self.height = COLUMNHEIGHT
                        self.blank = BLANK
                        self.distance = DISTANCE
                        self.speed = COLUMNSPEED
                        self.surface = COLUMNIMG
                        self.ls = []
                        for i in range(3):
                                x = WINDOWWIDTH + i*self.distance
                                y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 20)
                                self.ls.append([x, y])
        
                def draw(self):
                        for i in range(3):
                                DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] - self.height))
                                DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))
    
                def update(self):
                        for i in range(3):
                                self.ls[i][0] -= self.speed
        
                        if self.ls[0][0] < -self.width:
                                self.ls.pop(0)
                                x = self.ls[1][0] + self.distance
                                y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 10)
                                self.ls.append([x, y])

        def rectCollision(rect1, rect2):
                if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
                        return True
                return False

        def isGameOver(bird, columns):
                for i in range(3):
                        rectBird = [bird.x, bird.y, bird.width, bird.height]
                        rectColumn1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
                        rectColumn2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
                        if rectCollision(rectBird, rectColumn1) == True or rectCollision(rectBird, rectColumn2) == True:
                                return True
                if bird.y + bird.height < 0 or bird.y + bird.height > WINDOWHEIGHT:
                        return True
                return False

        class Score():
                def __init__(self):
                        self.score = 0
                        self.addScore = True
    
                def draw(self):
                        font = pygame.font.SysFont('consolas', 40)
                        scoreSuface = font.render(str(self.score), True, (0, 0, 0))
                        textSize = scoreSuface.get_size()
                        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - textSize[0])/2), 100))
    
                def update(self, bird, columns):
                        collision = False
                        for i in range(3):
                                rectColumn = [columns.ls[i][0] + columns.width, columns.ls[i][1], 1, columns.blank]
                                rectBird = [bird.x, bird.y, bird.width, bird.height]
                                if rectCollision(rectBird, rectColumn) == True:
                                        collision = True
                                        break
                        if collision == True:
                                if self.addScore == True:
                                        self.score += 1
                                self.addScore = False
                        else:
                                self.addScore = True

        def gameStart(bird):
                bird.__init__()

                font = pygame.font.SysFont('consolas', 40)
                headingSuface = font.render('monster on run', True, (255, 255, 0))
                headingSize = headingSuface.get_size()
                
                font = pygame.font.SysFont('consolas', 20)
                commentSuface = font.render('Click to start', True, (255, 100, 100))
                commentSize = commentSuface.get_size()
    
                while True:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == MOUSEBUTTONDOWN:
                                        return

                        DISPLAYSURF.blit(BACKGROUND, (0, 0))
                        bird.draw()
                        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
                        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))

                        pygame.display.update()
                        fpsClock.tick(FPS)

        def gamePlay(bird, columns, score, xyz):
                bird.__init__()
                bird.speed = SPEEDFLY
                columns.__init__()
                score.__init__()
                while True:
                        mouseClick = False
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == MOUSEBUTTONDOWN:
                                        mouseClick = True
                        if xyz.dist < 0.1:
                                mouseClick = True
                        print(xyz.dist)
                        DISPLAYSURF.blit(BACKGROUND, (0, 0))
                        columns.draw()
                        columns.update()
                        bird.draw()
                        bird.update(mouseClick)
                        score.draw()
                        score.update(bird, columns)

                        if isGameOver(bird, columns) == True:
                                return

                        pygame.display.update()
                        fpsClock.tick(FPS)

        def gameOver(bird, columns, score):
                font = pygame.font.SysFont('consolas', 60)
                headingSuface = font.render('GAMEOVER', True, (255, 0, 0))
                headingSize = headingSuface.get_size()
                
                font = pygame.font.SysFont('consolas', 20)
                commentSuface = font.render('Press "space" to replay', True, (0, 0, 0))
                commentSize = commentSuface.get_size()

                font = pygame.font.SysFont('consolas', 30)
                scoreSuface = font.render('Score: ' + str(score.score), True, (0, 0, 0))
                scoreSize = scoreSuface.get_size()

                while True:
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                                if event.type == KEYUP:
                                        if event.key == K_SPACE:
                                                return
        
                        DISPLAYSURF.blit(BACKGROUND, (0, 0))
                        columns.draw()
                        bird.draw()
                        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
                        DISPLAYSURF.blit(commentSuface, (int((WINDOWWIDTH - commentSize[0])/2), 500))
                        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - scoreSize[0])/2), 160))

                        pygame.display.update()
                        fpsClock.tick(FPS)

        def main():
                bird = Bird()
                columns = Columns()
                score = Score()
                xyz = threadVideo()
                xyz.start()
                
                while True:
        
                        gameStart(bird)
                        gamePlay(bird, columns, score, xyz)
                        gameOver(bird, columns, score)

        if __name__ == '__main__':
                main()
#giving title 
win.title('hawk eye')
win.iconbitmap('back-ground.ico')
#setting geomtry of the gui
win.geometry("600x600")
win.configure(background = 'black')
#placing the main image or logo in the gui
bg = PhotoImage(file = "back-ground.png")
background = Label(win, image=bg, bd=0)
#using pack as i want center allignment
background.pack()
lbl = Label(win, text ='hand sign to speech converter and play game using hand sign', bg='black',fg='skyblue')
lbl.pack()
#setting font for friendly view
Font = ("Comic Sans Ms", 30, "bold")
lbl.configure(font = Font )
label2 = Label( win, text = "Welcome",bg='black',fg='purple')
label2.pack(pady = 50)
label2.configure(font = Font)
#trying to place image
my_canvas1 = Canvas(win, width=250, height=215, bg='black')
my_canvas1.place(x=83, y=580)
#introducing image1
start = PhotoImage(file = 'start.png')
start_but1= my_canvas1.create_image(128,110, image=start)
but1 = Button(win ,text="convert to speech", command = run_texttospeech)
but1.place(x= 100, y= 800)
but1.config(height = 1, width = 30)
#placing image 2
my_canvas2 = Canvas(win, width=250, height=215, bg='black')
my_canvas2.place(x=733, y=580)
stop = PhotoImage(file='stop1.png')
stop_but2=my_canvas2.create_image(130,110,image=stop)
but2 = Button( win , text = "play game", command = run_game)
but2.place(x=750, y = 800)
but2.config(height = 1, width = 30)
#placing image 3
my_canvas3 = Canvas(win, width=250, height=215, bg='black')
my_canvas3.place(x=1382, y=580)
Exit = PhotoImage(file='exit.png')
Exit_but3= my_canvas3.create_image(128,110,image=Exit)
but3 = Button( win, text = "Exit", command = win.destroy)
but3.place(x=1400 , y = 800)
but3.config(height = 1, width = 30)
#def updatecorners(round,x1,y1,x2,y2,r=25):
#points = (x1+r, y1, x1+r, y1, x2-r, y1, x2, y1+r, x2, y1+r, x2, y2-r)
#canvas.coords(round, *points)
#want round button and bg box but not able to find any solution
win.mainloop()