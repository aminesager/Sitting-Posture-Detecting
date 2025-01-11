import math


def calculer_angle(xa, ya, xb, yb, xc, yc):
    # Calcul des longueurs des côtés du triangle
    cote_ab = m.sqrt((xb - xa)**2 + (yb - ya)**2)
    cote_bc = m.sqrt((xc - xb)**2 + (yc - yb)**2)
    cote_ac = m.sqrt((xc - xa)**2 + (yc - ya)**2)

    # Calcul des cosinus de l'angle ABC à l'aide de la loi des cosinus
    cos_angle_abc = (cote_ab**2 + cote_bc**2 - cote_ac**2) / (2 * cote_ab * cote_bc)

    # Calcul de l'angle en radians
    angle_radian = m.acos(cos_angle_abc)

    # Conversion de l'angle en radians en degrés
    angle_degre = m.degrees(angle_radian)
    return angle_degre




# Fonction pour calculer la distance euclidienne
def trouverDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

# Fonction mathématique qui calcule l'angle
def trouverAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degre = int(180 / m.pi) * theta
    return degre




