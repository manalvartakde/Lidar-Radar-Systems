import numpy as np
import os
import manal_functions as manal
import matplotlib.pyplot as plt

folders = ["labels", "predictions"]
folder_loc = "E:/Sem 1 Notes/Lidar And Radar Systems/Task 2/KITTI_Selection/KITTI_Selection/"

final_vals = {"Precision" : [] , "recall" : []}
data = {}
labels = {}
predictions = {}
 # Data reading
for folder in folders:
    pth = folder_loc + folder
    f = os.listdir(pth)
    for file in f:                             
        pth = folder_loc + folder + "/" + file 
        arr = np.loadtxt(pth, delimiter=",")
        if(folder == "labels"):
            labels[file[:6]] = arr
        if(folder == "predictions"):
            predictions[file[:6]] = arr
            
########## END OF READING LOOPS ###################
# data storage
            
for no in labels.keys():
    data[no] = [labels[no], predictions[no]]   # data[key][0] = labels  /// data[key][1] = predictions
#calculation for IOU

# print(data["006130"])
thres = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.98]

for key in ["006048", "006067", "006121", "006130", "006211", "006291"]:
    x = []
    y = []
    for threshold in thres:
        path_bev = "E:/Sem 1 Notes/Lidar And Radar Systems/Task 2/KITTI_Selection/KITTI_Selection/bev/" + key + ".png"
        arr_labels = []
        arr_predictions = []
        text_arr = []
        (labels, predictions) = data[key]
        # print(labels, predictions)
        if(len(predictions) == 0):
            labels = [labels]
        
        # print("\n \n Working on ", key)
        # print("Predicted elements",len(data[key][1]), key)
        # print("Labelled elements",len(data[key][0]), key)
        false_neg_arr = []
        for lab in range(len(labels)):
                
            try:
                if(False): continue# if(int(data[key][0][lab][0]) != 0):
                #     continue
                else:
                    (lab_cx,lab_cy,lab_w,lab_l) = (data[key][0][lab][1:5])    # rectangle point values for predicted
                    (im,re) = (data[key][0][lab][5:])
                    r_lab = manal.calculate_angle(im,re)
                    rotn_labels = manal.polygon_to_endpoints(manal.rotate_rectangle(lab_cx,lab_cy,lab_w,lab_l,r_lab))
                    # (lab_p1,lab_p2,lab_p3,lab_p4) = (rotn_labels[0], rotn_labels[1], rotn_labels[2], rotn_labels[3])    
                    (lab_p1,lab_p2,lab_p3,lab_p4) = (rotn_labels[i] for i in range(len(rotn_labels))) 

                    best_fit_iou = 0
                    
                    for pred in range(len(predictions)): 
                        if(len(predictions) != 0):        
                            try:
                                if(data[key][1][pred][6] < threshold): continue# if(int(data[key][1][pred][8]) != 0):
                                #     continue
                                else:
                                    (pr_cx,pr_cy,pr_w,pr_l) = (data[key][1][pred][0:4])
                                    (im,re) = (data[key][1][pred][4:6])
                                    r_pred = manal.calculate_angle(im,re)            
                                    rotn_predictions = manal.polygon_to_endpoints(manal.rotate_rectangle(pr_cx,pr_cy,pr_w,pr_l,r_pred))
                                    (pr_p1,pr_p2,pr_p3,pr_p4) = (rotn_predictions[i] for i in range(len(rotn_predictions)))                                                         ##
                                            
                                    new_iou = manal.total_bounding_area_points(lab_p1,lab_p2,lab_p3,lab_p4,pr_p1,pr_p2,pr_p3,pr_p4)[2]
                                    

                                    if(new_iou > best_fit_iou):
                                        best_fit_iou = new_iou

                            except:
                                print("Predicted FIRST Loop not executed for ", key)
                    if(best_fit_iou < 0.5):
                        false_neg_arr.append(new_iou)
                    # IoU values are filled according to predicted values order
                    
                    text_arr.append(round(best_fit_iou, 2))
            except:
                print("Labels FIRST Loop not executed for ", key)

    ############# PRINTING VALUES ##########
        # print(text_arr)
                
        print("\n\n Printing for Treshold: ", threshold,"\n Image:", key)
        true_positives = len([k for k in text_arr if(k>=0.50)])
        # print("True Positives: ", true_positives)
        false_positives = len(predictions) - true_positives
        # print("False Positives ", false_positives)
        # print("Total predicted values: ", len(predictions), "; TP+FP = ", true_positives+false_positives)
        
        if(true_positives+false_positives != 0):
            precision = round(true_positives / (true_positives+false_positives),2)
            print("Precision: ", precision)
        else:
            precision = 0.0
        
        false_negatives = len(false_neg_arr) 
        # print("False Negatives: ", false_negatives)

        if(true_positives + false_negatives != 0):
            recall_value = round(true_positives / (true_positives + false_negatives),2)
        else:
            recall_value = 0.0
        print("Recall Value: ", recall_value)
        y.append(precision)
        x.append(recall_value)

    fig, ax = plt.subplots()
    ax.scatter(x,y)
    ax.set(xlim=(0, 1), ylim=(0, 1))
    for i, txt in enumerate(thres):
        ax.annotate(txt, (x[i], y[i]))
    plt.title(key)
    plt.show()

############################ PLOTTING #################################

    # for pred in range(len(predictions)):      # looping for predictions // red
    #     try:
    #         if(data[key][1][pred][6] < threshold): continue
    #         else:
    #             (pr_cx,pr_cy,pr_w,pr_l) = (data[key][1][pred][0:4])
    #             (im,re) = (data[key][1][pred][4:6])
    #             r_pred = manal.calculate_angle(im,re)
    #             # Plotting #
    #             rotn_predictions = manal.rotate_rectangle(pr_cx,pr_cy,pr_w,pr_l,r_pred)
    #             arr_predictions.append(rotn_predictions)
    #     except:
    #         print("Prediction Loop not executed for ", key)

    # for lab in range(len(labels)):         # looping for labels // yellow // ground truth
    #     if(len(predictions) != 0):
    #         (lab_cx,lab_cy,lab_w,lab_l) = (data[key][0][lab][1:5])
    #         (im,re) = (data[key][0][lab][5:])
    #         r_lab = manal.calculate_angle(im,re)
    #         rotn_labels = manal.rotate_rectangle(lab_cx,lab_cy,lab_w,lab_l,r_lab)
    #         arr_labels.append(rotn_labels)
    #     else:
    #         (lab_cx,lab_cy,lab_w,lab_l) = (labels[0][1:5])
    #         (im,re) = (labels[0][5:])
    #         r_lab = manal.calculate_angle(im,re)
    #         rotn_labels = manal.rotate_rectangle(lab_cx,lab_cy,lab_w,lab_l,r_lab)
    #         arr_labels.append(rotn_labels)

    # manal.display_bounding_boxes_2(path_bev, arr_labels, arr_predictions, title = key, text_1 = text_arr, text_2= [precision, recall_value, true_positives, false_positives, false_negatives])


