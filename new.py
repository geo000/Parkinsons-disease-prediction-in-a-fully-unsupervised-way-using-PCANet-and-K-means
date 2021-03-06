#incremental trainning of PCANet
import nibabel as nib
import numpy as np  

import cv2
import timeit
import argparse
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
# avoid the odd behavior of pickle by importing under a different name
import pcanet as net
from utils import load_model, save_model, load_mnist, set_device
from sklearn.linear_model import SGDClassifier
from sklearn.cluster import MiniBatchKMeans
import os
parser = argparse.ArgumentParser(description="PCANet example")
parser.add_argument("--gpu", "-g", type=int, default=-1,
                    help="GPU ID (negative value indicates CPU)")

subparsers = parser.add_subparsers(dest="mode",
                                   help='Choice of train/test mode')
subparsers.required = True
train_parser = subparsers.add_parser("train")
train_parser.add_argument("--out", "-o", default="result",
                          help="Directory to output the result")

test_parser = subparsers.add_parser("test")
test_parser.add_argument("--pretrained-model", default="result",
                         dest="pretrained_model",
                         help="Directory containing the trained model")

args = parser.parse_args()

def train():
    print("Training PCANet")
    pcanet = net.PCANet(
        image_shape=(240,256),
        filter_shape_l1=2, step_shape_l1=1, n_l1_output=3,
        filter_shape_l2=2, step_shape_l2=1, n_l2_output=3,
        filter_shape_pooling=2, step_shape_pooling=2
    )
    #clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
    clf=MiniBatchKMeans(n_clusters=2,random_state=0,batch_size=27808)
    val = int(input("Which phase you want to train?? 1,2,3,4"))
    if val==1:
        print("TRAINING PHASE 1")
    
        for i in range(0,30):
            images_train=load_data_negative(i)
            print("Input Structure-")
            print(images_train.shape)
            pcanet.validate_structure()
            pcanet.fit(images_train)
            print("Transform")
            X_train= pcanet.transform(images_train)
            print("Resultant shape after the transform")
            print(X_train.shape)
            len1=X_train.shape[0]
            label1=np.zeros((len1,), dtype=int)
            clf=clf.partial_fit(X_train)
        print("Resultant of transform")
        print(X_train[10,0:30])
        save_model(pcanet,"/home/ganesh/pcanet.pkl")
        print("Phase 1 model saved")
        save_model(clf,"/home/ganesh/clf.pkl")
        print("Phase 1 classifier saved")
            
    elif val==2:
        print("TRAINING PHASE 2")
        print("Loading the exsisting model and Classifier")
        clf=load_model("/home/ganesh/clf.pkl")
        pcanet = load_model("/home/ganesh/pcanet.pkl")
        for i in range(60,120):
            images_train=load_data_negative(i)
            print("Input Structure-")
            print(images_train.shape)
            pcanet.validate_structure()
            pcanet.fit(images_train)
            print("Transform")
            X_train= pcanet.transform(images_train)
            print("Resultant shape after the transform")
            print(X_train.shape)
            len1=X_train.shape[0]
            label1=np.zeros((len1,), dtype=int)
            clf=clf.partial_fit(X_train)
        
        save_model(pcanet,"/home/ganesh/pcanet.pkl")
        print("Phase 2 model saved")
        save_model(clf,"/home/ganesh/clf.pkl")
        print("Phase 2 classifier saved")
     
    elif val==3:
        print("TRAINING PHASE 3")
        print("Loading the exsisting model and Classifier")
        clf=load_model("/home/ganesh/clf.pkl")
        pcanet = load_model("/home/ganesh/pcanet.pkl")
        for i in range(0,30):
           images_train=load_data_positive(i)
           print("Input Structure-")
           print(images_train.shape)
           pcanet.validate_structure()
           pcanet.fit(images_train)
           print("Transform")
           X_train= pcanet.transform(images_train)
           print("Resultant shape after the transform")
           print(X_train.shape)
           len1=X_train.shape[0]
           label1=np.ones((len1,), dtype=int)
           clf=clf.partial_fit(X_train)
        
        save_model(pcanet,"/home/ganesh/pcanet.pkl")
        print("Phase 3 model saved")
        save_model(clf,"/home/ganesh/clf.pkl")
        print("Phase 3 classifier saved")

    elif val==4:
        print("Loading the exsisting model and Classifier")
        clf=load_model("/home/ganesh/clf.pkl")
        pcanet = load_model("/home/ganesh/pcanet.pkl")
        print("TRAINING PHASE 4")
        for i in range(158,316):
            images_train=load_data_positive(i)
            print("Input Structure-")
            print(images_train.shape)
            pcanet.validate_structure()
            pcanet.fit(images_train)
            print("Transform")
            X_train= pcanet.transform(images_train)
            print("Resultant shape after the transform")
            print(X_train.shape)
            len1=X_train.shape[0]
            label1=np.ones((len1,), dtype=int)
            clf=clf.partial_fit(X_train)
        print("Resultant of transform")
        print(X_train[10,0:30])
        save_model(pcanet,"/home/ganesh/pcanet.pkl")
        print("Phase 4 model saved")
        save_model(clf,"/home/ganesh/clf.pkl")
        print("Phase 4 classifier saved")
    
