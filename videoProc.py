
import cv2
import time
import math as m
import mediapipe as mp
import matplotlib.pyplot as plt

from colors import*
from angles import*
from landmarks import*


fps=0
listDos=[]
listCou=[]

# Initialisation de la classe mediapipe pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()



# ===============================================================================================#

if __name__ == "__main__":

   def process(nom_fichier):
        bonnes_images = 0
        mauvaises_images = 0
        a=0
        b=0
        cou_c=0
        cou_inc=0
        dos_c=0
        dos_inc=0

        # Création de l'objet video_capture
        cap = cv2.VideoCapture(nom_fichier)

        # Métadonnées
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        largeur = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        hauteur = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        taille_frame = (largeur, hauteur)

        # Type de sortie vidéo
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_sortie = cv2.VideoWriter('res.mp4', fourcc, fps, taille_frame)
        
        if not cap.isOpened():
            print("Erreur lors de l'ouverture de la video")
            return
        else:
            print("video good")

        print('script begins')
        
        if not cap.isOpened():
                print("Error: Could not open video.")
                exit()
        
        while cap.isOpened():
            '''
            cap.read() retourne un tuple le remier element est success et l'autre element est image : 
                1) success indique si le frame a éte lit correctement
                2) image indique les données elles mêmes
            '''

            success, image = cap.read()
            if not success:
                print("Images nullex")
                break
            


            fps = cap.get(cv2.CAP_PROP_FPS)
            h, w = image.shape[:2]

            # Conversion de BGR en RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Traitement de l'image
            points_cles = pose.process(image)

            # Conversion de RGB en BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            '''
                ces deux lignes sont assez importants dans ce projet:
                    lm <-- comme variable va contenir les coordonnées des points clés détectés dans l'image.
                    inclure des parties du corps telles que les épaules, la cou, le dos ...
                
                Ces deux lignes permettent d'accéder aux données des points clés détectés dans l'image traitée (lm) 
                ainsi qu'à la classe de points clés prédéfinie (lmPose).
                Une fois ces données accessibles, elles peuvent être utilisées
                pour diverses tâches telles que l'analyse de la pose du corps, 
                la reconnaissance de gestes, etc.
            '''

            lm = points_cles.pose_landmarks
            lmPose = mp_pose.PoseLandmark

 
            inclinaison_cou = trouverAngle(x_eg, y_eg, x_og, y_og)
            inclinaison_torse = calculer_angle(x_ed, y_ed, x_hd, y_hd, x_gd, y_gd)
            listCou.append(round(abs(90-inclinaison_cou)))
            listDos.append(round(inclinaison_torse))
            
            cv2.circle(image, (x_od, y_od), 3, noir, -1)
            cv2.circle(image, (x_hd, y_hd), 3, rouge, -1)
            cv2.circle(image, (x_ed, y_ed), 3, noir, -1)
            cv2.circle(image, (x_ed, y_ed-100), 3, noir, -1)
            cv2.circle(image, (x_gd, y_gd), 3, noir, -1)
            
            
            if 80 < inclinaison_torse < 119:
                cv2.line(image, (x_hd, y_hd), (x_ed, y_ed), vert, 3)
                cv2.line(image, (x_hd, y_hd), (x_gd, y_gd), vert, 3)
                dos_c = dos_c+1
            else:
                cv2.line(image, (x_hd, y_hd), (x_ed, y_ed), rouge, 3)
                cv2.line(image, (x_hd, y_hd), (x_gd, y_gd), rouge, 3)
                dos_inc = dos_inc+1
                

            if 0 < inclinaison_cou < 25:
                cv2.line(image, (x_ed, y_ed), (x_od, y_od), vert, 3)
                cv2.line(image, (x_ed, y_ed -100), (x_ed, y_ed ), vert, 3)
                cou_c = cou_c+1
            else:
                cv2.line(image, (x_ed, y_ed), (x_od, y_od), rouge, 3)
                cv2.line(image, (x_ed, y_ed -100), (x_ed, y_ed ), rouge, 3)
                cou_inc = cou_inc+1
                
            texte_angle = 'Les angles: Cou : ' + str(int(inclinaison_cou)) + '  Dos : ' + str(int(inclinaison_torse))
            text_duree_cou  =  '% temps cou = '+str(round(100*cou_c / (a+1+b))) +"%" +" "+ str(round (1/fps * cou_c)) + "s"
            text_duree_dos  =  "% temps dos =" +  str(100*round(dos_c / (a+b+1))) + "%" + " " + str(round (1/fps * dos_c)) + "s" 
            cv2.putText(image, texte_angle, (10, 660), police, 1, noir, 2)
            cv2.putText(image, text_duree_cou, (10, 694), police, 1, noir, 2)
            cv2.putText(image, text_duree_dos, (10, 730), police, 1, noir, 2)
            cv2.putText(image, str(int(inclinaison_cou)), (x_eg + 10, y_eg), police, 0.5, noir, 2)
            cv2.putText(image, str(int(inclinaison_torse)), (x_hg + 10, y_hg), police, 0.5, noir, 2)
            
            if 0< inclinaison_cou < 25 and 70 < inclinaison_torse < 119:
                mauvaises_images = 0
                bonnes_images += 1
                a=a+1
                

                # Relier les points
                
                
              
                    

            else:
                bonnes_images = 0
                mauvaises_images += 1
                b=b+1

                # Relier les points


            # Calcul du temps de maintien dans une posture particulière
            temps_bonne_posture = (1 / fps) * a
            temps_mauvaise_posture =  (1 / fps) * mauvaises_images
            

            txt = 'Temps total : ' + str(round(((a+b)/fps))) + 's'
            cv2.putText(image, txt, (50, 120), police, 0.9, noir, 3)
            
            # Temps de posture
            if temps_bonne_posture > 0:
                texte_temps_bon = 'Correcte : ' + str(round(((a+b)/fps)*(a/(a+b)), 3)) + 's '+ str(round(a/(a+b)*100))+  '%'
                cv2.putText(image, texte_temps_bon, (50, 50), police, 0.9, noir, 3)
            else:
                texte_temps_mauvais = 'Incorrecte : ' + str(round(((a+b)/fps)*(b/(a+b)), 3)) + 's'
                cv2.putText(image, texte_temps_mauvais, (50, 50), police, 0.9, noir, 3)

            # Affichage
            cv2.imshow('Projet Slim et Amine', image)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
            if points_cles.pose_landmarks:
                lm = points_cles.pose_landmarks
            else:
                print("No landmarks detected.")
                continue  # Skip this frame

        
        print("poucentage correcte = ", a/(a+b)*100,  "%")
        print("poucentage incorrecte = " ,b/(a+b)*100,  "%")
        print("duree correcte = ", ((a+b)/(fps))*(a/(a+1+b))  )
        print("duree incorrecte = ", ((a+b)/(fps))*(b/(a+1+b))  )
        
        ind = []
        for i in range(a+b):
            ind.append(round(i/fps))


        
        
        
        
        cap.release()
        cv2.destroyAllWindows()
        return 'res.mp4'

process("correct.mp4")
