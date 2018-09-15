
# coding: utf-8

# ## MyMusic360_face_reader Application
# #### AI - ML system built using Microsoft Azure FACE API 
# ##### System loads user pictures and gets trained.
# ##### Users use cam-login i.e. picture to authenticate into the system
# ##### Along with the credential verification, mm360 system also guages their mood
# ##### mm360_face_reader then sends the user details including mood to the audio selection system.
# ##### Audio selection system will use the mood to play - recommend the music for the user.

# In[1]:


import cognitive_face as CF
import requests
from io import BytesIO
from PIL import Image, ImageDraw
import sys, getopt, os
import requests
import json
#from cv2 import *
import numpy as np
import cv2
import time


# ** STEPS **<br>
# *** Detecting faces using the Face - Detect API ***<br>
# *** Creating PersonGroups using the PersonGroup - Create API *** <br>
# *** Creating persons using the PersonGroup Person - Create API ***<br>
# *** Train a PersonGroup using the PersonGroup – Train API ***<br>
# *** Identifying unknown faces against the PersonGroup using the Face - Identify API ***<br>

# In[2]:


#######
# Init
#######
subscription_key = '0699e543b5874c18b121d87671317d8a'
img_url = './mm360_filename.jpg' 
root_folder = './group_pictures'

# base face_api url
uri_base = 'https://southcentralus.api.cognitive.microsoft.com/face/v1.0'

# To get some custom data
custom_data = {'skb':'Balaji',
              'ak':'Andrew',
              'sg':'Suswidth',
              'ns':'Nikhil',
              'nss':'Nishanth',
              'jgs':'Jessica',
              'rb':'Raji'}
emotion_metric = {
                0:'anger',
                1:'contempt',
                2:'disgust',
                3:'fear',
                4:'happiness',
                5:'neutral',
                6:'sadness',
                7:'surprise'}

CF.BaseUrl.set(uri_base)
CF.Key.set(subscription_key)


# In[6]:


#######
# getBinaryFileData
#######
def getBinaryFileData(filename):
    # open jpg file as binary file data for intake by the MCS api  
    with open(filename, 'rb') as f:
        img_data = f.read()
        return img_data


# In[7]:


# def take_picture():
#     cam = cv2.VideoCapture(0)   # 0 -> index of camera
#     s, img = cam.read()
#     if s:    # frame captured without any errors
#        namedWindow("cam-test")
#        imshow("cam-test",img)
#        destroyWindow("cam-test")
#        imwrite("mm360_filename.jpg",img) #save image

#     # close the camera    
#     cam.release()
#     print("Succesfully took mm360_filename.jpg")


# In[8]:


#######
# take_picture
#######
def take_picture():
    # Camera 0 is the integrated web cam on my netbook
    camera_port = 0

    #Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30
    
    try:
 
        # Now we can initialize the camera capture object with the cv2.VideoCapture class.
        # All it needs is the index to a camera port.
        camera = cv2.VideoCapture(camera_port)

        # Captures a single image from the camera and returns it in PIL format
        def get_image():
            # read is the easiest way to get a full image out of a VideoCapture object.
            retval, im = camera.read()
            return im

        # Ramp the camera - these frames will be discarded and are only used to allow v4l2
        # to adjust light levels, if necessary
        for i in range(ramp_frames):
            temp = get_image()
        print("Taking image...")
        
        # Take the actual image we want to keep
        camera_capture = get_image()
        file = "./mm360_filename.jpg"
        
        # A nice feature of the imwrite method is that it will automatically choose the
        # correct format based on the file extension you provide. Convenient!
        cv2.imwrite(file, camera_capture)
        print(f'saving {file}..')

        # You'll want to release the camera, otherwise you won't be able to create a new
        # capture object until your script exits
        del(camera)
    except Exception as e:
        print(f"EXCETION in take_picture::{e}")
        del(camera)
    print(f'Campleted taking picture.')


# In[9]:


#######
# getRectangle
#######
#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    #return ((left, top), (bottom, right))
    return (left,top,bottom,right)


# *** Detecting faces using the Face - Detect API ***<br>

# In[14]:


