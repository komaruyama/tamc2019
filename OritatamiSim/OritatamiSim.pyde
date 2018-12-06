add_library('pdf')
add_library('svg')
#import svg

import time

input = ""

cam = 0.0
defaultCam = 0.0
zoom = 1.0

drag = [0,0]

select = [0,0,0,0]
highlight = False

firstSelected = False

toSVG = False

path = []
confo = dict({})
bonds = []

unit = 80

gridBorder = 1


beadTypes = []

tColor = color(0, 0, 255)
bContour = [color(0, 0, 0), color(0, 0, 0), color(0, 0, 0), color(0, 0, 0), color(0,0,0)]
bFill = [color(255, 255, 255), color(255, 255, 255), color(255, 255, 255), color(255, 255, 255), color(255,255,255)]
bName = ["0", "1", "2", "3", "4"]
bondColor = color(255, 0, 0)




def setup():
    global cam, defaultCam, path, confo, beadTypes, bonds
    
    size(1200,400)
    frameRate(30)
    defaultCam = (height/2.0) / tan(PI*30.0 / 180.0)
    cam = defaultCam
    
#    for i in range(0,10,2):
#        confo.update({(i+0,0):1})
#        path.append((i+0,0))
#        confo.update({(i+0,1):3})
#        path.append((i+0,1))
#        confo.update({(i+1,1):0})
#        path.append((i+1,1))
#        confo.update({(i+1,0):2})
#        path.append((i+1,0))
#    
    path.append([0,0])
    confo.update({(0, 0): 1})
    
    if input != "":
        f = open(input, "r")
        path = []
        confo = {}
        tmp = f.readline().strip().split("=>")
        for i in tmp:
            tmp2 = i.split(",")
            path.append([int(tmp2[0]),int(tmp2[1])])
            confo.update({(int(tmp2[0]),int(tmp2[1])):int(tmp2[2])})
        
        tmp = f.readline().strip().split("=")
        for i in tmp:
            tmp2 = i.split(",")
            bonds.append([int(tmp2[0]),int(tmp2[1]), int(tmp2[2]), int(tmp2[3])])
            
        f.close()
    
    beadTypes = list(set(confo.values()))
    
    print(beadTypes)
    
    #size(800, 400,PDF,"test1.pdf")
      
      
      
def draw():
    #noStroke()
    global zoom, r, highlight, toSVG 
    clear()
    background(255)
    
    if toSVG:
        beginRecord(SVG, "output.svg")
    
    highlight = False
    #translate(mouseX, mouseY)
    
    
    zoom = cam/defaultCam
    r = zoom*unit*0.2
    
    #drawGrid()
    #drawSmallGrid()
    drawSurroundGrid()
     
   
   
    for i in range(len(path)-1):
        drawTranscript(path[i][0], path[i][1], path[i+1][0], path[i+1][1])
    
    # for i in range(0,len(path),4):
    #     drawBond(path[i][0]+0, path[i][1]+0, path[i][0]+1, path[i][1]+1)
    #     drawBond(path[i][0]+0, path[i][1]+0, path[i][0]+1, path[i][1]+0)
    
    for i in bonds:
         drawBond(i[0], i[1], i[2], i[3])
            
    for i in path:
        drawBead(i[0], i[1], confo[(i[0],i[1])])
    #if firstSelected:
        #drawBead(last[0], last[1], len(beadTypes))
    
   
    if highlight:
        stroke(color(255, 0, 0))
        fill(color(0,0,0,100))
        ellipse(select[0],select[1], r*1.2, r*1.2)
        
    if toSVG:
        saveConfo(path, confo)
        endRecord()
        toSVG = False
    #exit()
      
   

def mouseDragged():
    global drag
    drag = [drag[0]+mouseX-pmouseX, drag[1]+mouseY-pmouseY]
                  
                                                      
                                                
def mouseClicked():
    global path, confo, toSVG, firstSelected, bonds, last
    if key == 'p':
        toSVG = True
    print(key)
    if highlight:
        if mouseButton == RIGHT:
            if firstSelected:
                firstSelected = False
                bonds.append(last+select[2:])
            else:
                last = select[2:]
                firstSelected = True
        else:
            if (select[2],select[3]) in confo:
                last = select[2:]
                firstSelected = True
            elif int(key) in range(len(bContour)):
                path.append([select[2],select[3]])
                confo.update({(select[2],select[3]):int(key)})
                last = select[2:]
        
    
     
       
def mouseWheel(event):
    global cam
    print(cam)
    e = event.getCount()   
    cam += 5*e
   
    
     
       
def drawBead(x, y, type):
    pushMatrix()
    
    translate(drag[0]+width/2, drag[1]+height/2)
    shearX(PI/6.0)
    scale(zoom)
    scale(unit*1, -unit*sqrt(3)/2)
    
    rx = screenX(x, y)
    ry = screenY(x, y)
    
    popMatrix()
    
    
    strokeWeight(zoom*unit/30.0)
    stroke(bContour[type])
    fill(bFill[type])
    
    
    # if rx-r<mouseX and mouseX<rx+r  and  ry-r<mouseY and mouseY<ry+r:
    #     stroke(color(255, 0, 0))
    #     fill(color(0,0,0,175))
         
    ellipseMode(RADIUS)
    ellipse(rx, ry, 0.2*zoom*unit, 0.2*zoom*unit)
    
    #textFont(loadFont("Utopia-Bold-48.vlw"))
    textAlign(CENTER, CENTER)
    textSize(zoom*unit*0.2)
    fill(0)
    text(bName[type], rx, ry)
    
    
    
    
    