def load_data_negative(no):
    #Loading the normal class
    all_files=os.listdir("/home/ganesh/ganeshcen19/NC")
    path1=os.path.join("/home/ganesh/ganeshcen19/NC",all_files[no])
    print(path1)
    img = nib.load(path1)
    img=img.get_data()
    data_arr=np.asarray(img, dtype = float)
    data_arr=np.squeeze(data_arr,axis=3)
    if data_arr.shape!=(176, 240, 256):
        normal_data=np.empty([176,240,256], dtype=float)
        for itr in range(0,176):
                temp=data_arr[itr,:,:]
                resized = cv2.resize(temp,(256,240), interpolation = cv2.INTER_AREA)
                #resized = np.expand_dims(resized, axis=0)
                normal_data[itr,:,:]=resized
    else:
        normal_data=data_arr
                
    
    return normal_data

def load_data_positive(no):
    #Loading the normal class
    all_files=os.listdir("/home/ganesh/ganeshcen19/PD")
    path1=os.path.join("/home/ganesh/ganeshcen19/PD",all_files[no])
    print(path1)
    img = nib.load(path1)
    img=img.get_data()
    data_arr=np.asarray(img, dtype = float)
    data_arr=np.squeeze(data_arr,axis=3)    
    if data_arr.shape!=(176, 240, 256):
        normal_data=np.empty([176,240,256], dtype=float)
        for itr in range(0,176):
                temp=data_arr[itr,:,:]
                resized = cv2.resize(temp,(256,240), interpolation = cv2.INTER_AREA)
                #resized = np.expand_dims(resized, axis=0)
                normal_data[itr,:,:]=resized
    else:
        normal_data=data_arr
                
    
    return normal_data

def test(pcanet, classifier):
    images_test, y_test = load_test()
    print("Transforming images")
    X_test = pcanet.transform(images_test)
    print("Doing the classification")
    y_pred = classifier.predict(X_test)
    return y_pred, y_test

def load_test():
    all_files=os.listdir("/home/ganesh/ganeshcen19/NC")
    path1=os.path.join("/home/ganesh/ganeshcen19/NC",all_files[2])
    print(path1)
    img = nib.load(path1)
    img=img.get_data()
    normal_data=np.asarray(img, dtype = float)
    normal_data=normal_data[0:20,:,:]
    print(normal_data.shape)
            
    all_files=os.listdir("/home/ganesh/ganeshcen19/PD")
    
    
    path1=os.path.join("/home/ganesh/ganeshcen19/PD",all_files[2])
    print(path1)
    img = nib.load(path1)
    img=img.get_data()
    data_arr=np.asarray(img,dtype = float)
    data_arr=data_arr[0:20,:,:]
    normal_data=np.concatenate((normal_data,data_arr),axis=0)
    
    normal_data=np.squeeze(normal_data,axis=3);
    print("Test data shape")
    print(normal_data.shape)

    label1=np.zeros((20,), dtype=int)
    label2=np.ones((20,), dtype=int)
    label=np.concatenate((label1,label2),axis=0)
    print("Test Label Shape")
    print(label.shape)
    print("Labels")
    print(label)
    return normal_data,label
if args.gpu >= 0:
    set_device(args.gpu)


if args.mode == "train":
    print("Training the model...")
    train()
           
elif args.mode == "test":   
    print("Loading the exsisting model and Classifier")
    clf=load_model("/home/ganesh/clf.pkl")
    pcanet = load_model("/home/ganesh/pcanet.pkl")
    y_pred, y_test=test(pcanet, clf)
    print("Prediction")
    print(y_pred)
    print("Actual")
    print(y_test)
    print("Evaluating the accuracy")
    accuracy = accuracy_score(y_test, y_pred)
    print("accuracy: {}".format(accuracy))
    
    