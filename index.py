from email.mime import base
from unicodedata import name
import pygame
import sys
import random
import csv

from sqlalchemy import true
## IMPORTS
import mindwave
from psychopy import visual
import json
import time
import pandas as pd
from random import choices
from tqdm import tqdm
import sys
import os
from os.path import join as pjoin

name1 = input("Enter name : ")




learn_threshold = True

trial_only = False


print("Connecting...")
# headset = mindwave.Headset('/dev/tty.MindWaveMobile-SerialPo') # mac version
headset = mindwave.Headset('COM8') # windows version. set up COM port first (see video) change COM6 to whichever
print("Connected!")
print("Starting...")
headset.serial_open()
# Wait for the headset to steady down
while (headset.poor_signal > 5 or headset.attention == 0):
    time.sleep(0.1)
def on_blink(headset, blink_strength):
    print("Blink detected.")

headset.blink_handlers.append(on_blink)


print("Calibrating... please don't blink for 10 seconds")
start_time = time.time()
raw_total = 0
while (time.time()- start_time) < 10:
    raw_total += headset.raw_value
    time.sleep(1)
base_line = raw_total / 10


numBlinks = 0
threshold = 135


if learn_threshold:
    while(numBlinks < 8 or numBlinks > 12): 
        print("When you see START blink 10 times, pause for a second after blinks")
        numBlinks = 0
        time.sleep(2.5)
        print("START")

        print(threshold)
        start_time = time.time()
        while (time.time()- start_time) < 15:
            attention = headset.attention
            raw_val = headset.raw_value
            if abs(raw_val) > threshold + abs(attention)/2 + base_line:
                numBlinks += 1
                time.sleep(.4)

        if numBlinks < 8 or numBlinks > 12:
            threshold -= (10 - numBlinks)*2

        print(numBlinks)
        print(threshold)
else: 
    print("When you see START blink 10 times, pause for a second after blinks")
    numBlinks = 0
    time.sleep(2.5)
    print("START")
    print(threshold)
    start_time = time.time()
    while (time.time()- start_time) < 15:
        attention = headset.attention
        raw_val = headset.raw_value
        if abs(raw_val) > threshold + abs(attention)/2 + base_line:
            numBlinks += 1
            time.sleep(.4)

    #if name1 in rows[:][0]:
    #    trial = 1
    #    for element in rows:
    #        if element == name1:
    #            trial += 1
    #else:
    #    trial = 1

    
import pandas as pd

# reading the csv file
df = pd.read_csv('data.csv')
df.loc[len(df) + 1] = [name1, 1, threshold, numBlinks]

# writing into the file
df.to_csv('data.csv', mode='a', index=False, header = False)
    


