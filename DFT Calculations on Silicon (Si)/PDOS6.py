import numpy as np
import matplotlib.pyplot as plt

fermi_level = 5.7611  # Fermi level

# -------- PDOS for atom 1 & atom 2 shown separately--------

files_atom1 = {
    'Atom 1 s orbital': 'si.pdos_atm#1(Si)_wfc#1(s)',
    'Atom 1 p orbital': 'si.pdos_atm#1(Si)_wfc#2(p)',
}

files_atom2 = {
    'Atom 2 s orbital': 'si.pdos_atm#2(Si)_wfc#1(s)',
    'Atom 2 p orbital': 'si.pdos_atm#2(Si)_wfc#2(p)',
}

def plot_pdos(files, atom_label):
    plt.figure(figsize=(7,5))
    for label, filename in files.items():
        try:
            data = np.loadtxt(filename)
            energy = data[:,0] - fermi_level  # Shift energy axis 
            pdos = data[:,1]
            plt.plot(energy, pdos, label=label)
        except Exception as e:
            print(f"Could not load {filename}: {e}")
    plt.axvline(x=0, color='k', linestyle='--', label='Fermi level (0 eV)')  # Fermi level 
    plt.xlabel('Energy (eV)')
    plt.ylabel('PDOS (states/eV)')
    plt.title(f'Projected DOS for {atom_label}')
    plt.legend()
    plt.grid(True)
    plt.show()

plot_pdos(files_atom1, 'Atom 1')
plot_pdos(files_atom2, 'Atom 2')

# -------- total DOS VS summed PDOS --------

data = np.loadtxt('si.pdos_tot')
energy = data[:, 0] - fermi_level  # Shift energies 
dos_total = data[:, 1]
pdos_sum = data[:, 2]

plt.figure(figsize=(7,5))
plt.plot(energy, dos_total, label='Total DOS', color='red', linewidth=2)
plt.plot(energy, pdos_sum, label='Sum of PDOS', color='blue', linestyle='--', linewidth=2)
plt.axvline(x=0, color='k', linestyle=':', label='Fermi level (0 eV)')  # Fermi level at zero
plt.xlabel('Energy (eV)')
plt.ylabel('Density of States (states/eV)')
plt.title('Total DOS and Sum of Projected DOS')
plt.legend()
plt.grid(True)
plt.show()