#######
# recogn_from_local_img
# detect image (face) method
#######
def recogn_from_local_img(filename):
    #     CF.BaseUrl.set(uri_base)
    #     CF.Key.set(subscription_key)
    
    #     attributes: [Optional] Analyze and return the one or more specified
    #         face attributes in the comma-separated string like
    #         "age,gender". Supported face attributes include age, gender,
    #         headPose, smile, facialHair, glasses, emotion, makeup, accessories,
    #         occlusion, blur, exposure, noise. Note that each face attribute
    #         analysis has additional computational and time cost.
    #         attributes='age,gender,emotion'

    try:
        response = CF.face.detect(filename, attributes='emotion')
        print(response)
        return response
    except Exception as e:
        print(e)
        
        
#     face_ids = [d['faceId'] for d in response]
#     print(face_ids)


# In[11]:


#######
# drawRectangeAroungFace
#######
def drawRectangeAroungFace(img_url):
    faces = recogn_from_local_img(img_url)
    # print(faces)

    #Download the image from the url
    img = Image.open(BytesIO(getBinaryFileData(img_url)))

    #For each face returned use the face rectangle and draw a red box.
    draw = ImageDraw.Draw(img)
    for face in faces:
        print(getRectangle(face))
        draw.rectangle(getRectangle(face), outline='red')
        
    # #Display the image in the users default image browser.
    img.show()


# In[12]:


#json.loads(recogn_from_local_img_1(img_url))[0]
#match_image(img_url)
#getBinaryFileData(img_url)
#drawRectangeAroungFace(img_url)


# *** Delete a PersonGroup using the PersonGroup – Delete API ***<br>

# In[13]:


#######
# deletePersonGroup
#######
def deletePersonGroup(personGroupId):
    CF.BaseUrl.set(uri_base)
    CF.Key.set(subscription_key)
    
    try:
        CF.person_group.delete(personGroupId)
    except Exception as e:
        print(e)
        


# *** Creating PersonGroups using the PersonGroup - Create API *** <br>

# In[14]:


#######
# createPersonGroup
#######
def createPersonGroup(personImage, personGroupId):
    
    #BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'
    #PERSON_GROUP_ID = personGroupId
    CF.BaseUrl.set(uri_base)
    CF.Key.set(subscription_key) 
    
    try:
        # create person group
        CF.person_group.create(personGroupId, personGroupId)
        
        print(f"personGroupId = {personGroupId}")

        return personGroupId;
        
    except Exception as e:
        print(f"EXCEPTION :: {e}")  
        raise e


# *** Creating persons using the PersonGroup Person - Create API ***<br>

# In[15]:


#######
# createPersonGroup
#######
def createPerson(personGroupId, personName):

    try:
       
        # create person
        cust_data = custom_data.get(personName)
        if(cust_data == None):
            cust_data = 'Hello New User'
        response = CF.person.create(personGroupId, 
                                    personName, 
                                    cust_data)
                                    #f'{personName} person data')
        print(f"RESPONSE={response}")
        # Get person_id from response
        person_id = response['personId']
        
        print(f"person_id = {person_id}")

        return person_id;
        
    except Exception as e:
        print(f"EXCEPTION :: {e}")  
        raise e


# *** Add persons using the PersonGroup Person - Create API ***<br>

# In[ ]:


#######
# addPersonFace
#######
def addPersonFace(personImage,
                  personGroupId, 
                  person_id,
                  user_name_key,
                  personUserData):
    try:
        #add_face(image, person_group_id, person_id, user_data=None, target_face=None).
        #targetFace=left,top,width,height
        #"targetFace=10,10,100,100"
        
        tf_rect = personUserData[0]['faceRectangle']
        tf_rect_val = f'{tf_rect["left"]},{tf_rect["top"]},{tf_rect["width"]},{tf_rect["height"]}'
        print(tf_rect_val)
        
        cust_data = custom_data.get(user_name_key)
        if(cust_data == None):
            cust_data = 'Hello New User'
        persisted_face_id = CF.person.add_face(personImage, 
                                               personGroupId, 
                                               person_id, 
                                               cust_data,
                                               #f'{personGroupId} person data',
                                               tf_rect_val)
                          

        print(f"CF.person.lists: {CF.person.lists(personGroupId)}")
        print(f"Sucessfully added ")

        return persisted_face_id
    except Exception as e:
        print(f"EXCEPTION :: {e}")  
        raise e


# #### Add a New Person Face to a existing Person

# In[21]:


#######
# addFaceToExistingPerson
#######
def addFaceToExistingPerson(personImage,
                  personGroupId,
                  user_name_key
                  ):
    try:
        #add_face(image, person_group_id, person_id, user_data=None, target_face=None).
        #targetFace=left,top,width,height
        #"targetFace=10,10,100,100"
        
        personUserData = recogn_from_local_img(personImage)
        tf_rect = personUserData[0]['faceRectangle']
        tf_rect_val = f'{tf_rect["left"]},{tf_rect["top"]},{tf_rect["width"]},{tf_rect["height"]}'
        print(tf_rect_val)
            
        # get the current members in the PersonGroup List
        currentGroupMembers = CF.person.lists(personGroupId)
        for user in currentGroupMembers:
            if(user['name'] == user_name_key):
                persisted_face_id = CF.person.add_face(personImage, 
                                                       personGroupId, 
                                                       user['personId'], 
                                                       user['name'],
                                                       #f'{personGroupId} person data',
                                                       tf_rect_val)
            else: #NEw addition
                print(f"Cannot ADD Person Face for {user_name_key}, PersonGroupId={personGroupId}")
                print(f"user['name'] = {user['name']} Not Found!!")

        print(f"CF.person.lists: {CF.person.lists(personGroupId)}")
        print(f"Sucessfully added ")

        return persisted_face_id
    except Exception as e:
        print(f"EXCEPTION :: {e}")  
        raise e


# *** Train a PersonGroup using the PersonGroup – Train API ***<br>

# In[17]:


#######
# trainPersonGroup
#######
def trainPersonGroup(personGroupId):
        try:
            CF.person_group.train(personGroupId)
            response = CF.person_group.get_status(personGroupId)
            status = response['status']

            print(f"STATUS  = {status}")
            return status

        except Exception as e:
            print(f"EXCEPTION :: {e}")

        print(f'Complete training {personGroupId}')   


# *** Identifying unknown faces against the PersonGroup using the Face - Identify API ***<br>

# In[18]:


#######
# identifyPerson
#######
def identifyPerson(filename, personGroupId):
    try:
        response = CF.face.detect(filename, attributes='emotion')
        face_ids = [d['faceId'] for d in response]
        print(f"face_ids = {face_ids}")
    
        identified_faces = CF.face.identify(face_ids, personGroupId)
        print(f"identified_faces = {identified_faces}")
        # get the emotions for the matching face_ids
        responses = []
        for d in response:
            for ided_face in identified_faces:
                if(d['faceId'] == ided_face['faceId']):
                    #print(d)
                    responses.append({
                        'faceId': d['faceId'],
                        'candidates':ided_face['candidates'],
                        'emotion': d['faceAttributes']['emotion']})
            print(responses)
        return responses
    except Exception as e:
        print(f"EXCEPTION:{e}")


# In[ ]:


# 'emotion': {'anger': 0.0,
#    'contempt': 0.0,
#    'disgust': 0.0,
#    'fear': 0.0,
#    'happiness': 0.0,
#    'neutral': 0.999,
#    'sadness': 0.001,
#    'surprise': 0.0}
# a = [0.0,0.0,0.0,0.0,0.0,0.999,0.001,0.0]
# print(max(enumerate(a),key=lambda x: x[1])[0])


# In[20]:


def getEmotionsAsList(emotion):
    emotionList = []
    emotionList.append(emotion['anger'])
    emotionList.append(emotion['contempt'])
    emotionList.append(emotion['disgust'])
    emotionList.append(emotion['fear'])
    emotionList.append(emotion['happiness'])
    emotionList.append(emotion['neutral'])
    emotionList.append(emotion['sadness'])
    emotionList.append(emotion['surprise'])
    
    print(emotionList)
    return emotionList                         


# In[21]:


def guageEmotionList(emotion):
    emotionList = getEmotionsAsList(emotion)
    #get the highest number among the mood fields
    topEmotion = max(enumerate(emotionList),key=lambda x: x[1])[0]
    mood = emotion_metric[topEmotion]
    return mood


# <h3> Method to loadi the  user pictures and train MyMusic360 </h3><br>
# <p>1. Loads the images from root folder</p>
# <p>1.1 Expects folder structure to be  </p>
#     start(root) : group_pictures/ <br>
#     Members folder, must be names with unique member initials:  <br>
#         group_pictures/skb, group_pictures/sg, group_pictures/ak <br>
#     Pictures (*.jpg) specific to users under their names folder <br>
#         skb's pics under group_pictures/skb/*.jpg </p>
# <p>2 Creates PersonGroup for root folder </p>
# <p>3 Creates Person (s) for each member folder </p>
# <p>4 Adds pics under each Person </p>
# <p>5 Trains the PersonGroup </p>