def drawTranscript(x0, y0, x1, y1):
    pushMatrix()
    
    translate(drag[0]+width/2, drag[1]+height/2)
    shearX(PI/6.0)
    scale(zoom)
    scale(unit*1, -unit*sqrt(3)/2)
    
    rx0 = screenX(x0, y0)
    ry0 = screenY(x0, y0)
    rx1 = screenX(x1, y1)
    ry1 = screenY(x1, y1)
    popMatrix()
    
    stroke(tColor)
    strokeWeight(zoom*unit/10.0)
    line(rx0, ry0, rx1, ry1)
    
    
    
    
def drawBond(x0, y0, x1, y1):
    pushMatrix()
    
    translate(drag[0]+width/2, drag[1]+height/2)
    shearX(PI/6.0)
    scale(zoom)
    scale(unit*1, -unit*sqrt(3)/2)
    
    rx0 = screenX(x0, y0)
    ry0 = screenY(x0, y0)
    rx1 = screenX(x1, y1)
    ry1 = screenY(x1, y1)
    popMatrix()
    
    stroke(bondColor)
    strokeWeight(zoom*unit/12.0)
    
    line(lerp(rx0, rx1, 0.25), lerp(ry0, ry1, 0.25), lerp(rx0, rx1, 0.33), lerp(ry0, ry1, 0.33))
    line(lerp(rx0, rx1, 0.48), lerp(ry0, ry1, 0.48), lerp(rx0, rx1, 0.56), lerp(ry0, ry1, 0.56))
    line(lerp(rx0, rx1, 0.71), lerp(ry0, ry1, 0.71), lerp(rx0, rx1, 0.8), lerp(ry0, ry1, 0.8))
    
    

def drawSurroundGrid():
    global highlight, select
    
    pushMatrix()
    translate(drag[0]+width/2, drag[1]+height/2)
    shearX(PI/6.0)
    scale(zoom)
    scale(unit*1, -unit*sqrt(3)/2)
    
    highlight = False
    
    gridPoints = []
    for i in path:
        for j in range(-gridBorder, gridBorder+1):
            for k in range(-gridBorder, gridBorder+1):
                tx = screenX(i[0]+j, i[1]+k)
                ty = screenY(i[0]+j, i[1]+k)
                if [tx, ty] not in gridPoints:
                    gridPoints.append([tx, ty])
                if tx-r<mouseX and mouseX<tx+r and ty-r<mouseY and mouseY<ty+r:
                    select = [tx, ty, i[0]+j, i[1]+k]
                    highlight = True
                #gridPoints.append([screenX(-i, -j), screenY(-i, -j)])
    popMatrix()
    
    stroke(0)
    strokeWeight(1)
    fill(0)
    for p in gridPoints:
        ellipse(p[0], p[1],2,2)    
        
                    
    
def drawSmallGrid():
    global highlight, select
    X = [min([i[0] for i in path])-gridBorder, max([i[0] for i in path])+gridBorder] 
    Y = [min([i[1] for i in path])-gridBorder, max([i[1] for i in path])+gridBorder]
    
    pushMatrix()
    translate(drag[0]+width/2, drag[1]+height/2)
    shearX(PI/6.0)
    scale(zoom)
    scale(unit*1, -unit*sqrt(3)/2)
    
    highlight = False
    
    gridPoints = []
    for i in range(X[0], X[1]+1):
        for j in range(Y[0], Y[1]+1):
            tx = screenX(i, j)
            ty = screenY(i, j)
            gridPoints.append([tx, ty])
            if tx-r<mouseX and mouseX<tx+r and ty-r<mouseY and mouseY<ty+r:
                select = [tx, ty, i, j]
                highlight = True
            #gridPoints.append([screenX(-i, -j), screenY(-i, -j)])
    popMatrix()
    stroke(0)
    strokeWeight(1)
    fill(0)
    for p in gridPoints:
        ellipse(p[0], p[1],2,2)



def drawGrid():
    global highlight, select
    X = int(2*width/(unit*1.0*zoom)) 
    Y = int(2*height/(unit*1.0*zoom))
    
    pushMatrix()
    translate(drag[0]+width/2, drag[1]+height/2)
    shearX(PI/6.0)
    scale(zoom)
    scale(unit*1, -unit*sqrt(3)/2)
    
    highlight = False
    
    gridPoints = []
    for i in range(-X/2, X/2):
        for j in range(-Y/2, Y/2):
            tx = screenX(i, j)
            ty = screenY(i, j)
            gridPoints.append([tx, ty])
            if tx-r<mouseX and mouseX<tx+r and ty-r<mouseY and mouseY<ty+r:
                select = [tx, ty, i, j]
                highlight = True
            #gridPoints.append([screenX(-i, -j), screenY(-i, -j)])
    popMatrix()
    stroke(0)
    strokeWeight(1)
    fill(0)
    for p in gridPoints:
        ellipse(p[0], p[1],2,2)
        
        
def saveConfo(path, confo):
    l = time.localtime(time.time())
    f = open("out"+str(l.tm_year)+str(l.tm_mon)+ str(l.tm_mday)+str(l.tm_hour)+str(l.tm_min)+".oriconf", 'w')
    
    for i in path[:-1]:
        f.write(str(i[0])+","+ str(i[1])+","+str(confo[(i[0],i[1])])+ "=>")
    i = path[-1]
    f.write(str(i[0])+","+ str(i[1])+","+str(confo[(i[0],i[1])])+"\n")
    f.close()
