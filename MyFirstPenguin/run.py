import os
import json
import random
import math
from pickletools import dis
from math import sqrt
from nt import close

ROTATE_LEFT = "rotate-left"
ROTATE_RIGHT = "rotate-right"
ADVANCE = "advance"
RETREAT = "retreat"
SHOOT = "shoot"
PASS = "pass"

MOVE_UP =  {"top" : ADVANCE, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
MOVE_DOWN =  {"top" : ROTATE_LEFT, "bottom" : ADVANCE, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
MOVE_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : ADVANCE ,"left" : ROTATE_LEFT }
MOVE_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : ADVANCE }

SHOOT_UP =  {"top" : SHOOT, "bottom" : ROTATE_LEFT, "right" : ROTATE_LEFT ,"left" : ROTATE_RIGHT }
SHOOT_DOWN =  {"top" : ROTATE_LEFT, "bottom" : SHOOT, "right" : ROTATE_RIGHT ,"left" : ROTATE_LEFT }
SHOOT_RIGHT = {"top" : ROTATE_RIGHT, "bottom" : ROTATE_LEFT, "right" : SHOOT ,"left" : ROTATE_LEFT }
SHOOT_LEFT = {"top" : ROTATE_LEFT, "bottom" : ROTATE_RIGHT, "right" : ROTATE_RIGHT,"left" : SHOOT }


def calcDistance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

def MoveToClosest(body, tiles):
    
    
    if len(tiles) == 0:
        return None
    
    
    closest = tiles.pop()
    
    if closest["type"] == "jquery" and len(tiles) != 0:
        closest = tiles.pop()    

    if closest["type"] == "jquery":
        return None
    
    
    
    closest_dist = calcDistance(body["you"], closest)


    for powerUp in tiles:
        
        if closest["type"] == "jquery":
            continue
        
        dist = calcDistance(body["you"], powerUp)
        
        if dist < closest_dist:
            closest_dist = dist
            closest = powerUp
        
    return moveTowardsPoint(body, closest["x"], closest["y"])    

def findPowerUp(body):
    return MoveToClosest(body, body["bonusTiles"])
    
        
    
    
def moveTowardsPoint(body, pointX, pointY):
    penguinPositionX = body["you"]["x"]
    penguinPositionY = body["you"]["y"]
    plannedAction = PASS
    bodyDirection = body["you"]["direction"]

    if penguinPositionX < pointX:
        plannedAction = MOVE_RIGHT[bodyDirection]
    elif penguinPositionX > pointX:
        plannedAction = MOVE_LEFT[bodyDirection]
    elif penguinPositionY < pointY:
        plannedAction = MOVE_DOWN[bodyDirection]
    elif penguinPositionY > pointY:
        plannedAction = MOVE_UP[bodyDirection]
        

    if plannedAction == ADVANCE and wallInFrontOfPenguin(body):
        plannedAction = SHOOT
                
    return plannedAction

def wallInFrontOfPenguin(body):
    xValueToCheckForWall = body["you"]["x"]
    yValueToCheckForWall = body["you"]["y"]
    bodyDirection = body["you"]["direction"]

    if bodyDirection == "top":
        yValueToCheckForWall -= 1
    elif bodyDirection == "bottom":
        yValueToCheckForWall += 1
    elif bodyDirection == "left":
        xValueToCheckForWall -= 1
    elif bodyDirection == "right":
        xValueToCheckForWall += 1
    return doesCellContainWall(body["walls"], xValueToCheckForWall, yValueToCheckForWall)

def doesCellContainWall(walls, x, y):
    for wall in walls:
        if wall["x"] == x and wall["y"] == y:
            return True
    return False

def fireInRange(body):
    
    bodyX = body["you"]["x"]
    bodyY = body["you"]["y"]
    

    newPos = {"x" : bodyX, "y" : bodyY}
    
    
    closest_dist = 100

    fires = body["fire"]

    if len(fires) == 0:
        return None

    move = None

    for fire in fires:
        if abs(fire["x"] - bodyX) <= abs(fire["y"] - bodyY) and abs(closest_dist) > abs(fire["x"] - bodyX):
            if fire["x"] - bodyX < 0:
                move = MOVE_RIGHT[body["you"]["direction"]]
            else:
                move = MOVE_LEFT[body["you"]["direction"]]
            closest_dist = fire["x"] - bodyX
        
        if abs(fire["x"] - bodyX) >= abs(fire["y"] - bodyY) and abs(closest_dist) > abs(fire["y"] - bodyY):
            if fire["y"] - bodyY < 0:
                move = MOVE_DOWN[body["you"]["direction"]]
            else:
                move = MOVE_UP[body["you"]["direction"]]
            closest_dist = fire["y"] - bodyY

        
    return move
        

def enemiesInRange(body):
    you = body["you"]
    enemy = body["enemies"][0]
    
    return SHOOT
    
    if(abs(you["x"]-enemy["x"]) < abs(you["y"]-enemy["y"])):
        if(you["y"]-enemy["y"] < 0):
            return SHOOT_DOWN[body["you"]["direction"]]
        else:
            return SHOOT_UP[body["you"]["direction"]]
    else:
        if(you["x"]-enemy["x"] < 0):
            return SHOOT_RIGHT[body["you"]["direction"]]
        else:
            return SHOOT_LEFT[body["you"]["direction"]]
    
    return SHOOT

def shootInRange(body):
    plannedAction = "pass"
    me = body['you']
    bodyDirection = body["you"]["direction"]
    
    meX = me['x']
    meY = me['y']
    for enemy in body["enemies"]:
        enemyX = enemy['x']
        enemyY = enemy['y']

        xLengde = abs(enemyX - meX)
        yLengde = abs(enemyY - meY)
        if xLengde <= yLengde:
            # Hvis x lengden er kortere
            if meY < enemyY:
                #Rotate top
                return SHOOT_DOWN[bodyDirection]
            else:
                return SHOOT_UP[bodyDirection]
        else:
            if meX <= enemyX:
                return SHOOT_RIGHT[bodyDirection]
            else:
                return SHOOT_LEFT[bodyDirection]
    return PASS

def nothinToDo(body):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)

def chooseAction(body):
    if(len(body["fire"]) != 0):
        move = fireInRange(body)
    elif(len(body["enemies"][0]) > 1 and calcDistance(body["enemies"][0], body["you"]) <= body["you"]["weaponRange"]):
        move = shootInRange(body)
    else:
        move = findPowerUp(body)

    
    if move is None:
        move =  nothinToDo(body)
    
    if move == PASS:
        move = SHOOT
        
    return move

env = os.environ
req_params_query = env['REQ_PARAMS_QUERY']
responseBody = open(env['res'], 'w')

response = {}
returnObject = {}
if req_params_query == "info":
    returnObject["name"] = "Agent Pee"
    returnObject["team"] = "Willy"
elif req_params_query == "command":    
    body = json.loads(open(env["req"], "r").read())
    returnObject["command"] = chooseAction(body)

response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()