# In[22]:


#######
# loadGroupImages
#
# main method to load the images of group members and train
# so any future login can be identified
#######
def loadGroupImages(folder, personGroupId):
    # contains [{personId: [persistent_face_ids]}]
    # eg: [{skb:[face_id_1, face_id2]}, {sg:[face_id_1, face_id2]}, {ak:[face_id_1, face_id2]}]
    
    personGroup = {}
    personList = []
    persistentPersonFaceIDList = []
    personId = ''
    persistentPersonFaceID = ''
    loop_count = 0
    file_loop_count = 0
    
    for root, dirs, files in os.walk(folder):
        current_folder = ''
        for dir in dirs:
            personGroup[dir] = {}
        
        for file in files:
            fullpath = os.path.join(root, file)
            
            ## Sleep to stay under the service restriction
            time.sleep(10)
            
            if ((os.path.splitext(fullpath)[1] == '.jpeg') or
                (os.path.splitext(fullpath)[1] == '.jpg')):
            
                # use foldername as the person name
                foldername = os.path.split(fullpath)[0].split('/')[2]
                
                personList = personGroup[foldername]
                
                if(loop_count == 0):
                    try:
                        print("Starting createPersonGroup")
                        createPersonGroup(file, personGroupId)
                        print("Finished createPersonGroup")
                    except CF.CognitiveFaceException as e:
                        print(e)
                        # if PersonGroupExists already exists just add faces to it
                        if(e.code == 'PersonGroupExists'):
                            print("Error PersonGroupExists")
                    loop_count += 1   
                try:
                    #
                    # create Person if does not exist
                    #
                    print("Starting createPerson()")
                    
                    # create a new key in the dict for the first entry 
                    # for every user/person
                    person_dict = personGroup.get(foldername)
                    if(len(person_dict) == 0):
                        print(f"****** Creating NEW personID ***") 
                        personId = createPerson(personGroupId, foldername)
                        person_dict = {personId:[]}
                        personGroup[foldername] = person_dict
                    else:
                        print(f"****** FOUUNd personID ***")
                        print(f"personId = {person_dict}")
                  
                    print("Finished createPerson()")

                    #
                    # Add Person(s) face
                    #
                    print("Starting addPersonFace()")
                    personId = list(person_dict.keys())[0]
                    print(f"personId = {personId}")
                    persistentPersonFaceID = addPersonFace(fullpath, 
                                                  personGroupId, 
                                                  personId,
                                                  foldername, 
                                                  recogn_from_local_img(fullpath))
                    persistentIdsList = person_dict.get(personId)
                    persistentIdsList.append(persistentPersonFaceID)
                    person_dict[personId] = persistentIdsList
                    print("Finished addPersonFace()")     
                    
                except Exception as e:
                    print(f"EXCEPTION in LOOP-createPerson :: {e}")
                file_loop_count += 1
                    
    print(f"ALL_DONE +++ {personGroup}")  
    #
    # Train the group
    #
    try:
        status = trainPersonGroup(personGroupId)
        # print Status
        print(f"STATUS: {status}")
    except CF.CognitiveFaceException as e:
        print(e)


# ## Method to communicate to the Spotify component.
# ### Take the Pic and check with load images to predict the user

# #### Steps :
# <b> Take Pic <br> 
# <b> Save pic locally <br> 
# <b> identify the person from the stored collection <br> 
# <b> guage the mood of the person - single value, highest from emotion will be used <br>
# <b> call spotify wrapper layer of the software , pass the user-info: user_id, mood

# In[23]:


