# DFT Class Exercises: Silicon & Aluminum

**First-principles calculations using Density Functional Theory (DFT) with Quantum ESPRESSO**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Projects](#projects)
  - [1. Silicon Band Structure & DOS](#1-silicon-band-structure--dos)
  - [2. Aluminum Convergence Study](#2-aluminum-convergence-study)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Results Summary](#results-summary)
- [Dependencies](#dependencies)
- [Acknowledgments](#acknowledgments)

---

## 📖 Overview

This repository contains two Density Functional Theory (DFT) projects completed as part of a **DFT course**, focusing on the **Quantum ESPRESSO** suite for first-principles materials simulations.

The projects cover two key areas of solid-state physics:

1. **Silicon (Si)** – Analysis of band structure, density of states (DOS), and projected density of states (PDOS)
2. **Aluminum (Al)** – Systematic convergence study of k-point grids, cutoff energies, and pseudopotential comparison

---

## 📁 Repository Structure

```
DFT_Class_Exercises/
├── Silicon/                              # Silicon calculations
│   ├── scf.in                            # SCF calculation
│   ├── nscf.in                           # NSCF calculation
│   ├── bands.in                          # Band structure input
│   ├── dos.in                            # DOS calculation
│   ├── pdos.in                           # PDOS calculation
│   ├── band.in                           # Band plotting input
│   ├── Si.pbe-n-kjpaw_psl.1.0.0.UPF      # Pseudopotential
│   ├── outdir/                           # Output directory
│   ├── Answers.pdf                       # Written analysis
│   └── README.md                         # Silicon project documentation
│
├── Aluminum/                             # Aluminum convergence study
│   ├── Input_template.in                 # Input file template
│   ├── run_all.sh                        # Automation script
│   ├── Al.pbesol-n-kjpaw_psl.1.0.0.UPF   # PBEsol pseudopotential
│   ├── Al.rel-pbe-nl-rrkjus_psl.1.0.0.UPF # Relativistic PBE pseudopotential
│   ├── Al-pbesol/                        # PBEsol results
│   │   ├── Al.scf.40.444.out
│   │   ├── Al.scf.40.666.out
│   │   ├── ... (all ecutwfc & k-grid combinations)
│   ├── Al-rel-pbe/                       # Relativistic PBE results
│   │   ├── Al.scf.40.444.out
│   │   ├── Al.scf.40.666.out
│   │   ├── ... (all ecutwfc & k-grid combinations)
│   ├── Analysis.pdf                      # Written analysis
│   └── README.md                         # Aluminum project documentation
│
└── README.md                             # This file
```

---

## 🔬 Projects

### 1. Silicon Band Structure & DOS

**Objective**: Calculate and analyze the electronic structure of bulk silicon.

#### Key Features

| Feature | Details |
|---------|---------|
| **Structure** | Diamond cubic (Fd3̄m), 2 atoms/unit cell |
| **Exchange-Correlation** | PBE-GGA |
| **Pseudopotential** | `Si.pbe-n-kjpaw_psl.1.0.0.UPF` (PBE, norm-conserving) |
| **Cutoff Energy** | 40 Ry |
| **k-point grid (SCF)** | 8×8×8 |
| **k-point grid (NSCF)** | 12×12×12 |
| **Band path** | Γ → X → K → L → Γ |

#### Results

| Quantity | Value |
|----------|-------|
| **Band Gap** | 0.6480 eV (DFT-PBE) |
| **VBM** | -0.0001 eV |
| **CBM** | 0.6479 eV |
| **Experimental Gap** | 1.1 eV (indirect) |

> **Note:** DFT-PBE underestimates the band gap (the well-known "band gap problem"), but the indirect nature of the gap is correctly predicted.

#### Workflow

```
SCF (scf.in) → NSCF (nscf.in) → DOS (dos.in) → Bands (bands.in) → PDOS (pdos.in)
```

#### Key Concepts Explored

- **Van Hove singularities** – Peaks in DOS from flat bands or degeneracies
- **Band gap classification** – Silicon as a semiconductor (finite gap)
- **PDOS** – Orbital contributions (s vs. p states)
- **Band dispersion** – Delocalized electrons (dispersive bands) vs. localized states (flat bands)

#### Documentation

See `Silicon/README.md` for detailed instructions, input files, and analysis.

---

### 2. Aluminum Convergence Study

**Objective**: Establish optimal computational parameters for bulk aluminum through systematic convergence testing.

#### Key Features

| Parameter | Tested Values |
|-----------|---------------|
| **Pseudopotentials** | PBEsol (PAW) vs. rel-PBE (USPP, spin-orbit) |
| **Cutoff Energy (ecutwfc)** | 40, 60, 100 Ry |
| **k-point grids** | 4×4×4, 6×6×6, 8×8×8, 10×10×10 |
| **Structure** | FCC, 1 atom/unit cell |
| **Lattice Constant** | 10.2 Bohr |

#### Results Summary

| Pseudopotential | ecutwfc (Ry) | Best k-grid | Total Energy |
|-----------------|--------------|-------------|--------------|
| PBEsol | 40-100 | 6×6×6 | -38.40445 Ry |
| rel-PBE | 40-100 | 6×6×6 | -4.93765 Ry |

#### Key Conclusions

1. **A 6×6×6 k-point grid** provides an optimal balance between accuracy and computational cost for aluminum.

2. **ecutwfc = 40 Ry** is sufficient; increasing to 60 or 100 Ry yields negligible energy changes (< 0.005 Ry).

3. **Absolute energy differences** between pseudopotentials stem from distinct energy references, not physical differences.

4. **Spin-orbit coupling** (rel-PBE) doubles the number of bands (nbnd=12 vs. nbnd=6) and increases computational cost, but is essential for materials with heavy elements.

#### Automation

The `run_all.sh` script automates all calculations:

```bash
#!/bin/bash
pseudos=("Al.pbesol-n-kjpaw_psl.1.0.0.UPF" "Al.rel-pbe-nl-rrkjus_psl.1.0.0.UPF")
k_grids=("4 4 4 0 0 0" "6 6 6 0 0 0" "8 8 8 0 0 0" "10 10 10 0 0 0")
ecut="40"  # Also tested: 60, 100
# ... (see Aluminum/run_all.sh for full script)
```

#### Documentation

See `Aluminum/README.md` for detailed instructions, input templates, and convergence analysis.

---

## 🛠️ Prerequisites

### Software
- **Quantum ESPRESSO** (v6.x or later)
- **Bash** (for running automation scripts)
- **Python/Matplotlib** (optional, for plotting results)

### Required Files
- Pseudopotential files (included in each project folder)
- Input templates (provided)

---

## 🚀 How to Run

### For Silicon Calculations

```bash
cd Silicon/

# 1. Run SCF
pw.x < scf.in > scf.out

# 2. Run NSCF (for DOS)
pw.x < nscf.in > nscf.out

# 3. Calculate DOS
dos.x < dos.in > dos.out

# 4. Calculate band structure
bands.x < bands.in > bands.out

# 5. Plot bands
band.x < band.in > band.out

# 6. Calculate PDOS
projwfc.x < pdos.in > pdos.out
```

### For Aluminum Convergence Study

```bash
cd Aluminum/

# 1. Make the script executable
chmod +x run_all.sh

# 2. Ensure pseudopotentials are in the correct location
# (Edit pseudo_dir path in input files if needed)

# 3. Run all calculations
./run_all.sh

# 4. Extract results
grep "!" Al-pbesol/Al.scf.40.*.out
grep "!" Al-rel-pbe/Al.scf.40.*.out
```

### Manual Run (Single Calculation)

```bash
# For any input file
pw.x -in Al.scf.40.101010.in > Al.scf.40.101010.out
```

---

## 📊 Results Summary

### Silicon

| Property | DFT Result | Experimental |
|----------|------------|--------------|
| Band Gap | 0.648 eV | 1.1 eV |
| Nature | Indirect | Indirect |
| Material Type | Semiconductor | Semiconductor |

### Aluminum

| Pseudopotential | Total Energy | ecutwfc Convergence | k-grid Convergence |
|-----------------|--------------|---------------------|---------------------|
| PBEsol | -38.40445 Ry | <0.005 Ry | 6×6×6 optimal |
| rel-PBE | -4.93765 Ry | <0.005 Ry | 6×6×6 optimal |

> **Note:** The energy difference between pseudopotentials is due to different **energy references** in the pseudopotential files, not physical differences in aluminum.

---

## 📦 Dependencies

| Software | Version | Purpose |
|----------|---------|---------|
| **Quantum ESPRESSO** | 6.x | DFT calculations (pw.x, dos.x, bands.x, projwfc.x) |
| **Bash** | 4.x | Automation scripts |
| **sed/awk** | - | Text processing |
| **Python** | 3.x | Plotting (optional) |
| **Matplotlib** | 3.x | Visualization (optional) |

### Installation

```bash
# Ubuntu/Debian
sudo apt-get install quantum-espresso

# Or compile from source
wget https://github.com/QEF/q-e/archive/refs/tags/qe-7.0.tar.gz
tar -xzf qe-7.0.tar.gz
cd q-e-qe-7.0
./configure
make all
```

---

## 📚 References

1. **Quantum ESPRESSO** – [https://www.quantum-espresso.org/](https://www.quantum-espresso.org/)

2. **Van Hove, L.** (1953). "The Occurrence of Singularities in the Elastic Frequency Distribution of a Crystal." *Phys. Rev.* **89**, 1189.

3. **Ashcroft, N. W. & Mermin, N. D.** (1976). *Solid State Physics*. Brooks Cole.

4. **Kittel, C.** (2004). *Introduction to Solid State Physics*, 8th Edition. Wiley.

5. **Martin, R. M.** (2020). *Electronic Structure: Basic Theory and Practical Methods*, 2nd Ed. Cambridge University Press.

6. **Perdew, J. P. et al.** (2008). "Restoring the Density-Gradient Expansion for Exchange in Solids and Surfaces." *Phys. Rev. Lett.* **100**, 136406.

7. **Methfessel, M. & Paxton, A. T.** (1989). "High-Precision Sampling for Brillouin-Zone Integration in Metals." *Phys. Rev. B* **40**, 3616.

---

## 🙏 Acknowledgments

These projects were completed as part of a **Density Functional Theory (DFT) course**, focusing on practical applications of first-principles calculations to understand the electronic structure and convergence behavior of materials.

---

**Happy Computing!** 🧮✨
