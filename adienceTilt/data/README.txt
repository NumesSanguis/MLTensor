**************************************************************************************************
*********  "Adience benchmark of unfiltered faces for gender and age classification"  ************


This database is comprised of face images, manually tagged for age, gender and anonymous identity (to be used in face recognition tasks).

The source images are public photos, taken by mobile devices, posted on Flickr (see License file for more details)

*** Project Homepage ***
Code and files available at:

http://www.openu.ac.il/home/hassner/Adience/



*******************************
** cross validation protocol **
*******************************
There are 5 folds (4 cross-validation folds, and one test).

Use the first 4 for validation, and the last for test results.

There are two kinds of folds, regular, and those of frontal faces only (yaw_angle ~= 0, as estimated by the part-based-detector)

Each fold gets a file, the first line of each file is the heading, and is self explanatory.

The fields for each face are:
user_id, original_image, face_id, age, gender, x, y, dx, dy, tilt_ang, fiducial_yaw_angle, fiducial_score

user_id - The Flickr user account. All the images for that account are under the subfolder with the same name
original_image - the filename. Unfortunately we are unable to provide a URL, as we only have the file name and there is no way to reproduce it from the API. A link to the account is provided for accrediting.
face_id - an identifier of a person, as tagged by us to be the same person (can be used for a "same-not-same" setting

x,y,dx,dy give a bounding box around a face

********************
*** tilt_ang     ***
********************
the parameter tilt_ang, describes the tilt of the face inside that box.

For example, if the angle is -90, than the face is tilted to the left, such that when looking at the photo you'll see:

Angles at intervals of 5 degrees are used. The angle is approximate.

Note: The bounding box is NOT to be rotated, 
      it describes a box drawn around a face in the image "as is" (== loaded from file without referring to any exif data)

ang = 0:

   o   o
     |
    ___
     
ang = -90:
  o
    --  |
  o   

ang = 90:

        o
  | --  
        o   

ang = 180:
    ___

     |
   o   o

****************************************
*** fiducial_yaw_ang, fiducial_score ***
****************************************

A Parts-based detector from http://www.ics.uci.edu/~xzhu/face/ was used here, after alighning the tilt angle
The results of the fiducial point detector is given here, without guarantee, with some heuristics

The fiducial score value minimum is 0,
a value of 40 and above indicates a good match
but even a value of around 20 has a good chance of being decent

The detector also supplies an estimate of the yaw angle, which we used to create the set of "Frontal" photos.

a result of 0 means frontal, while 90,-90 are left and right



****************************************
*** Dataset Statistics               ***
****************************************


*** -45 to 45 degrees folds ***
fold --- 0 ---
   users 34
   photos 3158
   faces 4272
   persons 480
fold --- 1 ---
   users 34
   photos 2429
   faces 3547
   persons 430
fold --- 2 ---
   users 34
   photos 2781
   faces 3714
   persons 411
fold --- 3 ---
   users 33
   photos 2309
   faces 3280
   persons 422
fold --- 4 ---
   users 33
   photos 2453
   faces 3703
   persons 541


*** frontal only folds ***

frontal fold --- 0 ---
   users 32
   photos 2403
   faces 3076
   persons 397
frontal fold --- 1 ---
   users 34
   photos 2261
   faces 2932
   persons 360
frontal fold --- 2 ---
   users 32
   photos 1785
   faces 2311
   persons 355
frontal fold --- 3 ---
   users 34
   photos 1814
   faces 2399
   persons 338
frontal fold --- 4 ---
   users 32
   photos 1667
   faces 2328
   persons 433
