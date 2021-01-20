import json
import shapely.geometry as geom
from shapely import ops
import matplotlib.pyplot as plt
import math
import rbfopt
import numpy as np
import sys

def place_outlets(studio, floors):
    # write me!

    studioList = make_studio(studio)    # list of polygons for each room, with index 0 being the whole studio
    wallList = split_studio(studioList)    # splits the whole studio into lines that represent the walls
    floorList = make_floors(floors)     # list of polygons for the pucks  

    seed_pts_master,seed_lengths_master = make_seed_pts(wallList)     # a matrix of 2D points/lengths for each wall
    seed_outlets_master = make_seed_outlets(seed_pts_master,studioList[0])   # a matrix of polygons for each wall
    betweenMasterList = count_intersections(seed_outlets_master,floorList) # a matrix of True or False that identifies which outlet has at least one intersection for each wall 
                                                                             
    #print(betweenMasterList)

    new_outlets_master = []
    for i in range(len(betweenMasterList)):     # for each wall
        new_outlets = []
        for j in range(len(betweenMasterList[i])):      # for each outlet on each wall
            if betweenMasterList[i][j] == False:        # if intersects
                outlet = optimize_outlet(seed_lengths_master[i][j],wallList[i],studioList[0],floorList)        # update the outlet
                print("original length: ")
                print(seed_lengths_master[i][j])
            else:
                outlet = seed_outlets_master[i][j]
            new_outlets.append(outlet)
        new_outlets_master.append(new_outlets)

    draw(wallList)
    draw(floorList)
    drawM(new_outlets_master)

    plt.show()

    # flatten the list of outlets
    outlets_poly = []
    for i in range(len(new_outlets_master)):
        for j in range(len(new_outlets_master[i])):
            outlets_poly.append(new_outlets_master[i][j])
    
    # make a dictionary so can be dumped into json file
    outlets = {}
    keys = range(len(outlets_poly))
    for i in keys:
        x,y = outlets_poly[i].boundary.coords.xy
        list  = []
        for j in range(len(x)):
            coord = [x[j],y[j]]
            list.append(coord)
        outlets[i] = list
    #print(outlets)

    return outlets

def make_seed_pts(walls):

    wall_lengths = []
    for w in walls:
        wall_lengths.append(w.length)
        #print(w.length)

    #seed_pts_master = []
    seed_pts_master = []
    seed_lengths_master = []
    max_allowed = 72    # 6 feet = 72 inches
    for i in range(len(wall_lengths)):      # for each wall
        seed_pts = []
        seed_lengths = []
        if wall_lengths[i] <= max_allowed*2:
            pt = walls[i].interpolate(0.5,True)
            seed_pts.append(pt)
            seed_lengths.append(round((0.5*wall_lengths[i])))      # divide by 12 to make label in feet
        else:          
            pt_start = walls[i].interpolate(max_allowed)     #6 feet is 72 inches
            seed_pts.append(pt_start)
            seed_lengths.append(6)
            pt_end = walls[i].interpolate(wall_lengths[i] - max_allowed)
            seed_lengths.append(round((wall_lengths[i] - max_allowed)))      # divide by 12 to make label in feet
            seed_pts.append(pt_end)
            gap = wall_lengths[i] - max_allowed*2
            if gap > 144:      # if the gap is more than 12 feet
                if (gap%144 == 0):      # gaps for multiples of 12 require one less seed point
                    intervals = (gap/144)-1
                else:
                    intervals = math.floor(gap/144)      # divide into intervals of max 12 feet
                for j in range(1,intervals+1):
                    pt_next = walls[i].interpolate(max_allowed+max_allowed*2*j) # the first 6ft plus 12ft distance times number of intervals
                    seed_pts.append(pt_next)             
                    seed_lengths.append(round((max_allowed+max_allowed*2*j)))        # divide by 12 to make label in feet
        seed_pts_master.append(seed_pts)
        seed_lengths_master.append(seed_lengths)    

    ## visualization:
    #for j in range(len(seed_pts)):
    #    x,y = seed_pts[j].xy
    #    plt.plot(x,y,'o')
    #    plt.annotate(str(seed_lengths[j]),(seed_pts[j].x,seed_pts[j].y))
    ##print(len(seed_pts))

    return seed_pts_master,seed_lengths_master     # matrix of 2D points/lengths for each wall

