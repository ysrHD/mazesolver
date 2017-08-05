from PIL import Image, ImageDraw
import numpy
import PIL
import time

################################################################
## HOW TO USE:
## - The file must be in a .png format
## - The maze wall must be in gray-scale
## - The file must be in the same directory as this program
## - The starting point must be a valid point (not a wall)
## - The finishing point must be a valid point (not a wall)
## - The maze must be solvable
##
## INPUT EXAMPLE:
## bebek
## 250,523
## 430,48
##
################################################################

filename = input("What's the file name? ")
start = ','.join((input("Starting point? (in format X,Y) ")).split(',')[::-1])
fin = ','.join((input("Finishing point? (In format X,Y) ")).split(',')[::-1])

img = PIL.Image.open(filename+".png").convert('L')
imgarr = numpy.array(img)
starttime = time.time()

def keyy(i,j):
    return str(i)+','+str(j)
print ('. . . . . . . . . . . . . . . . .')
print ('Reading',filename+'.png . . .')

graph = {}
for i in range(len(imgarr)):
    for j in range(len(imgarr[i])):
        graph[keyy(i,j)]=[]
        if imgarr[i][j]!=0:
            if i+1<len(imgarr): # right     q
                if imgarr[i+1][j] ==255:
                    graph[keyy(i,j)] += [[keyy(i+1,j),1]]
            if j+1<len(imgarr[0]): # down
                if imgarr[i][j+1] ==255:
                    graph[keyy(i,j)]+= [[keyy(i,j+1),1]]
            if j>0: # up
                if imgarr[i][j-1] ==255:
                    graph[keyy(i,j)]+= [[keyy(i,j-1),1]]
            if i>0: # left
                if imgarr[i-1][j] ==255:
                    graph[keyy(i,j)] += [[keyy(i-1,j),1]]
            if i+1<len(imgarr) and j+1<len(imgarr[0]): # right down
                if imgarr[i+1][j+1] ==255:
                    graph[keyy(i,j)] += [[keyy(i+1,j+1),(2**0.5)]]
            if i > 0 and j>0:  # left up
                if imgarr[i - 1][j-1] == 255:
                    graph[keyy(i, j)] += [[keyy(i - 1, j-1), (2**0.5)]]
            if i+1<len(imgarr) and j > 0:  # right up
                if imgarr[i + 1][j - 1] == 255:
                    graph[keyy(i, j)] += [[keyy(i + 1, j - 1), (2 ** 0.5)]]
            if j+1<len(imgarr[0]) and i > 0: # down left
                if imgarr[i-1][j+1] ==255:
                    graph[keyy(i,j)]+= [[keyy(i-1,j+1),(2 ** 0.5)]]

def dijkstraa(graph, start, fin):
    dist = {}
    q = [] # queue
    processsd = {}
    parents = {}
    for k in graph:
        dist[k] = float('inf')
        processsd[k] = False
    dist[start] = 0
    q+=[[0,start]]
    while q!=[]:
        a = q[0][1]
        q.pop(0)
        if processsd[a]: continue
        processsd[a]  =True
        for u in graph[a]:
            b = u[0]
            w = u[1]
            if (dist[a]+w < dist[b]):
                dist[b] = dist[a]+w
                q+=[[dist[b],b]]
                parents[b] = a

    def findpathto(tofind):
        cur = tofind
        path = [cur]
        while parents[cur] != tofind and parents[cur] in parents:
            cur = parents[cur]
            path += [cur]
        return path[::-1]
    return findpathto(fin)#,dist[fin]

print ('Solving the maze . . .')
sol = (dijkstraa(graph,start,fin))
print ('Drawing the path . . .')
finsol = []
img = PIL.Image.open(filename+".png").convert("L")
imgarr = numpy.array(img)
im = Image.open(filename+".png")
draw = ImageDraw.Draw(im)
for i in sol:
    tmp = i.split(',')
    finsol +=[[int(tmp[0]),int(tmp[1])]]
    imgarr[int(tmp[0])][int(tmp[1])] = 140
    draw.point((int(tmp[1]), int(tmp[0])), fill=(54,39,248))
im.save(filename+"outfileeenew.png")
del draw
print ('Finished in', (round(time.time() - starttime, 2)), 'seconds!')
im.show()
print ('. . . . . . . . . . . . . . . . .')