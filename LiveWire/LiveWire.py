import numpy as np
import math
import cv2
import networkx as nx


# Load an color image in grayscale
input_img = cv2.imread('img02.JPG',0)
# input_img = cv2.imread('Images/opencv-logo-white.PNG',0)
# input_img = cv2.imread('Images/orignal.PNG',0)
# input_img = cv2.imread('Images/changed.PNG',0)
# Even if the image path is wrong, it won’t throw any error, but print img will give you None
print(input_img)
# print(img.copy().astype(np.int8))
# Gaussian result
guassian_img = input_img.copy()
#  Gradient edges and angle of the Image
edge = input_img.copy()
angle = input_img.copy()
# result angle initialized after Non-maximum Suppression stage
result_angle = input_img.copy()
# Hysteresis Thresholding
# result_thresholding= None

imgx=len(input_img)
imgy=len(input_img[0])

gaussian_matrix=(1.0/273)* np.array([[1,4,7,4,1],
                                     [4,16,26,16,4],
                                     [7,26,41,26,7],
                                     [4,16,26,16,4],
                                     [1,4,7,4,1]])
# Noise Reduction with  5x5 Gaussian filter
# for x in range(2,imgx-2):
#     for y in range(2,imgy-2):
#         temp_array=np.empty([5, 5], dtype=int)
#         # print("%s:%s"% (x,y),end="\n")
#         total=0
#         for i in np.arange(-2,3):
#             for j in np.arange(-2,3):
#                 # print("%s:%s"% (x+i,y+j),end=" ")
#                 # print(img[x+i,y+j],end=" ")
#                 # print("%s:%s"% (i+2,j+2),end=" ")
#                 temp_array[i,j]=input_img[x+i,y+j]
#                 total=total+ (gaussian_matrix[i,j]*input_img[x+i,y+j])
#                 # print("\ndddddddddd")
#         # print(temp_array)
#         # print(int(round(sum(sum(np.matmul(temp_array, gaussian_matrix))))))
#         guassian_img[x,y]=(int(round(total)))
#         # print("\n")

# Finding Intensity Gradient of the Image
for x in range(0,imgx-1):
    for y in range(0,imgy-1):
        if guassian_img[x,y+1] > guassian_img[x,y]:
            temp1= int(guassian_img[x,y+1]-guassian_img[x,y])
        else:
            temp1= int(guassian_img[x,y]-guassian_img[x,y+1])
        if guassian_img[x+1,y] > guassian_img[x,y]:
            temp2= int(guassian_img[x+1,y]-guassian_img[x,y])
        else:
            temp2= int(guassian_img[x,y]-guassian_img[x+1,y])
        # print(int(round(np.math.sqrt(temp1+temp2))))
        edge[x,y]=(int(round(math.sqrt(np.power(temp1,2)+np.power(temp2,2)))))
        if temp1 !=0:
            # angle[x,y]=(np.math.tan(int(round(temp2/temp1))))
            angle[x,y]=math.degrees((math.atan(temp2/temp1)+90))
            # else:
            # print(temp2,temp1,end=",")

cv2.imshow('Orignal edges',edge)

# Non-maximum Suppression
for x in range(0,imgx-1):
    for y in range(0,imgy-1):
        result_angle[x,y]=angle[x,y]
        if (angle[x,y]>0 and angle[x,y]<22.5) or (angle[x,y]>157.5 and angle[x,y]<202.5) or (angle[x,y]>337.5 and angle[x,y]<360):
            # print(angle[x,y],"1",end="\n")
            if  angle[x,y]<angle[x,y-1] or  angle[x,y]<angle[x,y+1]:
                result_angle[x,y]=0
        elif (angle[x,y]>22.5 and angle[x,y]<67.5) or (angle[x,y]>202.5 and angle[x,y]<247.5):
            # print(angle[x,y],"2",end="\n")
            if  angle[x,y]<angle[x-1,y+1] or  angle[x,y]<angle[x+1,y-1]:
                result_angle[x,y]=0
        elif (angle[x,y]>67.5 and angle[x,y]<112.5) or (angle[x,y]>247.5 and angle[x,y]<292.5):
            # print(angle[x,y],"3",end="\n")
            if  angle[x,y]<angle[x-1,y] or  angle[x,y]<angle[x+1,y]:
                result_angle[x,y]=0
        elif (angle[x,y]>112.5 and angle[x,y]<157.5) or (angle[x,y]>292.5 and angle[x,y]<337.5):
            # print(angle[x,y],"4",end="\n")
            if  angle[x,y]<angle[x-1,y-1] or  angle[x,y]<angle[x+1,y+1]:
                result_angle[x,y]=0
                # else:
                # print(x,y,angle[x,y],end=",")
                # print("no region found")