def make_seed_outlets(seed_pts_master,studio):

    seed_outlets_master = []    
    for i in range(len(seed_pts_master)):
        seed_outlets = []
        for j in range(len(seed_pts_master[i])):
            x = seed_pts_master[i][j].x
            y = seed_pts_master[i][j].y
            outletPoly = geom.Polygon([(x+2,y+2),(x+2,y-2),(x-2,y-2),(x-2,y+2)])
            segments = ops.split(outletPoly,studio.boundary)
            for s in segments:
                if studio.contains(s.centroid):
                    seed_outlets.append(s)
                    a,b = s.boundary.xy
                    #plt.plot(a,b)
                    #plt.annotate(str(j),(s.centroid.x,s.centroid.y))
        seed_outlets_master.append(seed_outlets)

    return seed_outlets_master

def count_intersections(seed_outlets_master,floorList):

    betweenMasterList = []
    for i in range(len(seed_outlets_master)):  # for each outlet
        betweenList = []
        for j in range(len(seed_outlets_master[i])):
            in_between = True
            for k in range(len(floorList)):
                if seed_outlets_master[i][j].intersects(floorList[k]):
                    in_between = False
                    break
            betweenList.append(in_between)
        betweenMasterList.append(betweenList)
    #print(boolList)
   
    return betweenMasterList  # boolList is a list of True or False that identifies which outlet has at least one intersection; falseCount is how many of the outlets have intersections

class Wrapper:
    # constructor method where you can pass arguments that the other methods will be able to access
    def __init__(self,wall,studio,floors,seed_length):
        self.wall = wall
        self.studio = studio
        self.floors = floors
        self.seed_length = seed_length

    # the method with only one argument (new_length) and calls the original function that needs additional arguments
    def obj_function_for_rbfopt(self,new_length):
        return obj_funct(new_length,self.wall,self.studio,self.floors,self.seed_length)

def obj_funct(new_length,wall,studio,floors,seed_length):
 
    new_outlet = make_new_outlet(new_length[0],wall,studio)     # new_length is an array that comes from the optimizer

    difference = abs(new_length[0]-seed_length)

    # check for intersections
    for i in range(len(floors)):
        if new_outlet.intersects(floors[i]):
            in_between = 1
            break
        else:
            in_between = 0
   
    #add_to_new_list_of_outlets
    #count_intersections(all the outlets for this wall)

    return in_between+difference*.01

def make_new_outlet(length,wall,studio):

    # make the new outlet
    new_pt = wall.interpolate(length)
    x = new_pt.x
    y = new_pt.y
    newPoly = geom.Polygon([(x+2,y+2),(x+2,y-2),(x-2,y-2),(x-2,y+2)])
    segments = ops.split(newPoly,studio.boundary)
    for s in segments:
        if studio.contains(s.centroid):
            outlet = s
    return outlet

def optimize_outlet(seed_length,wall,studio,floors):
    
    #testing numpy array making:
    #b = np.array([2])
    #print(b[0])

    A = Wrapper(wall,studio,floors,seed_length)
    bb = rbfopt.RbfoptUserBlackBox(1,np.array([seed_length-8]),np.array([seed_length+8]),np.array(['I']),A.obj_function_for_rbfopt)
    settings = rbfopt.RbfoptSettings(max_iterations=20,max_evaluations=20,minlp_solver_path='C:/Users/sgupt/source/repos/bonmin-win64/bonmin.exe',nlp_solver_path='C:/Users/sgupt/source/repos/ipopt-win64/ipopt.exe')
    alg = rbfopt.RbfoptAlgorithm(settings,bb)
    #alg.set_output_stream(open('nul','w'))
    objval,x,itercount,evalcount,fast_evalcount = alg.optimize()
    print(objval)
    print(x[0])
  
    return make_new_outlet(x[0],wall,studio)

##################### RBFOpt example start

#class Wrapper:
#    # constructor method where you can pass arguments that the other methods will be able to access
#    def __init__(self,extra):
#        self.arg=extra

#    # the method with only one argument (x) and calls the original function that needs additional arguments
#    def obj_function_for_rbfopt(self,x):
#        return obj_funct(x,self.arg)

#def obj_funct(x,extra):
#    return x[0]*x[1]-x[2]+extra

#def optimize(extra):
#    A = Wrapper(extra)
#    bb = rbfopt.RbfoptUserBlackBox(3,np.array([0]*3),np.array([10]*3),np.array(['r','r','r']),A.obj_function_for_rbfopt)
#    settings = rbfopt.RbfoptSettings(max_evaluations=50,minlp_solver_path='c:/users/sgupt/source/repos/bonmin-win64/bonmin.exe',nlp_solver_path='c:/users/sgupt/source/repos/ipopt-win64/ipopt.exe')
#    alg = rbfopt.RbfoptAlgorithm(settings,bb)
#    alg.set_output_stream(open('nul','w'))
#    objval,x,itercount,evalcount,fast_evalcount = alg.optimize()
#    print(objval)
#    print(x)
#    return

##################### RBFOpt example end


