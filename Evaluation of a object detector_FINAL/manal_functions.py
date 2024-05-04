import shapely as shape
from shapely import affinity
import matplotlib.pyplot as plt
import math


def calculate_angle(imaginary, real):
    ''' Returns thita in polar coordinates 
    we find thita by calculating r = arctan(imaginary / real)'''
    theta = math.atan2(imaginary, real)
    return round(theta,3)

def total_bounding_area_points(p1_1,p1_2,p1_3,p1_4,p2_1,p2_2,p2_3,p2_4):
    '''Returns union, intersection iou of two object areas
    Args: Four corner points of rectangle'''
    obj_label = shape.Polygon([p1_1,p1_2,p1_3,p1_4])
    obj_predicion = shape.Polygon([p2_1,p2_2,p2_3,p2_4])
    poly_union = obj_label.union(obj_predicion)
    poly_intersection = obj_label.intersection(obj_predicion)
    iou = poly_intersection.area / poly_union.area
    return(int(poly_union.area), int(poly_intersection.area),round(iou,3))

def rotate_rectangle(cx,cy,w,l,r):
    '''Returns coordinates of rotated rectangle in shapely format
    Args: '''
    rect_origin = shape.Polygon([(-w/2, -l/2), (w/2, -l/2), (w/2, l/2), (-w/2, l/2)])
    rot_rect = affinity.rotate(rect_origin, r * 180 / 3.14)
    translated_rectangle = affinity.translate(rot_rect, cx, cy)
    return(translated_rectangle)

def plot_polygon(rect_1, rect_2 = None):
    '''Plots Two polygons
    Accepts two arguments of each rectangle
    Args: Enclosed coordinates of polygon in Shapely Polygon function
    Eg: shape.Polygon([(0,0), (1,0), (1,1), (0,1)])'''
    try:
        x1, y1 = rect_1.exterior.xy
    except:
        pass
    try:
        x2, y2 = rect_2.exterior.xy
    except:
        pass
    plt.plot(x1,y1, "g")  # Required Rotated Rectangle
    #plt.fill(x1,y1,"lightgreen")
    try:
        plt.plot(x2,y2, "r")  # Required Rotated Rectangle
        #plt.fill(x2,y2,"orange")
    except:
        pass
    plt.show()

def display_bounding_boxes_2(path,labels, predictions, color = ("red", "lime"), title = "bev", text_1 = None, text_2 = None):
    ''' Displays Bounding boxes in the image
        Args: takes image path and list of coordinates of the rectangle and colour of the bounding box'''
    img = plt.imread(path)
    c = 0
    i = 0
    l = [predictions, labels]
    for list in l:
        for rect in list:
            rectangle = shape.Polygon(rect)
            x,y = rectangle.exterior.xy
            plt.plot(x,y, color = color[i])
            # print(c)
            if(i == 1):
                try:
                    # if(text_1[c] == 0 or text_1[c] < 0.50):
                    if(text_1[c] == 0):
                        plt.text(x[2], y[2], text = "", color = "white")
                        c+=1
                    else:
                        plt.text((x[0] + x[2]) // 2, (y[0] + y[2]) // 2 , text_1[c], color = "white")
                        c+=1
                except:
                    c+=1
                    print("LOOP IN BACKEND FOR BOUNDING BOXES NOT EXECUTED")
        i += 1
    plt.text(-10,680,"Precision: {0}%".format(text_2[0] * 100), color = "blue", size = 12 , weight = "bold")
    plt.text(340,680,"Recall Value: {0}%".format(text_2[1] * 100), color = "blue", size = 12 , weight = "bold")
    plt.text(280,-12," TP: {0}".format(text_2[2]), color = "green", size = 12 , weight = "bold")
    plt.text(400,-12," FP: {0}".format(text_2[3]), color = "orange", size = 12 , weight = "bold")
    plt.text(520,-12," FN: {0}".format(text_2[4]), color = "orange", size = 12 , weight = "bold")
    plt.text(10,-12," Image: {0}".format(title), color = "brown", size = 12 , weight = "bold")
    plt.imshow(img)
    # plt.title(title)
    plt.savefig("E:\Sem 1 Notes\Lidar And Radar Systems\Task 2\T-2_images 1.0\{0}.png".format(title))
    plt.show()

def calculate_endpoints(cx,cy,w,l):
    ''' Converts x,y,w,l values into four coordinates of a rectangle'''
    return([(int(cx-w/2), int(cy-l/2)), (int(cx+w/2), int(cy-l/2)), (int(cx+w/2), int(cy+l/2)), (int(cx-w/2), int(cy+l/2))])

def polygon_to_endpoints(polygon):
    '''Takes input as coordinates in shapely polygon functions and returns four coordinates of rectangele in list format'''
    x_coords, y_coords = polygon.exterior.xy
    endpoints = list(zip(x_coords, y_coords))
    return(endpoints[0:-1])