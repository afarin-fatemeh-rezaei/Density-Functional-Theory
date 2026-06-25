# DFT Calculations on Silicon (Si)

**Density Functional Theory (DFT) analysis of bulk silicon using Quantum ESPRESSO**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Methodology](#methodology)
- [File Structure](#file-structure)
- [Workflow](#workflow)
- [Input Files](#input-files)
- [Results](#results)
  - [Band Structure](#band-structure)
  - [Density of States (DOS)](#density-of-states-dos)
  - [Projected Density of States (PDOS)](#projected-density-of-states-pdos)
- [Analysis & Discussion](#analysis--discussion)
- [Dependencies](#dependencies)
- [How to Run](#how-to-run)
- [References](#references)
- [Acknowledgments](#acknowledgments)

---

## 📖 Overview

This project was developed as an assignment for a **Density Functional Theory (DFT) course**. The goal was to perform *ab initio* calculations on bulk **silicon (Si)** using the **Quantum ESPRESSO** suite, analyzing its electronic structure through:

- **Band structure**
- **Total Density of States (DOS)**
- **Projected Density of States (PDOS)**

The calculations were performed using the **Perdew-Burke-Ernzerhof (PBE)** exchange-correlation functional within the generalized gradient approximation (GGA).

---

## 🧪 Methodology

### Software
- **Quantum ESPRESSO** (v6.x or later)
- **Pseudopotential**: `Si.pbe-n-kjpaw_psl.1.0.0.UPF` (PBE, norm-conserving)

### Crystal Structure
- **Structure**: Diamond cubic (silicon)
- **Lattice Constant**: `celldm(1) = 10.410909236 Bohr` (~5.43 Å, experimental)
- **Space Group**: Fd3̄m
- **Atoms per Unit Cell**: 2 (Si at 0,0,0 and 0.25,0.25,0.25)

### Computational Parameters
| Parameter | Value |
|-----------|-------|
| Exchange-Correlation | PBE-GGA |
| Plane-wave cutoff (ecutwfc) | 40 Ry |
| Charge density cutoff (ecutrho) | 320 Ry |
| Number of bands (nbnd) | 8 |
| SCF convergence | 1×10⁻⁸ |
| k-point grid (SCF) | 8×8×8 |
| k-point grid (NSCF) | 12×12×12 |

---

## 📁 File Structure

```
dft_silicon/
├── scf.in                # Self-consistent field calculation
├── nscf.in               # Non-self-consistent field calculation
├── bands.in              # Band structure calculation
├── dos.in                # Density of states calculation
├── pdos.in               # Projected density of states calculation
├── band.in               # Band plotting input
├── Answers.pdf           # Written analysis (questions & answers)
├── Si.pbe-n-kjpaw_psl.1.0.0.UPF  # Pseudopotential file
└── outdir/               # Output directory (generated)
    ├── si.save/          # SCF output files
    ├── si.bands.dat      # Band structure data
    ├── si.dos.dat        # DOS data
    └── si.pdos_atm*      # PDOS data files
```

---

## 🔄 Workflow

The standard Quantum ESPRESSO workflow consists of the following steps:

```
1. SCF Calculation (scf.in)
   ↓
2. NSCF Calculation (nscf.in) → For DOS with tetrahedra method
   ↓
3. DOS Calculation (dos.in)
   ↓
4. Bands Calculation (bands.in + band.in)
   ↓
5. PDOS Calculation (pdos.in)
```

### Step-by-Step Execution

1. **Run SCF** (self-consistent field) to obtain the charge density:
   ```bash
   pw.x < scf.in > scf.out
   ```

2. **Run NSCF** (non-self-consistent) with tetrahedra occupations for accurate DOS:
   ```bash
   pw.x < nscf.in > nscf.out
   ```

3. **Calculate DOS**:
   ```bash
   dos.x < dos.in > dos.out
   ```

4. **Calculate Band Structure**:
   ```bash
   bands.x < bands.in > bands.out
   ```

5. **Plot Bands** (generates `si.bands.dat`):
   ```bash
   band.x < band.in > band.out
   ```

6. **Calculate PDOS** (projected DOS):
   ```bash
   projwfc.x < pdos.in > pdos.out
   ```

---

## 📄 Input Files

### `scf.in` (Self-Consistent Field)
Calculates the ground-state charge density.
- 8×8×8 k-point grid
- Converges to 1×10⁻⁸ Ry

### `nscf.in` (Non-Self-Consistent Field)
Uses the converged charge density from SCF.
- 12×12×12 k-point grid (finer mesh)
- `occupations='tetrahedra'` for accurate DOS integration

### `bands.in` (Band Structure)
- Path through high-symmetry points:
  - Γ (0,0,0) → X (0,0.5,0) → K (-0.5,0,-0.5) → L (-0.375,0.25,-0.375) → Γ

### `dos.in` (Density of States)
- Energy range: -9.0 to 16.0 eV
- Uses `dos.x` to compute total DOS

### `pdos.in` (Projected DOS)
- Projects DOS onto atomic orbitals
- Energy range: -15 to 15 eV

---

## 📊 Results

### Band Structure

The band structure calculation yields the **indirect band gap** of silicon:

| Quantity | Value |
|----------|-------|
| **Band Gap** | 0.6480 eV (DFT-PBE) |
| **Valence Band Maximum (VBM)** | -0.0001 eV |
| **Conduction Band Minimum (CBM)** | 0.6479 eV |

> **Note:** DFT-PBE underestimates the band gap compared to the experimental value of **1.1 eV** (at room temperature). This is a known limitation of DFT (band gap problem).

### Density of States (DOS)

The total DOS plot (Figure 1 in `Answers.pdf`) shows:

- **Peaks** (Van Hove singularities): Occur at energies where the band structure is **flat** or **degenerate**, resulting in many states at the same energy.
- **Valleys**: Regions with few available states.
- **Band gap**: Clear separation between valence and conduction bands.

### Projected Density of States (PDOS)

PDOS analysis reveals the **orbital contributions**:

- **Atom 1** (Si at 0,0,0): Shows contributions from s and p orbitals.
- **Atom 2** (Si at 0.25,0.25,0.25): Equivalent contributions due to symmetry.

The PDOS allows identification of which atomic orbitals contribute to different parts of the electronic spectrum, providing insight into **chemical bonding** and **optical properties**.

### Figures from `Answers.pdf`

1. **Figure 1**: Total DOS showing Van Hove singularities
2. **Figure 2**: Band structure showing band gap
3. **Figure 3**: Atom 1 PDOS
4. **Figure 4**: Atom 2 PDOS
5. **Figure 5**: Comparison between DOS and PDOS

---

## 🔬 Analysis & Discussion

### 1. Relationship Between DOS and Band Structure

**(a)** Peaks in the DOS arise at energies where there are **many bands very close in energy**, often due to band degeneracy or flatness. These correspond to **Van Hove singularities** [1]—critical points (maxima, minima, saddle points) in the band structure.

**(b)** **Flat bands** (little dispersion with \(k\)) result in a large accumulation of electronic states at a given energy, leading to **pronounced peaks** in the DOS [2, 4].

### 2. Conductivity Analysis

**(a)** The energy gap between VBM and CBM defines the fundamental band gap. For silicon:
- Experimental: ~1.1 eV (indirect)
- DFT-PBE (this calculation): 0.6480 eV

**(b)** **Silicon is a semiconductor** because:
- Finite band gap (0.648 eV)
- Fermi energy lies within the gap
- If bands overlapped → metallic; if gap is several eV → insulator [2].

### 3. Interpretation of DOS, PDOS, and Band Structure

**(a)** **DOS**: Shows distribution of electronic states across energies. Peaks = many available states; valleys = few states.

**(b)** **PDOS**: Separates contributions from different atomic orbitals or atoms. Reveals bonding and optical properties.

**(c)** **Band Structure**: Shows how electron energies vary with momentum.
- **Dispersive bands** (steep slopes) = delocalized electrons, high mobility
- **Flat bands** = localized states, high effective mass
- **Band gap** = classification as metal, semiconductor, or insulator [2, 3].

---

## 📦 Dependencies

| Software | Purpose |
|----------|---------|
| **Quantum ESPRESSO** | DFT calculations (pw.x, dos.x, bands.x, projwfc.x) |
| **Python / Matplotlib** | Plotting (optional, for visualization) |
| **XCRYSDEN** | Structural visualization (optional) |

### Installation

```bash
# Install Quantum ESPRESSO (Ubuntu/Debian)
sudo apt-get install quantum-espresso

# Or compile from source:
wget https://github.com/QEF/q-e/archive/refs/tags/qe-7.0.tar.gz
tar -xzf qe-7.0.tar.gz
cd q-e-qe-7.0
./configure
make all
```

---

## 🚀 How to Run

1. **Ensure the pseudopotential file** (`Si.pbe-n-kjpaw_psl.1.0.0.UPF`) is in the same directory.

2. **Create the output directory**:
   ```bash
   mkdir -p outdir
   ```

3. **Run the calculations in order**:
   ```bash
   pw.x < scf.in > scf.out
   pw.x < nscf.in > nscf.out
   dos.x < dos.in > dos.out
   bands.x < bands.in > bands.out
   band.x < band.in > band.out
   projwfc.x < pdos.in > pdos.out
   ```

4. **Extract data**:
   - Band structure: `outdir/si.bands.dat`
   - DOS: `outdir/si.dos.dat`
   - PDOS: `outdir/si.pdos_atm*`

5. **Plot results** using your preferred plotting tool (Matplotlib, Gnuplot, XCRYSDEN).

---

## 📚 References

1. L. Van Hove, "The Occurrence of Singularities in the Elastic Frequency Distribution of a Crystal," *Phys. Rev.* **89**, 1189 (1953).

2. N. W. Ashcroft and N. D. Mermin, *Solid State Physics*, Brooks Cole (1976).

3. C. Kittel, *Introduction to Solid State Physics*, 8th Edition, Wiley (2004).

4. R. M. Martin, *Electronic Structure: Basic Theory and Practical Methods*, 2nd Ed., Cambridge University Press (2020).

---

## 🙏 Acknowledgments

This project was completed as part of a **DFT course** assignment, focusing on the practical application of first-principles calculations to understand the electronic structure of materials.

---

**Happy Computing!** 🧮✨