if not trial_only:
    pygame.init()

    width = 400
    height = 500
    pygame.display.set_caption('Simple Stacking Game')
    display = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    background = (23, 32, 42)

    white = (236, 240, 241)


    color = [(31, 40, 120), (38, 49, 148), (46, 58, 176), (53, 67, 203), (60, 76, 231), (99, 112, 236), (138, 148, 241), (177, 183, 245), (216, 219, 250), (236, 237, 253),
                (231, 249, 254), (207, 243, 252), (159, 231, 249), (111, 220, 247), (63, 208, 244), (15, 196, 241), (13, 172, 212), (11, 149, 183), (10, 125, 154), (8, 102, 125),
             (9, 81, 126), (12, 100, 156), (14, 119, 185), (30, 111, 202), (16, 137, 214), (18, 156, 243), (65, 176, 245), (113, 196, 248),(160, 215, 250), (208, 235, 253), (231, 245, 254),
             (232, 246, 243), (162, 217, 206), (162, 217, 206),
             (115, 198, 182), (69, 179, 157), (22, 160, 133),
             (19, 141, 117), (17, 122, 101), (14, 102, 85),
             (11, 83, 69),
             (21, 67, 96), (26, 82, 118), (31, 97, 141),
            (36, 113, 163), (41, 128, 185), (84, 153, 199),
            (127, 179, 213), (169, 204, 227), (212, 230, 241),
            (234, 242, 248),
             (230, 238, 251), (204, 221, 246), (153, 187, 237),
             (112, 152, 229), (51, 118, 220), (0, 84, 211),
             (0, 74, 186), (0, 64, 160), (0, 54, 135),
             (0, 44, 110)
             ]

    colorIndex = 0

    brickH = 10
    brickW = 100

    score = 0
    speed = 3



    class Brick:
        def __init__(self, x, y, color, speed):
            self.x = x
            self.y = y
            self.w = brickW
            self.h = brickH
            self.color = color
            self.speed = speed

        def draw(self):
            pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h))

        def move(self):
            self.x += self.speed
            if self.x > width:
                self.speed *= -1
            if self.x + self.w < 1:
                self.speed *= -1



    class Stack:
        def __init__(self):
            global colorIndex
            self.stack = []
            self.initSize = 25
            for i in range(self.initSize):
                newBrick = Brick(width/2 - brickW/2, height - (i + 1)*brickH, color[colorIndex], 0)
                colorIndex += 1
                self.stack.append(newBrick)

        def show(self):
            for i in range(self.initSize):
                self.stack[i].draw()

        def move(self):
            for i in range(self.initSize):
                self.stack[i].move()

        def addNewBrick(self):
            global colorIndex, speed

            headset.attention % len(color)

            y = self.peek().y
            if score > 50:
                speed += 0
            elif score%5 == 0:
                speed += 1

            newBrick = Brick(width, y - brickH, color[colorIndex], speed)
            colorIndex += 1
            self.initSize += 1
            self.stack.append(newBrick)

        def peek(self):
            return self.stack[self.initSize - 1]

        def pushToStack(self):
            global brickW, score
            b = self.stack[self.initSize - 2]
            b2 = self.stack[self.initSize - 1]
            if b2.x <= b.x and not (b2.x + b2.w < b.x):
                self.stack[self.initSize - 1].w = self.stack[self.initSize - 1].x + self.stack[self.initSize - 1].w - b.x
                self.stack[self.initSize - 1].x = b.x
                if self.stack[self.initSize - 1].w > b.w:
                    self.stack[self.initSize - 1].w = b.w
                self.stack[self.initSize - 1].speed = 0
                score += 1
            elif b.x <= b2.x <= b.x + b.w:
                self.stack[self.initSize - 1].w = b.x + b.w - b2.x
                self.stack[self.initSize - 1].speed = 0
                score += 1
            else:
                gameOver()
            for i in range(self.initSize):
                self.stack[i].y += brickH

            brickW = self.stack[self.initSize - 1].w


    def gameOver():
        loop = True

        font = pygame.font.SysFont("ARIAL", 60)
        text = font.render("Game Over!", True, white)

        textRect = text.get_rect()
        textRect.center = (width/2, height/2 - 80)

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    if event.key == pygame.K_r:
                        gameLoop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    gameLoop()
            display.blit(text, textRect)

            pygame.display.update()
            clock.tick()


    def showScore():
        font = pygame.font.SysFont("ARIAL", 30)
        text = font.render("Score: " + str(score), True, white)
        display.blit(text, (10, 10))



    def close():
        pygame.quit()
        sys.exit()


    def gameLoop():
        global brickW, brickH, score, colorIndex, speed
        loop = True

        brickH = 10
        brickW = 200
        colorIndex = 15
        speed = 3

        score = 0

        stack = Stack()
        stack.addNewBrick()

        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:

                        close()
                    if event.key == pygame.K_r:
                        gameLoop()
            attention = headset.attention
            if abs(headset.raw_value) > threshold + abs(attention)/2 + base_line:
                stack.pushToStack()
                time.sleep(.4)
                stack.addNewBrick()



            display.fill(background)

            stack.move()
            stack.show()

            showScore()

            pygame.display.update()
            clock.tick(60)

    gameLoop()


