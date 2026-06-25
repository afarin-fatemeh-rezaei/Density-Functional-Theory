import numpy as np
import matplotlib.pyplot as plt

def read_qe_bands_dat(filename):
    
    with open(filename, 'r') as f:
        lines = f.readlines()

    band_energies = []
    kpoints = []
    i = 0
    num_bands_per_kpoint = None

    while i < len(lines):
        line = lines[i].strip()
       
        if line.startswith('&plot') or line == '':
            i += 1
            continue

        
        parts = line.split()
        if len(parts) == 3:
            
            i += 1
            bands_lines = []
           
            while i < len(lines):
                next_line = lines[i].strip()
                
                if next_line == '' or next_line.startswith('&plot') or len(next_line.split())==3:
                    break
                bands_lines.append(next_line)
                i += 1

            
            energies = []
            for bl in bands_lines:
                energies.extend([float(x) for x in bl.split()])

            if num_bands_per_kpoint is None:
                num_bands_per_kpoint = len(energies)
            else:
                assert len(energies) == num_bands_per_kpoint, "Inconsistent number of bands per k-point"

            band_energies.append(energies)
            kpoints.append(len(kpoints))  # just indices 0,1,2,...

        else:
            # Unexpected line, skip
            i += 1

    band_energies = np.array(band_energies)
    kpoints = np.array(kpoints)

    return kpoints, band_energies

# Usage

bands_file = 'si.bands.dat'
kpoints, bands = read_qe_bands_dat(bands_file)

# Fermi level 
fermi_energy =5.7611



plt.figure(figsize=(8,6))
for band_idx in range(bands.shape[1]):
    plt.plot(kpoints, bands[:, band_idx] - fermi_energy, color='b')

plt.axhline(0, color='k', linestyle='--', linewidth=1, label='Fermi level')
plt.xlabel('K-point index')
plt.ylabel('Energy (eV)')
plt.title('Band Structure')
plt.legend()
plt.tight_layout()
plt.show()



# Align bands relative to Fermi energy
aligned_bands = bands - fermi_energy

# For each k-point find highest occupied and lowest unoccupied energies
vbm_per_k = []
cbm_per_k = []

for k in range(aligned_bands.shape[0]):
    energies = aligned_bands[k, :]
    # Occupied states ≤ 0 eV
    occupied = energies[energies <= 0]
    # Unoccupied states > 0 eV
    unoccupied = energies[energies > 0]

    if len(occupied) > 0:
        vbm_per_k.append(np.max(occupied))
    else:
        # If no occupied states? Append a very low number
        vbm_per_k.append(-np.inf)

    if len(unoccupied) > 0:
        cbm_per_k.append(np.min(unoccupied))
    else:
        cbm_per_k.append(np.inf)

vbm = np.max(vbm_per_k)
cbm = np.min(cbm_per_k)

band_gap = cbm - vbm

print(f"Valence Band Maximum (VBM): {vbm:.4f} eV")
print(f"Conduction Band Minimum (CBM): {cbm:.4f} eV")
print(f"Band Gap: {band_gap:.4f} eV")
