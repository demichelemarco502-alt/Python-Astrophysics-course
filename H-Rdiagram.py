#installation of the needed libraries
import matplotlib.pyplot as plt
import numpy as np

from astroquery.vizier import Vizier
import astropy.units as u
from astropy.coordinates import SkyCoord

!pip install astroquery
from google.colab import files
uploaded = files.upload()

#define the function to read the file
def read_columns_simple(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    columns_names = lines[0].split()

    data_lines = lines[3:]

    #lgL_index = 3
    #lgTeff_index = 4
    lgL_index = columns_names.index('lg(L)')
    lgTeff_index = columns_names.index('lg(Teff)')
    H1cen_index = columns_names.index('1H_cen')
    time_index = columns_names.index('time')


    lgL = []
    lgTeff = []
    H1cen = []
    time = []

    for line in data_lines:
        columns = line.split()
        lgL.append(float(columns[lgL_index]))
        lgTeff.append(float(columns[lgTeff_index]))
        H1cen.append(float(columns[H1cen_index]))
        time.append(float(columns[time_index]))

    return lgL,lgTeff,H1cen,time
  
#define a function that finds the first index below a certain threshold, related to hydrogen percentage
def trova_indice(lista, soglia):
    return next((i for i, valore in enumerate(lista) if valore < soglia))

#then I extract the temperature and the luminosity from the file
filename  = 'M001Z14V0 (1).dat'
filename2 = 'M002Z14V0 (1).dat'
filename09 = 'M0p8Z14V0.dat'
filename08 = 'M0p9Z14V0 (1).dat'

lgL,lgTeff,H1cen,time = read_columns_simple(filename)
lgL2,lgTeff2,H1cen2,time2 = read_columns_simple(filename2)
lgL08,lgTeff08,H1cen08,time08 = read_columns_simple(filename08)
lgL09,lgTeff09,H1cen09,time09 = read_columns_simple(filename09)

#I grasp the M67 data
m67_coords = SkyCoord(ra=132.825*u.deg, dec = 11.812*u.deg, frame='icrs')

radius=0.25*u.deg
vizier=Vizier()
result = vizier.query_region(m67_coords, radius=radius, catalog='I/345/gaia2')

lum=[]
teff=[]                   #ho creato due arrays per poter raccogliere dal database delle 50 stelle quelle che hanno misurate sia temperatura sia luminosita

for i in range(len(result[0][0])):
  lum.append(result[0][i][len(result[0][i])-1])
  teff.append(result[0][i][len(result[0][i])-5])
print(lum)
print()
print(teff)
print()
print(len(lum))
print(len(teff))

#Then I create the H-R diagram with matplotlib
plt.figure(figsize=(8,6))
plt.plot(lgTeff,lgL, 'bo-',label = '1Msun')
plt.plot(lgTeff2,lgL2, 'gs--',label = '2Msun')
plt.plot(lgTeff08,lgL08, 'bv-.', label = '08Msun')
plt.plot(lgTeff09,lgL09, 'k*:', label = '09Msun')


plt.xticks(size=15)     #posso anche introdurre una variabile size e metterlo dentro ai plt
plt.yticks(size=15)

#plt.plot(3.81,0.84, 'k*', markersize = 20, label = 'Procione')
#plt.plot(3.95,2.02, 'c*', markersize = 20, label = 'Alioth')
#plt.plot(4.08,5.08, 'b*', markersize = 20, label = 'Rigel')
#plt.plot(3.56,4.94, 'r*', markersize = 20, label = 'Betalgeuse')
#plt.errorbar(3.56,4.94, yerr = 0.3, xerr = 0.04, fmt = 'r*')
#plt.legend(bbox_to_anchor=(1.04,1), loc= 'upper left', prop={'size':12})     #loc regolato anche da numeri, convinene mettere la legenda fuori

filtered_lum = [np.log10(1) for l,t in zip(lum, teff) if 1 is not None and t is not None]
filtered_teff = [np.log10(t) for l,t in zip(lum, teff) if 1 is not None and t is not None]
plt.plot(filtered_teff, filtered_lum, 'b*', markersize=20, label = '  m67')
plt.legend(bbox_to_anchor=(1.04,1), loc='upper left', prop={'size':12})

plt.gca().invert_xaxis()
plt.xlabel('Teff [K]', fontsize=15)
plt.ylabel('lg(L) [Lsun]', fontsize=15)
plt.title('HR diagram')
plt.grid(True)
plt.show()


#comments on the graph, I'm interested in knowing the thresholds value (soglia), how fast the star burns the hydrogen.

soglia = [0.7,0.35,0.10]

indice = [trova_indice(H1cen,soglia) for soglia in soglie]
indice2 = [trova_indice(H1cen2,soglia) for soglia in soglie]

print('Gli indici sono:', indici)
print('Gli indici sono:', indici2)

Lum = []
for l in lgL:
  Lum.append(10**l)

Lum2 = []
for l in lgL2:
  Lum2.append(10**l)

Lum_targets = []
time_targets = []
for i in indici:
  Lum_targets.append(Lum[i])
  time_targets.append(time[i])

Lum_targets2 = []
time_targets2 = []
for i in indici2:
  Lum_targets2.append(Lum2[i])
  time_targets2.append(time2[i])

print()
print('I rapporti di luminosita, in questi rispettivi momenti, sono:', np.asarray(Lum_targets2)/np.asarray(Lum_targets))
print()
print('Con una stima approssimativa dei rapporti di eta, basata sulla')
print('luminosita media e le diverse masse iniziali, si ottiene: ', (2/Lum_targets2[1])/(1/Lum_targets[1]))

print('Mentre i rapporti di eta sono:', np.asarray(time_targets2)/np.asarray(time_targets))


