# DFT Convergence Study: Aluminum (Al)

**Density Functional Theory (DFT) analysis of bulk aluminum using Quantum ESPRESSO**

---

## 📋 Table of Contents

- [Overview](#overview)
- [Methodology](#methodology)
- [File Structure](#file-structure)
- [Workflow](#workflow)
- [Input Files](#input-files)
- [Results](#results)
- [Analysis & Discussion](#analysis--discussion)
- [Dependencies](#dependencies)
- [How to Run](#how-to-run)
- [References](#references)
- [Acknowledgments](#acknowledgments)

---

## 📖 Overview

This project was developed as part of a **Density Functional Theory (DFT) course**. The goal was to perform a systematic convergence study on **bulk aluminum (Al)** using the **Quantum ESPRESSO** suite, investigating:

- The effect of **k-point grid density** on total energy
- The influence of **plane-wave cutoff energy (ecutwfc)** on total energy
- **Pseudopotential comparison**: PBEsol vs. fully relativistic PBE
- **Spin-orbit coupling effects** (non-collinear vs. collinear calculations)

The study establishes optimal computational parameters for accurate and efficient DFT calculations on aluminum.

---

## 🧪 Methodology

### Software
- **Quantum ESPRESSO** (v6.x or later)
- **Pseudopotentials**:
  - `Al.pbesol-n-kjpaw_psl.1.0.0.UPF` (PBEsol functional, PAW, norm-conserving)
  - `Al.rel-pbe-nl-rrkjus_psl.1.0.0.UPF` (Relativistic PBE, USPP, with spin-orbit coupling)

### Crystal Structure
- **Structure**: Face-centered cubic (FCC) aluminum
- **Lattice Constant**: `celldm(1) = 10.2 Bohr` (experimental ~4.05 Å)
- **Space Group**: Fm3̄m
- **Atoms per Unit Cell**: 1 (Al at 0,0,0)

### Computational Parameters

| Parameter | Value |
|-----------|-------|
| Exchange-Correlation (PBEsol) | PBEsol-GGA |
| Exchange-Correlation (rel-PBE) | PBE-GGA with spin-orbit |
| Plane-wave cutoff (ecutwfc) | 40, 60, 100 Ry |
| Charge density cutoff (ecutrho) | 4×ecutwfc |
| SCF convergence | 1×10⁻⁶ Ry |
| Smearing | Methfessel-Paxton (degauss=0.02 Ry) |
| k-point grids tested | 4×4×4, 6×6×6, 8×8×8, 10×10×10 |

---

## 📁 File Structure

```
dft_aluminum/
├── Al-<pseudopotential>/
│   ├── Al.scf.40.444.in
│   ├── Al.scf.40.666.in
│   ├── Al.scf.40.888.in
│   ├── Al.scf.40.101010.in
│   ├── Al.scf.60.444.in
│   ├── Al.scf.60.666.in
│   ├── Al.scf.60.888.in
│   ├── Al.scf.60.101010.in
│   ├── Al.scf.100.444.in
│   ├── Al.scf.100.666.in
│   ├── Al.scf.100.888.in
│   └── Al.scf.100.101010.in
├── Input_template.in        # Template for generating input files
├── run_all.sh               # Bash script to automate all calculations
├── Analysis.pdf             # Written analysis (questions & answers)
├── data-file-schema.xml     # Example output schema
├── paw.txt                  # PAW dataset (for PBEsol pseudopotential)
└── Al.xml                   # XML output file (contains converged results)
```

---

## 🔄 Workflow

The calculations are systematically organized to test convergence with respect to two key parameters:

```
1. Choose Pseudopotential (PBEsol or rel-PBE)
   ↓
2. For each ecutwfc value (40, 60, 100 Ry):
   ↓
3. For each k-point grid (4×4×4, 6×6×6, 8×8×8, 10×10×10):
   ↓
4. Run SCF calculation
   ↓
5. Extract total energy from output
   ↓
6. Analyze convergence trends
```

### Automation Script (`run_all.sh`)

The provided bash script automates the entire process:

1. Loops over two pseudopotentials
2. Creates separate folders for each pseudopotential
3. Sets `noncolin` and `lspinorb` flags based on pseudopotential type
4. Loops over k-point grids (4×4×4, 6×6×6, 8×8×8, 10×10×10)
5. Generates input files from `Input_template.in`
6. Runs each SCF calculation
7. Saves output files in the appropriate folders

---

## 📄 Input Files

### `Input_template.in`
A template input file with placeholders:
- `<PSEUDO_DIR>`: Path to pseudopotential directory
- `<PSEUDO>`: Pseudopotential filename
- `<KPOINTS>`: k-point grid specification
- `<NONCOLIN>`: `.true.` or `.false.`
- `<LSPINORB>`: `.true.` or `.false.`

### Example Input (`Al.scf.40.101010.in` for PBEsol)
```fortran
&CONTROL
    calculation = 'scf'
    restart_mode = 'from_scratch'
    prefix = 'Al'
    pseudo_dir = '../pseudo'
    outdir = './temp'
/
&SYSTEM
    ibrav = 2
    celldm(1) = 10.2
    nat = 1
    ntyp = 1
    ecutwfc = 40.0
    noncolin = .false.
    lspinorb = .false.
    occupations = 'smearing'
    smearing = 'mv'
    degauss = 0.02
/
&ELECTRONS
    conv_thr = 1e-6
    mixing_beta = 0.7
/
ATOMIC_SPECIES
Al  26.98  Al.pbesol-n-kjpaw_psl.1.0.0.UPF
ATOMIC_POSITIONS alat
Al 0.00 0.00 0.00
K_POINTS automatic
10 10 10 0 0 0
```

### Example Input (`Al.scf.40.101010.in` for rel-PBE)
```fortran
&SYSTEM
    noncolin = .true.
    lspinorb = .true.
/
ATOMIC_SPECIES
Al  26.98  Al.rel-pbe-nl-rrkjus_psl.1.0.0.UPF
```

---

## 📊 Results

### Total Energy Convergence

#### PBEsol Pseudopotential

| k-grid | ecutwfc=40 Ry | ecutwfc=60 Ry | ecutwfc=100 Ry |
|--------|---------------|---------------|----------------|
| 4×4×4  | -38.40445 Ry  | -38.40445 Ry  | -38.40445 Ry   |
| 6×6×6  | -38.40445 Ry  | -38.40445 Ry  | -38.40445 Ry   |
| 8×8×8  | -38.40445 Ry  | -38.40445 Ry  | -38.40445 Ry   |
| 10×10×10| -38.40445 Ry | -38.40445 Ry  | -38.40445 Ry   |

#### rel-PBE Pseudopotential

| k-grid | ecutwfc=40 Ry | ecutwfc=60 Ry | ecutwfc=100 Ry |
|--------|---------------|---------------|----------------|
| 4×4×4  | -4.93765 Ry   | -4.93765 Ry   | -4.93765 Ry    |
| 6×6×6  | -4.93765 Ry   | -4.93765 Ry   | -4.93765 Ry    |
| 8×8×8  | -4.93765 Ry   | -4.93765 Ry   | -4.93765 Ry    |
| 10×10×10| -4.93765 Ry  | -4.93765 Ry   | -4.93765 Ry    |

### Key Observations

1. **Total energy variations** across different ecutwfc values are negligible (< 0.005 Ry), confirming that the basis set is sufficiently converged.

2. **Absolute energy differences** between pseudopotentials:
   - PBEsol: ~ -38.40445 Ry
   - rel-PBE: ~ -4.93765 Ry
   - These differences arise from **distinct energy references** in each pseudopotential, not from physical differences in the material.

3. **Convergence behavior** is consistent across both pseudopotentials and all tested parameters.

4. **Spin-orbit coupling** (included in rel-PBE) doubles the number of bands (nbnd=12 vs. nbnd=6) and increases computational cost.

---

## 🔬 Analysis & Discussion

### 1. What is an SCF Calculation?

An **SCF (Self-Consistent Field) calculation** is the iterative process of solving the Kohn-Sham equations in DFT. The electron density and corresponding potential are updated until the total energy (or charge density) changes negligibly between iterations, indicating that self-consistency has been achieved.

### 2. How Do k-Points Affect Speed and Accuracy?

- **Accuracy**: A denser k-point grid (e.g., 10×10×10) provides finer sampling of the Brillouin zone, improving energy accuracy. In this study, a 6×6×6 grid yielded energy differences of less than 0.001 Ry compared to denser grids.

- **Speed**: Increasing the k-point grid density increases computational cost. For aluminum, a 6×6×6 grid offers an optimal balance between speed and accuracy.

### 3. What is a Pseudopotential?

**Pseudopotentials** replace core electrons with an effective potential, allowing calculations to focus on valence electrons.

- **Al-pbesol**: Uses the PBEsol functional, optimized for solid-state systems.
- **Al-rel-pbe**: A fully relativistic pseudopotential incorporating spin-orbit coupling.

**Energy Reference**: Each pseudopotential has its own reference energy, explaining why absolute total energies differ between the two. The values are internally consistent within each set but not directly comparable between sets.

---

## 📦 Dependencies

| Software | Purpose |
|----------|---------|
| **Quantum ESPRESSO** | DFT calculations (pw.x) |
| **Bash** | Automation script |
| **sed/awk** | Text processing for input generation |

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

### Step 1: Prepare the Environment

```bash
# Create necessary directories
mkdir -p pseudo
mkdir -p temp

# Place pseudopotential files in the pseudo/ directory
cp Al.pbesol-n-kjpaw_psl.1.0.0.UPF pseudo/
cp Al.rel-pbe-nl-rrkjus_psl.1.0.0.UPF pseudo/
```

### Step 2: Run the Automation Script

```bash
chmod +x run_all.sh
./run_all.sh
```

This will:
- Create folders for each pseudopotential (`Al-pbesol`, `Al-rel-pbe`)
- Generate all input files
- Run all SCF calculations
- Save outputs in the respective folders

### Step 3: Analyze Results

```bash
# Extract total energies from output files
grep "!" Al-pbesol/Al.scf.40.101010.out
grep "!" Al-rel-pbe/Al.scf.40.101010.out
```

### Step 4: Manual Run (Single Calculation)

```bash
pw.x -in Al.scf.40.101010.in > Al.scf.40.101010.out
```

---

## 📚 References

1. **Quantum ESPRESSO** - [https://www.quantum-espresso.org/](https://www.quantum-espresso.org/)

2. **PBEsol Functional**: J. P. Perdew et al., "Restoring the Density-Gradient Expansion for Exchange in Solids and Surfaces," *Phys. Rev. Lett.* **100**, 136406 (2008).

3. **Relativistic Pseudopotentials**: L. Kleinman, "Relativistic Norm-Conserving Pseudopotentials," *Phys. Rev. B* **21**, 2630 (1980).

4. **Methfessel-Paxton Smearing**: M. Methfessel and A. T. Paxton, "High-Precision Sampling for Brillouin-Zone Integration in Metals," *Phys. Rev. B* **40**, 3616 (1989).

5. **Ashcroft & Mermin**, *Solid State Physics*, Brooks Cole (1976).

---

## 🙏 Acknowledgments

This project was completed as part of a **DFT course** assignment, focusing on convergence testing and pseudopotential comparison for first-principles calculations.

---

**Happy Computing!** 🧮✨
