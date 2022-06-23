# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python [conda env:sophie] *
#     language: python
#     name: conda-env-sophie-py
# ---

# # Template

# %load_ext autoreload
# %load_ext rpy2.ipython
# %autoreload 2
import os
from ponyo import utils, train_vae_modules
from sophie import process

# Set seeds to get reproducible VAE trained models
train_vae_modules.set_all_seeds()

# +
# Read in config variables
config_filename = "config_example.tsv"

params = utils.read_config(config_filename)

# +
# Load config params

# Local directory to store intermediate files
local_dir = params["local_dir"]

# Raw compendium filename
raw_compendium_filename = params["raw_compendium_filename"]

# Normalized compendium filename
normalized_compendium_filename = params["normalized_compendium_filename"]
# -

# ## Setup directories

utils.setup_dir(config_filename)

# ## Normalize compendium

train_vae_modules.normalize_expression_data(
    config_filename,
    raw_compendium_filename,
    normalized_compendium_filename)

# ## Train VAE

# Train VAE
train_vae_modules.train_vae(config_filename,
                            normalized_compendium_filename)
