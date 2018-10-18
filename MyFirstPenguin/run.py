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
    
    bodyX = body["you"]["x"]
    bodyY = body["you"]["y"]
    

    newPos = {"x" : bodyX, "y" : bodyY}
    
    
    closest_dist = 100

    fires = body["fire"]

    if len(fires) == 0:
        return None
        

    for fire in fires:
        if abs(fire["x"] - bodyX) <= abs(fire["y"] - bodyY) and abs(closest_dist) > abs(fire["x"] - bodyX):
            closest_dir = "x"
            closest_dist = fire["x"] - bodyX
        
        if abs(fire["x"] - bodyX) >= abs(fire["y"] - bodyY) and abs(closest_dist) > abs(fire["y"] - bodyY):
            closest_dir = "y"
            closest_dist = fire["y"] - bodyY
        
        
    newPos[closest_dir] = newPos[closest_dir] + closest_dist

    return moveTowardsPoint(body, newPos["x"], newPos["y"])
"""
# This method tries to place him in the correct position to shoot the enemy
def shootInRange(body):
    plannedAction = "pass"
    me = body['you']
    if body["enemies"]:
        for enemy in body["enemies"]:
            if enemy["x"] == me['x']:
                plannedAction = rotateX(me, enemy)
                if plannedAction == "CORRECT":
                    # TODO Calculate dmg
                    return SHOOT
            elif enemy['y'] == me['y']:
                plannedAction = rotateY(me, enemy)
                if plannedAction == "CORRECT":
                    # TODO Calculate dmg
                    return SHOOT
            else:
                plannedAction = stalkEnemy(me, enemy)
    return plannedAction


# Vurderer hvilken som er kortest vei til å komme i samme linje som agenten
def stalkEnemy(me, enemy):
    enemyX = enemy['x']
    enemyY = enemy['y']
    meX = me['x']
    meY = me['y']

    xLengde = abs(enemyX - meX)
    yLengde = abs(enemyY - meY)

    if xLengde <= yLengde:
        if meX < enemyX:
            return moveTowardsPoint(body, meX + 1, meY)
        else:
            return moveTowardsPoint(body, meX - 1, meY)
    else:
        if meY < enemyY:
            return moveTowardsPoint(body, meX, meY + 1)
        else:
            return moveTowardsPoint(body, meX, meY - 1)


def calculateDmg(me, enemy):
    enemyHP = enemy["strength"] / me['weaponDamage']
    myHP = me["strength"] / enemy['weaponDamage']
    if enemyHP > myHP:
        return RETREAT
    else:
        return SHOOT


# Hvis fienden er i samme Y linje, roter i riktig direksjon
def rotateY(me, enemy):
    if me['x'] < enemy['x'] and me['direction'] != 'right':
        return MOVE_RIGHT
    elif me['x'] > enemy['x'] and me['direction'] != 'left':
        return MOVE_LEFT
    else:
        return "CORRECT"


# Hvis fienden er i samme X linje, roter i riktig direksjon
def rotateX(me, enemy):
    if me['y'] < enemy['y'] and me['direction'] != 'top':
        return MOVE_UP
    elif me['y'] > enemy['y'] and me['direction'] != 'bottom':
        return MOVE_DOWN
    else:
        return 'CORRECT'
"""    

def nothinToDo(body):
    centerPointX = math.floor(body["mapWidth"] / 2)
    centerPointY = math.floor(body["mapHeight"] / 2)
    return moveTowardsPoint(body, centerPointX, centerPointY)

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