def handleMM_User(groupUserId, pic_to_identify = None):
    try:
        global img_url
        if(pic_to_identify == None):
            # Take Pic
            take_picture()
        else:
            img_url = pic_to_identify
            
        # identify the person from the stored collection 
        responses = identifyPerson(img_url, groupUserId)
        person_id = responses[0]['candidates'][0]['personId']
        # guage the mood of the person - single value, highest from emotion will be used 
        print(responses[0]['emotion'])
        mood = guageEmotionList(responses[0]['emotion'])
        print(f"Mood = {mood}")
        info = CF.person.get(groupUserId, person_id)
    except Exception as e:
        print(f"EXCEPTION-handleMM_User::{e}")
        print(f"!! FATAL, Communication to comm_To_mm360_wrapper did not occur !!")
        return
    
    comm_To_mm360_wrapper = {
        'userName':info['name'],
        'userData':info['userData'],
        'userCurrentMood':mood
    }

    print(f"Welcome USER ==> {info['userData']}, your mood is {mood}")
    print(f"data_sent_to_music(spotify)_wrapper = {comm_To_mm360_wrapper}")
    
    return comm_To_mm360_wrapper
    #
    #  TBD -- CAll to Spotify Wrapper layer
    #
    # call_mm360_spotify_wrapper({comm_To_mm360_wrapper})


# ## Main start function call to load the images and be ready to recognize pic

# In[39]:


#loadGroupImages('./group_pictures', "mm360_group1")


# ## Step 2: Running the visual login and mood capture

# In[40]:


# Calling the user login i.e. photo capture for authentication and mood capture
# user detail name, credentials and mood will be sent to the music wrapper (spotify) component
#handleMM_User()


# In[ ]:


# skb_group_id = createPersonGroup('./group_pictures/skb/skb2.jpg',
#                                      "mm360_group1")
# skb_group_id
# balaji_client_id = createPerson("mm360_group1", "ak")
# 
# img_url = './group_pictures/ak/ak_pic2.jpeg'
# addPersonFace(img_url, 
#               "mm360_group1", 
#               "94e18f3b-a394-4f12-b9ec-01b8b9c03e9d", 
#               "ak",
#               recogn_from_local_img(img_url))
# trainPersonGroup("mm360_group1")
#deletePersonGroup("skb_family_group")
# deletePersonGroup("mm360_group1")


# In[ ]:


# take_picture()


# In[52]:


# responses = identifyPerson('mm360_filename.jpg', "mm360_group1")
# person_id = responses[0]['candidates'][0]['personId']
# print(responses[0]['emotion'])
# mood = guageEmotionList(responses[0]['emotion'])
# print(f"Mood = {mood}")


# In[53]:


# info = CF.person.get("mm360_group1", person_id)

# print(f"Welcome USER ==> {info['userData']}, your mood is {mood}")


# In[54]:


# info


# In[55]:


# responses


# In[56]:


# CF.person.get('mm360_group1', person_id)


# In[20]:


print(CF.person.lists("mm360_group1"))
#print(CF.person.lists("skb-family"))


# In[18]:


users = CF.person.lists("mm360_group1")
#users = CF.person.lists("skb-family")


# In[19]:


users


# In[10]:


for user in users:
    print(user['name'])


# In[15]:


personUserData = recogn_from_local_img('group_pictures/ak/ak_pic1.jpg')


# In[16]:


tf_rect = personUserData[0]['faceRectangle']
tf_rect_val = f'{tf_rect["left"]},{tf_rect["top"]},{tf_rect["width"]},{tf_rect["height"]}'
print(tf_rect_val)


# In[17]:


for user in users:
    if(user['name'] == 'ak'):
        persisted_face_id = CF.person.add_face('group_pictures/ak/ak_pic1.jpg', 
                                               "mm360_group1", 
                                               user['personId'], 
                                               user['name'],
                                               #f'{personGroupId} person data',
                                               tf_rect_val)
print(persisted_face_id)


# In[4]:


CF.person_group.get_status("mm360_group1")
#CF.person_group.get_status("skb-family")


# In[ ]:


# Test blocks
#take_picture()
#recogn_from_local_img(img_url)


# In[ ]:


#faces = identifyPerson('mm360_filename_2.jpg', "mm360_group1")
#print(faces)
#identifyPerson('mm360_filename_3.jpg', "mm360_group1")
#identifyPerson('mm360_filename.jpg', "mm360_group1")


# In[ ]:


#faces[0]['candidates'][0]


# In[ ]:


#CF.person.get("mm360_group1", '315369e7-7683-44ea-888e-b8e160d6717d')['name']


# In[59]:


#response = CF.face.detect('./mm360_filename.jpg', attributes='emotion')
# print(response[0]['faceAttributes']['emotion'])


# In[60]:


# responses = identifyPerson('mm360_filename.jpg', "mm360_group1")

