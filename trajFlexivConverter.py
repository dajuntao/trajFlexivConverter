import os
import numpy as np
from string import Template

# read raw waypoints text data
def fileReader(dir, filename, header):
    wpArray = []

    fileDir = os.path.join(os.getcwd(), dir, filename)
    ln = 0
    with open(fileDir, 'r') as file:
        for line in file:
            if header != True and ln != 0:
                wpArray.append(line)
            ln += 1

    return wpArray


# use a trajectory template file to convert text waypoints into a traj file
def trajConvertor(dir, filename, filetype, defaultInput, header, factor, rot):
    wpArray = fileReader(dir, filename+"."+filetype, header)
    trajFileName = filename + "_trajFlexiv.traj"

    wp_num = 0
    for line in wpArray:
        pos = line.split(',')

        # apply each waypoint to the Flexiv trajectory format
        with open('traj_v2.traj', 'r') as temp:
            src = Template(temp.read())
            wpFormated = src.substitute(defaultInput, patternName=wp_num, x=float(pos[0])/factor, y=float(pos[1])/factor, z=float(pos[2])/factor, rx=float(pos[3])*rot, ry=float(pos[4])*rot, rz=float(pos[5].replace('\n',''))*rot)
            fileWrite(wpFormated, trajFileName,wp_num)

        wp_num += 1
    
    print("Trajectory file successfully generated under directory: \\" + dir + "\\" + trajFileName)


# write out each converted waypoint
def fileWrite(wpFormated, trajFileName, wp_num):
    outputFileDir = os.path.join(os.getcwd(), dir, trajFileName)
    if wp_num == 0:
        file = open(outputFileDir, 'w')
        file.write("traj_coord_type: \"\"" + "\n")
        file.write("traj_coord_ref: \"\"" + "\n")
    else:
        file = open(outputFileDir, 'a')
    file.write(wpFormated + "\n")
    file.close()


if __name__ == "__main__":
    dir = input("Waypoints File Directory: ")               # file directory
    filename = input("Waypoints File Name: ")               # file name w/o extension
    filetype = input("Waypoints File Type: ")               # text file extension
    factor = float(input("Unit Factor to mm: "))            # trajectory files use "meter" as units, this is the input coordiante's factor to "meter"
    angle = int(input("Angle Unit (1=degree, 2=radian):"))  # select which angle convention
    header = False                                          # if to skip the header    

    if angle == 1:
        rot = 1
    else:
        rot = 1/np.pi*180

    # default inputs for each waypoint conforming to Flexiv trajectory file format
    defaultInput = {
                        'patternName': '0',
                        'patternType': 'Scatter',
                        'x': '0',
                        'y': '0',
                        'z': '0',
                        'rx': '0',
                        'ry': '0',
                        'rz': '0',
                        'coordType': 'WORLD',
                        'coordRef': 'WORLD_ORIGIN',
                        'A1': '0',
                        'A2': '-40',
                        'A3': '0',
                        'A4': '90',
                        'A5': '0',
                        'A6': '40',
                        'A7': '0',
                        'fx': '0',
                        'fy': '0',
                        'fz': '0',
                        'mx': '0',
                        'my': '0',
                        'mz': '0',
                        'pathProf': 'line',
                        'blendZone': '50',
                        'vel': '0.1',
                        'acc': '0.5',
    }

    trajConvertor(dir, filename, filetype, defaultInput, header, factor, rot)