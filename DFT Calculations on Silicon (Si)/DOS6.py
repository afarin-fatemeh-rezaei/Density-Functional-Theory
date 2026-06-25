import numpy as np
import matplotlib.pyplot as plt

energy, total_dos = np.loadtxt('si.dos.dat', usecols=(0, 1), unpack=True)

fermi_level = 5.7611
energy_shifted = energy - fermi_level  # Shift energies so Fermi level is at zero

plt.plot(energy_shifted, total_dos, color='red', label='Total DOS')
plt.xlabel('Energy (eV)')
plt.ylabel('DOS (states/eV)')
plt.title('Total Density of States')
plt.axvline(x=0, color='k', linestyle='--', label='Fermi Level')  
plt.legend()
plt.show()
