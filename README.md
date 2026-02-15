# Procoli + MontePython Workflow
**Author:** Esraaj Sarkar Gupta  
**Date:** 15th February 2026  

This framework automates the generation of **Profile Likelihoods** for cosmological parameters by interfacing `Procoli` with `MontePython` and `CLASS`.

---

## Overview
The workflow performs a robust profile likelihood analysis by finding the global minimum and then "walking" along the likelihood ridge in both positive and negative directions for a target parameter.



### Key Components
* **Global Optimization:** Uses simulated annealing to locate the $\chi^2$ minimum.
* **Profile Mapping:** Incremental exploration of the likelihood surface.
* **Bi-Directional Search:** Automatically flips the increment to cover both sides of the best-fit point.

---

## Configuration
The script is driven by a `config.yaml` file. This allows you to swap models or parameters without touching the core Python logic.

### Settings breakdown:
| Section | Description |
| :--- | :--- |
| **`env`** | Paths to your `MontePython` installation and environment. |
| **`run`** | Defines the chain directory, root name, and the parameter to profile (e.g., `H0`). |
| **`profile`** | Sets the search boundaries (`min`/`max`) and the step size (`increments`). |
| **`global_optimization`** | Tuning parameters for the initial simulated annealing (Steps, Jump Factors, Temp). |
| **`mapping`** | Tuning parameters for the incremental ridge exploration. |

---

## Function Reference

### `profile.global_min(N_min_steps)`
Finds the global best-fit. 
> **Note:** `N_min_steps` should be at least **2000**. Using a small value (like 100) often triggers the *"No decently sized chain"* error because it fails to generate a sufficient covariance matrix.

### `profile.set_global_jump_fac()` & `profile.set_global_temp()`
Sets the simulated annealing schedule. High temperatures and jump factors allow the optimizer to escape local minima, while lower values refine the search at the end.

### `profile.run_lkl_prof()`
Executes the actual profiling. This workflow runs this twice:
1.  **Forward:** Moves in the direction of `prof_incr`.
2.  **Backward:** Flips the sign of `prof_incr` and re-runs to ensure a symmetric profile.

---

## Execution Syntax

To run the workflow, ensure your environment is active and pass the configuration file as an argument:

```bash
python procoli_workflow.py config.yaml
```

### References
Procoli: Profiles of cosmological likelihoods - Karwal et. al.
        https://github.com/tkarwal/procoli
        https://arxiv.org/abs/2401.14225