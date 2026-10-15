# NASA ACME Microgravity Combustion Research
## Hybrid CAD Engineering, Reactive Flow Simulation, and Physics-Informed Machine Learning

---

### Abstract

This repository provides an integrated computational framework for the reconstruction, simulation, and predictive modeling of microgravity combustion phenomena, developed around the NASA Physical Sciences Informatics (PSI-23) dataset for the ACME (Advanced Combustion via Microgravity Experiments) research initiative conducted aboard the International Space Station (ISS). 

The platform bridges physical flight hardware and predictive artificial intelligence across three core engineering pillars:
1. **Hybrid Computer-Aided Design (CAD) Reconstruction:** Dual-track aeromechanical modeling combining automated parametric scripting via the Autodesk Inventor Python API for regular rotational geometries, paired with extensive manual reverse-engineering and precision CAD modeling by Emerson B. J. for high-complexity aerospace components exhibiting intricate GD&T, non-trivial Datums, and multi-feature intersections that exceeded automated procedural generation.
2. **Computational Fluid Dynamics (CFD):** Geometric boundary formulation and porous-media zona optimization targeting high-fidelity reactive flow simulations in ANSYS Fluent.
3. **Machine Learning & Physics-Informed Neural Networks (PINN):** Computer vision extraction of spatial flame dynamics from raw ISS diagnostic video streams paired with surrogate neural architectures (PINN, Bayesian PINN, and Support Vector Regression) for non-intrusive prediction of thermodynamic signatures and radiative flux.

---

### 1. Experimental Dataset & Context (NASA PSI-23)

The experimental foundation of this work is derived from the NASA ACME s-Flame (Spherical Diffusion Flame) mission series executed within the Combustion Integrated Rack (CIR) on the ISS. The mission evaluated spherical and burner-stabilized diffusion flames under microgravity conditions ($10^{-6}\;g$), isolating pure diffusion and radiative mechanisms from buoyant convective upward draft.

#### Target Test Ensembles for CFD Calibration and AI Benchmark:
* **Test ID 19304 (Nominal Baseline):** 45% methane ($CH_4$) dilution. Stable laminar spherical regime providing clean baseline boundary conditions for fundamental transport calibration.
* **Test ID 19352 (Dynamic Instability):** 100% pure fuel injection at critical low Lewis numbers ($Le < 1$), yielding cellular flame structure, spontaneous oscillations, and edge-extinction dynamics.
* **Test ID 20176 (High-Radiative Stress):** 30% fuel dilution producing dense soot formation where thermal radiation dominates the total chamber heat transfer balance due to the absence of buoyant exhaust removal.

---

### 2. Burner CAD Architecture: Hybrid Automated & Expert Manual Synthesis

The physical burner hardware consists of a coaxial multi-component assembly designed for precise reactant delivery and laminar flow conditioning. Due to the high geometric diversity and stringent aerospace tolerances across the 39 individual Manufacturing Drawings (MFD), a strict division of modeling methodologies was implemented:

