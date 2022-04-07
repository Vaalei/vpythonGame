import os
import signal
from vpython import *

def quitProg():
    global continue_loop
    continue_loop = False

def getbbPosSize(bbData):
    minmax = [[],[],[],[],[],[]] 
    for corner in bbData:
        minmax[0].append(corner.x)
        minmax[1].append(corner.y)
        minmax[2].append(corner.z)
    bb = []
    bb.append(min(minmax[0]))
    bb.append(max(minmax[0]))
    bb.append(min(minmax[1]))
    bb.append(max(minmax[1]))
    bb.append(min(minmax[2]))
    bb.append(max(minmax[2]))
    bb_pos = vec(bb[0]+(bb[1]-bb[0])/2, bb[2]+(bb[3]-bb[2])/2, bb[4]+(bb[5]-bb[4])/2)
    bb_size = vec(bb[1]-bb[0], bb[3]-bb[2], bb[5]-bb[4])
    return (bb_pos, bb_size)

def detectCol(obj1, obj2):
    if isinstance(obj1, box) and isinstance(obj2, box):
        xSize = (obj1.length + obj2.length)/2
        ySize = (obj1.height + obj2.height)/2
        zSize = (obj1.width + obj2.width)/2
        currDist = obj1.pos - obj2.pos
        xRange = abs(currDist.x) - xSize
        yRange = abs(currDist.y) - ySize
        zRange = abs(currDist.z) - zSize
        if xRange <= 0 and yRange <= 0 and zRange <= 0:
            if xRange > yRange and xRange > zRange:
                if currDist.x < 0:
                    hitArea = 'left' 
                else:
                    hitArea = 'right' 
            elif yRange > xRange and yRange > zRange:
                if currDist.y < 0:
                    hitArea = 'below' 
                else:
                    hitArea = 'above'
            else:
                if currDist.z < 0:
                    hitArea = 'front' 
                else:
                    hitArea = 'back'
        else:
            hitArea = 'noHit'
    elif isinstance(obj1, sphere) and isinstance(obj2, box):
        xSize = (obj1.radius + obj2.length)/2
        ySize = (obj1.radius + obj2.height)/2
        zSize = (obj1.radius + obj2.width)/2
        currDist = obj1.pos - obj2.pos
        xRange = abs(currDist.x) - xSize
        yRange = abs(currDist.y) - ySize
        zRange = abs(currDist.z) - zSize
        if xRange <= 0 and yRange <= 0 and zRange <= 0:
            hitArea = 'sphBoxHit'
        else:
            hitArea = 'noHit'
    elif isinstance(obj1, sphere) and isinstance(obj2, sphere):
        objDistance = obj1.radius + obj2.radius
        if mag(obj1.pos - obj2.pos) < objDistance:
            hitArea = 'sphereHit'
        else:
            hitArea = 'noHit'
    else:
        hitArea = 'noHit'
    return hitArea

