import random
import turtle
import copy
import time
from turtle import Screen

# head, snake,finished are global vars
finished=False
game_state = True
contact=0
snake=[(0,0),(0,20),(0,40),(0,60),(0,80)] # position of each part of snake
head=snake[-1]
monster=(-100,-100)
turtle.shape('square')

def init_screen(w=500,h=500) -> Screen():
    # return a turtle.Screen() object
    # w,h are width & height of the screen object
    s=Screen()
    s.setup(w,h)
    s.title('Snake')
    s.tracer(0)
    return s

def turn_snake_to_pixel_state():
    # toggle state of the game (Run or Pause)
    global game_state 
    game_state = not game_state 

def draw_snake(snake): 
    #Draw the snake block by block
    turtle.shape('square')
    turtle.color('green','black')
    i=0
    while i<=len(snake)-1:
        turtle.penup()
        turtle.goto(snake[i])
        turtle.stamp()
        i+=1
        if i==len(snake)-1:
            turtle.color('orange','red')

def instruction():
    turtle.penup()
    turtle.goto(-200,120)
    turtle.pendown()
    turtle.write('''Welcome to my snake game...
You are going to use the 4 arrow keys to move the snake
around the screen, trying to consume all the food 
items before the monster catches you...

Click anywhere on the screen 
to start the game.''',font='black 12 bold')

aim=[0,20]
def turn_snake_to_pixel(x,y): 
    #turn_snake_to_pixel the direction of the snake.
    global aim
    aim[0]=x
    aim[1]=y

def get_foods():
    global foods
    Foods=[]
    position=[]
    i=1
    value=0
    while i<=9:
        while True:
            x=(random.randint(-11,11))*20
            y=random.randint(-11,11)*20
            if (x,y) not in position:
                break
        position.append((x,y))
        value+=1
        food=(x,y,value)
        Foods.append(food)
        i+=1
    return Foods
foods=get_foods()

def draw_monster(monster):
    turtle.shape('square')
    turtle.color('purple')
    turtle.penup()
    turtle.goto(monster)
    turtle.stamp()

aim_monster=(8,8)

def contacted():
    for i in snake:
        if -20<= monster[0]-i[0]<=20 and -20<= monster[1]-i[1]<=20:
            return True
    return False

def move_monster():
    global monster, startTime, contact,finished
    current_time=time.time()
    speed_snake=200
    time_passed=int(current_time-startTime)
    print(time_passed)
    print(game_state )
    if finished==False:
        if contacted()==True:  #Count the number of times of contaction.
            contact+=1
        if game_state ==True:
            finished=False
            switch=True
            turtle.clear()
            monster=copy.deepcopy(monster)
            if finished!= True:
                head=copy.deepcopy(snake[-1]) #Move the snake.
                head= (head[0]+aim[0], head[1]+aim[1])
                if -240<= head[0]<= 240 and -240<= head[1]<= 240: #Snake doesn't exceed the boundary.
                    snake.append(head)
                    snake.pop(0)
                for (x,y,value) in foods: #Go to the appropriate position and write the number.
                    turtle.color('blue')
                    turtle.penup()
                    turtle.goto(x,y)
                    turtle.pendown()
                    turtle.write(value)
                draw_snake(snake)
                dict_food={}
                for (x,y,value) in foods: #Create a dictionary of positions corresponding to values.
                    dict_food[(x,y)]=value
                if head in dict_food.keys():
                    for i in range(dict_food[head]):
                        snake.append(head)
                        speed_snake=250
                    for (x,y,z) in foods:
                        if (x,y)== head:
                            foods.remove((x,y,z))
                if len(foods)==0: #All foods are eaten.
                    finished = True
                draw_snake(snake)
                if finished==True: #Present the final status.
                    draw_snake(snake)
                    draw_monster(monster)
                    turtle.color('cyan')
                    turtle.penup()
                    turtle.goto(snake[-1][0]-40,snake[-1][1]-40)
                    turtle.write('Winner!!!',align='left',font='Arial 16 bold')
            speed_monster= random.randint(190,210)  #The speed of the monster is slightly different from that of the snake.
            if finished!=True:
                if (switch==True): #If the monster is on the upper right of the snake's head, then it should go to lower left.
                    if monster[0]< snake[-1][0]:
                        monster=(monster[0]+ aim_monster[0],monster[1])
                    elif monster[0] > snake[-1][0]:
                        monster= (monster[0]- aim_monster[0],monster[1])
                switch=False
                if (switch==False):
                    if monster[1]< snake[-1][1]:
                        monster=(monster[0],monster[1]+aim_monster[1])
                    elif monster[1]> snake[-1][1]:
                        monster= (monster[0],monster[1]-aim_monster[1])
                    switch=True
                if -20<=monster[0]-snake[-1][0]<=20 and -20<=monster[1]- snake[-1][1]<=20:
                    finished = True
                draw_monster(monster)
                if finished!=True:
                    pass
                else:
                    draw_monster(monster)
                    turtle.penup()
                    turtle.goto(snake[-1][0]-40,snake[-1][1]-40)
                    turtle.write('Game Over!!!',align='left',font='Arial 16 bold')    
        g_screen.title('Snake   Contracted: %d, Time:%d'%(contact,time_passed ))
        print('contact:',contact)
        turtle.update()
        g_screen.tracer(0)
    turtle.ontimer(move_monster,speed_snake)

def start(): #Initialize the game and prompt the user to click and start.
    startTime=time.time()
    turtle.clear()
    get_foods()
    for (x,y,value) in foods:
        turtle.color('black')
        turtle.penup()
        turtle.goto((x,y))
        turtle.pendown()
        turtle.write(value)    
    instruction()
    draw_snake(snake)
    draw_monster(monster)

def main(x,y):
    global startTime
    turtle.hideturtle()
    turtle.listen()
    turtle.onkey(lambda: turn_snake_to_pixel(0,20), 'Up')
    turtle.onkey(lambda: turn_snake_to_pixel(0,-20), 'Down')
    turtle.onkey(lambda: turn_snake_to_pixel(-20,0), 'Left')
    turtle.onkey(lambda: turn_snake_to_pixel(20,0), 'Right')
    turtle.onkey(turn_snake_to_pixel_state, 'space')
    startTime=time.time()
    print('time:',startTime)
    instruction()
    move_monster()
    turtle.update()
    turtle.done()

g_screen=init_screen()
g_screen.tracer(0)
turtle.tracer(False)
start()
turtle.listen()
turtle.onscreenclick(main)
turtle.done()