def main():
    # room info
    studio = "json/studio_info.json"
    with open(studio) as json_file:
        studio = json.load(json_file)

    # floor info
    floors = "json/floor_info.json"
    with open(floors) as json_file:
        floors = json.load(json_file)

    outlets = place_outlets(studio, floors)
    with open('outlets.json', 'w') as json_out:
        json.dump(outlets, json_out)


def draw(list):
    for l in list:
        if l.type == 'Polygon':
            x,y = l.boundary.xy     #.exterior
        else:
            x,y = l.xy
        plt.plot(x,y)
    
    return

def drawM(matrix):
    for i in range(len(matrix)):
        for l in matrix[i]:
            if l.type == 'Polygon':
                x,y = l.boundary.xy     #.exterior
            else:
                x,y = l.xy
            plt.plot(x,y)
    return


def make_studio(studio):
    
    doors_index = -1
    count = -1

    # parse json data into point lists
    pointList = []
    for key, value in studio.items():   # studio is a dict where key is the name of the room and the value is an unflattened list of coordinates
        count += 1
        if key == 'doors':      # identify which index consists of the coordinates for doors
            doors_index = count
        pointList.append(value)     # adds unflattened coordinates to pointList

    # make polygons
    polyList = []
    for i in range(len(pointList)):   # for every unflattened list (one for each kind of room)
        flattened = [val for sublist in pointList[i] for val in sublist]    # flatten the coordinate point list       
        if i == doors_index:     # breaks up the door coordinates list into groups of 4 to avoid the single messy polygon
            for j in range(0,len(flattened),4):
               flat = flattened[j:j+4]
               polygon = geom.Polygon(flat) 
               polyList.append(polygon)              
        else:
            polygon = geom.Polygon(flattened) 
            polyList.append(polygon)   

    return polyList     # list of polygons for each room


def make_floors(floors):

    # parse json data into points
    pointList = []
    for key, value in floors.items():   # studio is a dict where key is the name of the room and the value is an unflattened list of coordinates
        if key == 'pucks':
            pointList.append(value)     # adds unflattened coordinates to pointList

    # make polygons
    polyList = []
    for i in range(len(pointList)):   # for every unflattened list (one for each kind of room)
        flattened = [val for sublist in pointList[i] for val in sublist]    # flatten the coordinate point list      
        for j in range(0,len(flattened),5):
            flat = flattened[j:j+4]
            polygon = geom.Polygon(flat) 
            polyList.append(polygon)   

    return polyList
   

def split_studio(polyList):

    total_wall = polyList[0].boundary

    # make the vertices from the rooms into Shapely Points
    pts = []
    for i in range(1,len(polyList)):      
        vertices = polyList[i].boundary.coords
        for v in vertices:
            pt = geom.Point(v)
            pts.append(pt)         

    # filter the Points by distance to the border of the main wall
    border_pts = []
    for p in pts:
        dist = p.distance(total_wall)
        if dist<(1e-3):
            border_pts.append(p)

    # filter the Points by being along a wall (rather than at a corner)
    opening_pts = []
    for b in border_pts:
        count = 0
        first_vertices = total_wall.coords
        vertices = []
        for f in first_vertices:
            vertices.append(geom.Point(f))
        for v in vertices:
            if b.distance(v)<(1e-3):
                count = count+1
        if count == 0:
            opening_pts.append(b)

    # get the length parameter of the Points along the main wall
    values = []
    for o in opening_pts:
        val = total_wall.project(o)
        values.append(val)

    # sort the length parameters and the Points by association
    values,opening_pts = zip(*sorted(zip(values,opening_pts)))

    ## some data visualization
    #for i in range(len(opening_pts)):
    #    vertex_x,vertex_y = opening_pts[i].xy
    #    plt.plot(vertex_x,vertex_y,'o')
    #    rounded = round(values[i])
    #    plt.annotate(str(rounded),(opening_pts[i].x,opening_pts[i].y))
    #    #x,y = polyList[0].boundary.xy       
    #    #plt.plot(x,y)    

    # make the segments from the main wall
    subs = []
    for i in range(len(values)):
        if i == (len(values)-1):
            sub_1 = ops.substring(total_wall,values[i],total_wall.length)
            sub_2 = ops.substring(total_wall,0,values[0])
            multi = geom.MultiLineString([sub_1,sub_2])
            sub = ops.linemerge(multi)
        else:
            sub = ops.substring(total_wall,values[i],values[i+1])
        subs.append(sub)

    # remove the Points
    lines = []
    for i in range(len(subs)):
        if subs[i].type == 'LineString':
            lines.append(subs[i])

    # remove the short walls
    walls = []
    for i in range(1,len(lines),2):
        if (lines[i].length)>24:
            walls.append(lines[i])

    plt.show()

    return walls



if __name__ == "__main__":
    main()