#### Algorithmic Automation vs. Manual Engineering Division:
* **Automated Procedural Scripting (Python + Autodesk Inventor API):** Utilized for axisymmetric baseline geometries, standard cylindrical envelopes, concentric through-hole arrays, automated material assignment, and bulk generation of intermediate STEP/IPT files.
* **Expert Manual Modeling (Emerson B. J.):** The most geometrically demanding and critical components could not be successfully resolved via automated scripts. Intricate aerospace GD&T specifications—such as compound asymmetric shoulders, tight true-position callouts relative to compound Datums (A, B, and C), delicate thin-wall retention tabs ($0.016"$), and non-uniform boundary sleeves—required dedicated manual modeling, spatial interpretation, and manual reverse engineering directly inside Autodesk Inventor to ensure absolute dimensional fidelity to NASA flight prints.

#### Key Geometry Specifications (Series S1100 to S1109):
* **S1101MFD1237 (BRE Flow Screen Sleeve):** High-complexity boundary sleeve with asymmetric shoulder geometry ($1.962"$ outer diameter, $0.016"$ wall thickness), dual alignment slots, and integrated tab features (manually modeled and resolved by Emerson B. J.).
* **S1101MFD1238 (BRE 50 mm Flow Screen):** High-mesh planar diffusion screen featuring a precision central bore ($\varnothing 0.320"$) and secondary probe passage ($\varnothing 0.161"$) maintained at true position tolerances.
* **S1101MFD1239 (BRE 50 mm Flow Straightener):** Ceramic core ($Al_2O_3$ Alumina) with an outer diameter of $\varnothing 1.960" \pm .005"$ and an axial length of $0.984" \pm .005"$, providing flow conditioning across 400 cells per square inch (cpsi) with two $\varnothing 0.161"$ probe clearance passages.

#### Model Export Standards:
* Native Parametric CAD: Autodesk Inventor Part (`.ipt`)
* Standard for the Exchange of Product Model Data: STEP AP214 (`.stp`) for universal multi-physics solver compatibility.

---

### 3. Simulation Strategy for ANSYS Fluent (CFD)

Direct geometric discretization of the microscopic honeycomb cells (over 1,100 square passages of $0.040"$) introduces severe mesh skewness, non-conformal cell interfaces, and excessive node counts exceeding $10^7$ elements for a single component. 

To maintain numerical stability, strict convergence rates, and grid independence:
* **Porous Media Approximation:** The flow straightener core is modeled as an equivalent continuous porous fluid domain (`Porous Zone`) characterized by directional viscous resistance ($1/\alpha$) and inertial loss factors ($C_2$) calculated via the Ergun porous media equation adjusted for square micro-channels.
* **Geometric Discretization:** The physical envelope and probe passages ($\varnothing 0.161"$) are preserved as exact boundary representations, guaranteeing exact mass flow continuity and heat conduction interfaces into the burner exterior walls.

---

### 4. Computer Vision, Machine Learning, and Surrogate Models

Telemetry logs provided in the NASA dataset do not explicitly report instantaneous flame radius or spatial boundary progression. To establish a multimodal dataset for physics-informed modeling, a specialized diagnostic pipeline was deployed:

#### Computer Vision Boundary Extraction:
* Automated frame extraction from low-light UV and visual spectrum camera feeds (.hobj / compressed video containers).
* Threshold segmentation and adaptive morphological contouring to track instantaneous flame front radius, luminous boundary growth rates, and extinction diameters.

#### Predictive Machine Learning Architectures:
* **Physics-Informed Neural Networks (PINNs):** Deep neural networks regularized with the governing differential equations of 1D spherical diffusion flames (species transport and energy conservation) to predict continuous temperature fields from sparse sensor readings.
* **Bayesian PINN:** Quantification of parametric uncertainty arising from microgravity sensor noise and micro-flow fluctuations.
* **Support Vector Regression (SVR):** Fast surrogate evaluation mapping chamber pressure and inlet mass flux directly to burner thermocouple temperature ($T_{max}$) and narrow-angle radiometer outputs.

---

### 5. Repository File Hierarchy

```
nasa-acme-burner-cad-cfd/
├── PSI-Documents/
│   ├── Engineering Documents/
│   │   ├── CADs_Nosso/
│   │   │   ├── Montagens/               # Consolidated assembly models (IPT & STEP)
│   │   │   └── Serie_1100_a_1109/       # Individual MFD 3D models (IPT & STEP AP214)
│   │   └── Desenhos_Tecnicos_NASA/      # Original technical drawing archives (PDF)
│   │       ├── ACME_drawings_burners/   # Burner series technical drawings
│   │       ├── ACME_drawings_igniter/   # Igniter subsystem drawings
│   │       └── ...                      # Auxiliary subsystems and instrumentation
│   ├── Metadata/                        # Mission test matrices and experimental logs
│   └── Reports/                         # Engineering reports, CAD summaries, and test reviews
├── Project_Demo/
│   ├── Dataset_Multimodal_Final.csv     # Extracted multi-sensor experimental dataset
│   ├── ML/
│   │   ├── DigitalTwin_PINN.py          # Physics-Informed Neural Network Digital Twin
│   │   ├── PINN.py                      # Core PINN implementation
│   │   ├── PINN_Bayesiana.py            # Bayesian uncertainty quantification network
│   │   └── SVR.py                       # Support Vector Regression baseline
│   ├── Ref/
│   │   ├── Diario_de_Bordo_SpaceApps.md # Technical progression log
│   │   └── PSI-23_Experimental table.csv# Master test condition matrix
│   ├── Treinamento_SVR/                 # Trained surrogate weights and telemetry splits
│   ├── Treinamento_Visao/               # Computer vision calibration and contour outputs
│   └── nasa_psi_pipeline.py             # Feature engineering and dataset compilation
├── .gitignore                           # Repository filtering rules
└── README.md                            # Technical project documentation
```

---

### 6. Cloud Data Architecture (Google Drive)

Due to file transfer constraints on raw video streams (.hobj / .mp4), comprehensive uncompressed drawing packs, and high-resolution volumetric CFD grids (`.cas.h5` / `.dat.h5`), voluminous project data is indexed and archived in the centralized cloud directory:

* **Central Storage Repository:** [NASA ACME Project Data Drive](https://drive.google.com/drive/folders/1WFyWEZC26ahaA6jAb-edNxs2iua_a0W8?usp=sharing)

---

### 7. Regulatory & Open Science Compliance Notice

* All primary research drawings, flight telemetry measurements, and optical sensor data utilized in this investigation originate from the **NASA Physical Sciences Informatics (PSI)** data repository under the open science data policy of the National Aeronautics and Space Administration.
* The contents are classified as **unclassified, public domain information with unlimited distribution rights**.
* Derivative algorithmic code, surrogate architectures, and computational models contained in this repository are maintained for scientific research, competition evaluation, and authorized technical appraisal.

---
### 8. Project Credits & Technical Leadership

* **Lead Mechanical Design & Simulation Engineer:** Emerson B. J. (EmersonBJ)  
  * Responsible for precision manual 3D modeling and reverse-engineering of high-complexity flight hardware components, GD&T resolution, ANSYS CFD boundary formulation, and multidisciplinary system integration.
* **Procedural Automation:** Python COM routines for automated parametric synthesis of axisymmetric baseline components and batch data pipeline orchestration.
