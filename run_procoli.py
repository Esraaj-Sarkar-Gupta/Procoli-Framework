"""
Procoli post processing framework

Requires MontePython chains

Esraaj Sarkar Gupta
15th Feb, 2026

References:
    Procoli: Profiles of cosmological likelihoods - Karwal et. al.
        https://github.com/tkarwal/procoli
        https://arxiv.org/abs/2401.14225
"""

import argparse
from pathlib import Path
import yaml
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    "config",
    help="Path to procoli configuration YAML file (e.g. config.yaml)"
)
args = parser.parse_args()
config_path = Path(args.config)

if not config_path.exists():
    raise FileNotFoundError(f"Config file not found: {config_path}")

if config_path.suffix.lower() not in {".yaml", ".yml"}:
    raise ValueError(f"Config must be a .yaml/.yml file, got: {config_path.suffix}")

with config_path.open("r") as file:
    config = yaml.safe_load(file)

# ---- Environment Conif ---- #
montepython_dir = Path(config["env"]["montepython_dir"]).expanduser().resolve()
montepython_py = montepython_dir / "MontePython.py"

if not montepython_py.exists():
    raise FileNotFoundError(f"MontePython.py not found at: {montepython_py}")

# Ensure MPI can find "MontePython.py"
os.environ["PATH"] = str(montepython_dir) + os.pathsep + os.environ.get("PATH", "")


# ===== Configuration ===== #
from procoli import lkl_prof

# ---- Configuration ---- #
chains_dir_name = os.path.abspath(config["run"]["chains_directory"])
chains_name = config["run"]["chains_name"]

parameter_to_profile = config["run"]["profile_parameter"]

# ---- Calling Procoli ---- #
profile = lkl_prof(
    chains_dir=chains_dir_name,
    prof_param=parameter_to_profile,
    info_root=chains_name
)

# ---- Search Tuning ---- #
profile.prof_max = float(config["profile"]["profile_max"])
profile.prof_min = float(config["profile"]["profile_min"])
profile.processes = int(config["profile"]["processes"])
profile.prof_incr = float(config["profile"]["profile_increments"])


# ---- Global Optimization Settings ---- #
global_jump_factors = list(config["global_optimization"]["jump_factors"])
global_temperatures = list(config["global_optimization"]["temperatures"])

if len(global_jump_factors) != len(global_temperatures):
    ValueError("Global jump factors and global temperatures must have the same number of phases!")

profile.set_global_jump_fac(
    global_jump_factors
)
profile.set_global_temp(
    global_temperatures
)

global_min_steps = int(
    config["global_optimization"]["min_steps"]
)

# ---- Ridge Exploration Settings ---- #
jump_factors = list(
    config["mapping"]["jump_factors"]
)
mapping_temperatures = list(
    config["mapping"]["temperatures"]
)

profile_min_steps  = int(
    config["mapping"]["min_steps"]
)

# ===== Running Positive Increments ===== #
# -- Global Optimization -- #
profile.global_min(
    N_min_steps = global_min_steps
)

# -- Profiling -- #
profile.init_lkl_prof()
profile.run_lkl_prof(
    time_mins = True,
    N_min_steps = profile_min_steps
)

# ===== Running Negative Increments ===== #
profile.prof_incr *= -1 # Flip Incrementation

# -- Global Optimization -- #

profile.global_min(
    N_min_steps = global_min_steps
)

# -- Profiling -- #
profile.init_lkl_prof()
profile.run_lkl_prof(
    time_mins = True,
    N_min_steps = profile_min_steps
)

print("Program Ends")
# As all good things do end