already_done_paths={}
def check_threshold(x,y):
    allow_path=False
    new_x=0
    new_y=0
    path_coordinates=[]
    while True:
        if (result_angle[x,y]>0 and result_angle[x,y]<22.5) or  (result_angle[x,y]>337.5 and result_angle[x,y]<360):
            new_x=x
            new_y=y+1
        elif (result_angle[x,y]>157.5 and result_angle[x,y]<202.5):
            new_x=x
            new_y=y-1
        elif (result_angle[x,y]>22.5 and result_angle[x,y]<67.5) :
            new_x=x-1
            new_y=y+1
        elif (result_angle[x,y]>202.5 and result_angle[x,y]<247.5):
            new_x=x+1
            new_y=y-1
        elif (result_angle[x,y]>67.5 and result_angle[x,y]<112.5):
            new_x=x-1
            new_y=y
            result_angle[x-1,y]=0
        elif (result_angle[x,y]>247.5 and result_angle[x,y]<292.5):
            new_x=x+1
            new_y=y
            result_angle[x+1,y]=0
        elif (result_angle[x,y]>112.5 and result_angle[x,y]<157.5):
            new_x=x-1
            new_y=y-1
        elif (result_angle[x,y]>292.5 and result_angle[x,y]<337.5):
            new_x=x+1
            new_y=y+1

        if edge[new_x,new_y]<minimum_value:
            break
        elif result_angle[new_x,new_y]>maximum_value:
            allow_path=True
            break
        path_coordinates.append((str(new_x)+","+str(new_y)))
        already_done_paths[(str(new_x)+","+str(new_y))]=True
        if not allow_path:
            for path in path_coordinates:
                a,b=path.split(",")
                edge[int(a),int(b)]=0

minimum_value=30
maximum_value=100
for x in range(0,imgx-1):
    for y in range(0,imgy-1):
        if edge[x,y]>minimum_value and edge[x,y]<maximum_value:
            if not (str(x)+","+str(y)) in already_done_paths.items():
                check_threshold(x,y)
        elif edge[x,y]<minimum_value:
            # print(edge[x,y],end="\n")
            edge[x,y]=0

DG = nx.DiGraph()
for x in range(0,imgx-1):
    for y in range(0,imgy-1):
        # Gx=0
        # Gy=0
        # if not(result_angle[x,y]==0 or edge[x,y]==0):
        #     Gx= (1/(edge[x,y]*np.cos(result_angle[x,y])))
        #     Gy= (1/(edge[x,y]*np.sin(result_angle[x,y])))
        # if Gx>0:
        #     DG.add_weighted_edges_from([((str(x)+","+str(y)), (str(x)+","+str(y+1)), Gx), ((str(x)+","+str(y)), (str(x)+","+str(y-1)), Gx)])
        # if Gy>0:
        #     DG.add_weighted_edges_from([((str(x)+","+str(y)), (str(x-1)+","+str(y)), Gy), ((str(x)+","+str(y)), (str(x+1)+","+str(y)), Gy)])

        if result_angle[x,y]==0 or edge[x,y]==0:
            Gx= 1000000
            Gy=1000000
        else:
            Gx= (1/(edge[x,y]*np.cos(result_angle[x,y])))
            Gy= (1/(edge[x,y]*np.sin(result_angle[x,y])))
        if Gx<0:
            Gx= 1000000
        if Gy<0:
            Gy=1000000

        DG.add_weighted_edges_from([((str(x)+","+str(y)), (str(x)+","+str(y+1)), Gx), ((str(x)+","+str(y)), (str(x)+","+str(y-1)), Gx), ((str(x)+","+str(y)), (str(x-1)+","+str(y)), Gy), ((str(x)+","+str(y)), (str(x+1)+","+str(y)), Gy)])



initial=True
startx=0
starty=0
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global initial
        global startx
        global starty
        global DG
        if initial:
            initial=False
            startx=x
            starty=y
        else:
            # Draw a diagonal blue line with thickness of 5 px
            temp_list=nx.dijkstra_path(DG,(str(startx)+","+str(starty)),(str(x)+","+str(y)))
            for i in np.arange(0,len(temp_list)-1):
                a,b=temp_list[i].split(",")
                c,d=temp_list[i+1].split(",")
                cv2.line(edge,(int(a),int(b)),(int(c),int(d)),(100,100,100),5)
            startx=x
            starty=y
            print(x,y)
            print(temp_list)

cv2.namedWindow("Results")
cv2.setMouseCallback("Results", draw_circle)
while (True):
    cv2.imshow("Results", edge)
    if cv2.waitKey(20) == 27:
        break

# show image in new window
# cv2.imshow('Results',edge)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