if __name__ == "__main__":
    scene.width = 1400
    scene.height = 700
    scene.title = 'Äppelspel'
    scene.range = 240
    scene.background = vec(0.1,0.1,0.1)

    quit= button(text='Avsluta', bind=quitProg, pos=scene.caption_anchor)

    fruit = sphere(pos=vec(0,-120,0), radius=13, color=vec(1,0,0))
    stick = cylinder(pos=fruit.pos+vec(0,13,0), axis=vec(0,1,0), radius=2, length=8, color=vec(0.6,0.3,0))
    leaf = ellipsoid(pos=fruit.pos+vec(10,20,0), axis=vec(1,0.3,0), size=vec(20,10,4), color=vec(0,1,0))
    eye_1 = sphere(pos=fruit.pos+vec(4,4,10), radius=2, color=vec(1,1,1))
    pupil_1 = sphere(pos=fruit.pos+vec(4,4,11.8), radius=0.5, color=vec(0,0,0))
    eye_2 = sphere(pos=fruit.pos+vec(-4,4,10), radius=2, color=vec(1,1,1))
    pupil_2 = sphere(pos=fruit.pos+vec(-4,4,11.8), radius=0.5, color=vec(0,0,0))

    apple = compound([fruit,stick,leaf,eye_1,pupil_1,eye_2,pupil_2])
    bb = getbbPosSize(apple.bounding_box())
    apple.bb = box(pos=bb[0], size=bb[1], color=vec(1,1,1), opacity=0.0)
    apple.vel = vec(0,0,0)

    wall_1 = box(pos=vec(0,-150,0), size=vec(300,10,30), color=vec(0,0,1))
    wall_2 = box(pos=vec(-250,-50,0), size=vec(200,10,30), color=vec(0,0,1))
    wall_3 = box(pos=vec(250,-50,0), size=vec(200,10,30), color=vec(0,0,1))
    wall_4 = box(pos=vec(0,50,0), size=vec(300,10,30), color=vec(0,0,1))
    walls = [wall_1, wall_2, wall_3, wall_4]

    pointBall = cylinder(pos=vec(0,70,0), axis=vec(0,30,0), radius=25, color=vec(0,1,0))
    bb = getbbPosSize(pointBall.bounding_box())
    pointBall.bb = box(pos=bb[0], size=bb[1], color=vec(1,1,1), opacity=0.0)

    pointLabel = label(pos=vec(-370,200,0), text='Points: 0', height=40, box = False, color = vec(1,0,0), font='sans')

    enemies = []
    enemyTime = 0.5
    t1 = clock()

    moveSpeed = 3
    vertJumpSpeed = 5
    horizJumpSpeed = 2
    gravitation = vec(0,-0.1,0)
    points = 0

    continue_loop = True
    while continue_loop:
        rate(60)
        k = keysdown()
        apple.vel += gravitation
        print(apple.vel)
        if clock() - t1 > enemyTime:
            t1 = clock()
            enemies.append(sphere(pos=vec(600-1200*random(),250,0), radius=8, color=vec(1,1,0)))
            enemies[-1].vel = vec(0.5-random(),2-4*random(),0) 
            if len(enemies) > 100:
                enemies.pop(0)
        hitPoint = detectCol(apple.bb, pointBall.bb)
        if hitPoint != 'noHit':
            points += 1
            pointLabel.text = 'Points: ' + str(points)
            if pointBall.pos.y == 70:
                pointBall.pos.y = -130            
            else: 
                pointBall.pos.y = 70
            pointBall.bb.pos.y =  pointBall.pos.y + pointBall.axis.y/2 
        for enemy in enemies:
            enemy.pos += enemy.vel
            hitArea = detectCol(enemy,apple.bb)
            if hitArea == 'sphBoxHit':
                text(text='GAME OVER', align='center', height = 40, color=color.green)
        for wall in walls:
            hitArea = detectCol(apple.bb, wall)
            if hitArea != 'noHit':
                if hitArea == 'above':
                    apple.vel = vec(0,0,0)
                    apple.pos.y = wall.pos.y + (wall.height + apple.height)/2.05
                    apple.bb.pos.y = apple.pos.y
                elif hitArea == 'below':
                    apple.vel.y = -apple.vel.y
                elif hitArea == 'left' or hitArea == 'right':
                    apple.vel.x = -apple.vel.x
                break
        if hitArea != 'above':
            apple.pos += apple.vel
            apple.bb.pos = apple.pos
        if apple.vel.y == 0:
            if  ' ' in k:
                apple.vel.y += vertJumpSpeed 
                apple.pos += apple.vel
                apple.bb.pos = apple.pos
                if 'right' in k:
                    apple.vel.x += horizJumpSpeed
                if 'left' in k:
                    apple.vel.x += -horizJumpSpeed
            if 'right' in k:
                apple.pos.x += moveSpeed
                apple.bb.pos.x += moveSpeed
            if 'left' in k:
                apple.pos.x += -moveSpeed
                apple.bb.pos.x += -moveSpeed
    
    os.kill(os.getpid(), signal.SIGTERM)
