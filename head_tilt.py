import cv2
import mediapipe as mp
import numpy as np
import time

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

drawing_spec = mp_drawing.DrawingSpec(thickness=None, circle_radius=0)


video = cv2.VideoCapture(0)

while video.isOpened():
    success, image = video.read()

    start = time.time()

    # Flip the image horizontally for a later selfie-view display
    #  convert the color from BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance
    image.flags.writeable = False
    
   
    results = face_mesh.process(image)
    
    # To improve performance
    image.flags.writeable = True
    
    #  from RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    #  2D Coordinates
                    face_2d.append([x, y])

                    # 3D Coordinates
                    face_3d.append([x, y, lm.z])       
            
            # Convert it to NumPy array
            face_2d = np.array(face_2d, dtype=np.float64)

            # Convert it to NumPy array
            face_3d = np.array(face_3d, dtype=np.float64)

            # camera matrix
            focal_length = 1 * img_w

            cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                    [0, focal_length, img_w / 2],
                                    [0, 0, 1]])

            # distortion parameters
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            # Solve PnP
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            # Get rotational matrix
            rmat, jac = cv2.Rodrigues(rot_vec)

            # Get angles
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            # Get the y rotation degree
            x = angles[0] * 360
            y = angles[1] * 360
            z = angles[2] * 360
          

           
            if y < -10:
                print("Left")
                text = "Left"
            elif y > 10:
                print("Right")
                text = "Right"
            elif x < -10:
                print("Brake")
                text = "Brake"
            elif x > 10:
                print("Accelerate")
                text = "Accelerate"
            else:
                print("Go")
                text = "Go"

            
            cv2.putText(image, text, (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
            


        end = time.time()
        totalTime = end - start

        #fps = 1 / totalTime
        #print("FPS: ", fps)

        

        mp_drawing.draw_landmarks(
                      image,
                     landmark_list=face_landmarks,
                     landmark_drawing_spec=drawing_spec,
                     connection_drawing_spec=drawing_spec)
      


    cv2.imshow('Head Pose Estimation', image)

   
    k = cv2.waitKey(1)
    # press q for close
    if k == ord('q'):
        break


video.release()
cv2.destroyAllWindows()