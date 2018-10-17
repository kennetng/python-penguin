import os
import json
import random
import math
from pickletools import dis
from math import sqrt

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


def calcDistance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

def MoveToClosest(body, tiles):
    
    if len(tiles) == 0:
        return None
    
    
    closest = tiles.pop()
    
    
    closest_dist = calcDistance(body["you"], closest)


    for powerUp in tiles:

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
    move = moveTowardsPoint(body, pointX, pointY)
    
    
    if move is MOVE_DOWN:
        return MOVE_UP
    if move is MOVE_UP:
        return MOVE_DOWN
    if move is MOVE_LEFT:
        return MOVE_RIGHT
    if move is MOVE_LEFT:
        return MOVE_RIGHT
    
    

def nothinToDo(body):
    return PASS

def chooseAction(body):
    if(len(body["fire"]) != 0):
        move = fireInRange(body)
    else:
        move = findPowerUp(body)
    
    if move is None:
        return nothinToDo(body)
        
    return move

env = os.environ
req_params_query = env['REQ_PARAMS_QUERY']
responseBody = open(env['res'], 'w')

response = {}
returnObject = {}
if req_params_query == "info":
    returnObject["name"] = "Pingu"
    returnObject["team"] = "Team Python"
elif req_params_query == "command":    
    body = json.loads(open(env["req"], "r").read())
    returnObject["command"] = chooseAction(body)

response["body"] = returnObject
responseBody.write(json.dumps(response))
responseBody.close()