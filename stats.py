indices2 = range(len(listCou))
plt.figure(figsize=(8, 6))
plt.plot(indices2, listCou, marker='.', linestyle='-', color='b', label='Courbe Indices vs listCou')

# Ajout des titres et labels
plt.title('Présentation de la posture cou en fonction du temps et images')
plt.xlabel('Frames (images)')
plt.ylabel('Valeurs de listCou')
ax2 = plt.twiny()
ax2.set_xlabel('Temps(s)')

ax2.set_xticks(ind)
ax2.set_xticklabels(ind)
limit1 = 90  
limit2 = 70 # Example limit values
plt.axhline(y=limit1, color='g', linestyle='-', label=f'Limite Max {limit1}')
plt.axhline(y=limit2, color='r', linestyle='-', label=f'Tangente horizontale à {limit2}')
plt.legend('Posture cou')

plt.grid(True)
plt.show()


indices2 = range(len(listCou))
plt.figure(figsize=(8, 6))
plt.plot(indices2, listDos, marker='.', linestyle='-', color='b', label='Courbe Indices vs Angle')

plt.title('Présentation de la posture dos en fonction du temps et images')
plt.xlabel('Frames (images)')
plt.ylabel('Valeurs de listCou')
ax2 = plt.twiny()
ax2.set_xlabel('Temps(s)')

ax2.set_xticks(ind)
ax2.set_xticklabels(ind)

limit1 = 105
limit2 = 60 
plt.axhline(y=limit1, color='g', linestyle='-', label='Valeur Max')
plt.axhline(y=limit2, color='r', linestyle='-', label='Valeur Min')
plt.legend('Posture dos')

plt.grid(True)
plt.show()