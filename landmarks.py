import mediapipe as mp
from videoProc import points_cles


'''
j'ai simplifié les noms des variables pour qu'ils ne soient pas assez longues
x_gg --> genou gauche dans l'axe des x
y_gg --> genou droite dans l'axe des y
y_ed --> épaule droite dans l'axe des y
x_hg --> hanche gauche dans l'axe des x
x_od --> oreille droite dans l'axe des x
et ainsi de suite 
'''

'''
ces lignes sont assez importants dans ce projet:
    lm <-- comme variable va contenir les coordonnées des points clés détectés dans l'image.
    inclure des parties du corps telles que les épaules, la cou, le dos ...

Ces lignes permettent d'accéder aux données des points clés détectés dans l'image traitée (lm) 
ainsi qu'à la classe de points clés prédéfinie (lmPose).
Une fois ces données accessibles, elles peuvent être utilisées
pour diverses tâches telles que l'analyse de la pose du corps, 
la reconnaissance de gestes, etc.
'''
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
lm = points_cles.pose_landmarks
lmPose = mp_pose.PoseLandmark





x_gg = int(lm.landmark[lmPose.LEFT_KNEE].x * w)
y_gg = int(lm.landmark[lmPose.LEFT_KNEE].y * h)


# Pour le genou droit
x_gd = int(lm.landmark[lmPose.RIGHT_KNEE].x * w)
y_gd = int(lm.landmark[lmPose.RIGHT_KNEE].y * h)

# Épaule gauche
x_eg = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
y_eg = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
# Épaule droite
x_ed = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
y_ed = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
# Oreille gauche
x_og = int(lm.landmark[lmPose.LEFT_EAR].x * w)
y_og = int(lm.landmark[lmPose.LEFT_EAR].y * h)

x_od = int(lm.landmark[lmPose.RIGHT_EAR].x * w)
y_od = int(lm.landmark[lmPose.RIGHT_EAR].y * h)
# Hanche gauche
x_hg = int(lm.landmark[lmPose.LEFT_HIP].x * w)
y_hg = int(lm.landmark[lmPose.LEFT_HIP].y * h)

x_hd = int(lm.landmark[lmPose.RIGHT_HIP].x * w) -50
y_hd = int(lm.landmark[lmPose.RIGHT_HIP].y * h)