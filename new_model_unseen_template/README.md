Here we train a new VAE model. Then simulate a background dataset using a template experiment that is **not included** in the training dataset (i.e. the datasets used to train the VAE model).

## Usage
1. Create a configuration and metadata files for your analysis. See [example configuration file](config_example.tsv). The definition for each paramter in the configuation file is describe below.

Note: When editing this configuration file, use a text editor instead of excel.

Parameters for input data files supplied by the user, directories that sophie will create, and parameters that control the execution behavior of sophie.

| Name | Description |
| :--- | :---------- |
| base_dir| str: Root directory containing analysis subdirectories. By default the path is one level up from where the scripts are run.|
| local_dir| str: Parent directory on local machine to store intermediate results. Make sure to end path name with "/"|
| raw_template_filename | str: Downloaded template gene expression data file. The input dataset should be a matrix that is sample x gene. The file should tab-delimited. The input dataset should be generated using the same platform as the model you plan to use (i.e. RNA-seq or array). The expression values are expected to have been uniformly processed and can be estimated counts (RNA-seq) or log2 expression (array).|
| raw_compendium_filename | str: Downloaded compendium gene expression data file. The input dataset should be a matrix that is sample x gene. The file should tab-delimited. The gene ids need to be consistent between the template and compendium datasets. The input dataset should be generated using the same platform as the model you plan to use (i.e. RNA-seq or array). The expression values are expected to have been uniformly processed and can be estimated counts (RNA-seq) or log2 expression (array).|
| project_id | str:  The experiment id to use as template experiment. This experiment is **not contained** within the training dataset that was used to train the VAE. The id is used to name intermediate simulated data files created.|
| num_simulated| int: The number of experiments to simulate. Experiments are simulated by shifting the template experiment in the latent space. In general, [Lee et al., Figure S4](https://www.biorxiv.org/content/10.1101/2021.05.24.445440v3) found that downstream statistical results were robust to different numbers of simulated experiments so starting with 25 experiments can compromise on the runtime of the downstream analyses. |
| simulated_data_dir | str:  The location where the simulated experiments are written to. This directory is created by https://github.com/greenelab/ponyo/blob/master/ponyo/utils.py|
| vae_model_dir | str:  The location where the VAE model files (.h5) are written to. This directory is created by https://github.com/greenelab/ponyo/blob/master/ponyo/utils.py|
| training_stats_dir| str: Directory where the VAE training log files are written to. This directory is created by https://github.com/greenelab/ponyo/blob/master/ponyo/utils.py|
| learning_rate| float: Step size used for gradient descent. In other words, it's how quickly the  methods is learning|
| batch_size | str: Training is performed in batches. So this determines the number of samples to consider at a given time|
| epochs | int: Number of times to train over the entire input dataset|
| kappa | float: How fast to linearly ramp up KL loss|
| intermediate_dim| int: Size of the hidden layer|
| latent_dim | int: Size of the bottleneck layer|
| epsilon_std | float: Standard deviation of Normal distribution to sample latent space|
| validation_frac | float: Fraction of samples to use for validation in VAE training|
| DE_method| str: "limma" or "deseq". Differential expression method to use.|
| count_threshold | int: Remove genes that have mean count <= count_threshold. By default this threshold is set to None, then no genes are removed.|
| template_process_samples_filename | str: Metadata file that maps sample ids to labels that indicate if the sample is kept or discarded. By default, a two-condition differential expression analysis is supported (case vs control). However, some experiments included more than 2 conditions and so these "extra" samples should not considered in the downstream differential expression analysis. This file contains 2 columns that are tab-delimited. The first column contains sample ids and the second column contains the group id: "1"s denote controls, "2"s denote cases and "drop" denotes samples to remove. For example, say there is an experiment that contains WT samples, mutant A samples and mutant B samples. Since we assume a two-condition experiment, we will remove all mutant B samples so that we can compare WT vs mutant A samples.|
| template_DE_grouping_filename | str: Metadata file that maps sample ids to groups for differential expression analysis. By default, a two-condition differential expression analysis is supported (case vs control). This file contains 2 columns that are tab-delimited. The first column contains sample ids and the second column contains the group id: "1"s denote controls and "2"s denote cases. |
| rank_genes_by | str: "log2FoldChange" if using DESeq or "log2FC" if using limma. |
| is_recount2| bool: True is the compendium dataset being used is recount2. This will determine how experiment ids are parsed for latent transformation approaches.|

Parameters for intermediate files created. Names of files need to be specified:
*Note: Ensure these file paths exists.*

| Name | Description |
| :--- | :---------- |
| scaler_transform_filename | str: The location where the scaler file is stored. This file was generated during the VAE training process.|
| normalized_compendium_filename | str: Normalized compendium gene expression data filename. Make sure to use the extension ".xz"| 
| mapped_template_filename | str: Template gene expression data filename. This file is generated by scale transforming the data using the scaler_filename. The gene ids of the template file and the compendium file are matched.|
| normalized_template_filename | str: Normalized template gene expression data filename. The template experiment is normalized using the same scaler transform that was used to 0-1 scale the normalized compendium used to train the VAE (scaler_transform_filename).|
| processed_template_filename | str: Processed template gene expression data filename. This file contains gene expression data after extra samples have been dropped based on `template_process_samples_filename` and count thresholding applied.|
| output_filename | str: Filename containing the SOPHIE results.|


2. Create metadata files that specify how samples within the selected template experiment should be grouped for the differential expression analysis. 
By default, a two-condition differential expression analysis is supported (case vs control). In the metadata file, "1"s denote controls and "2"s denote cases. In the metadata file, "1"s denote controls and "2"s denote cases. This file is specified by the `template_DE_grouping_filename` parameter. An example can be seen [here](costello_groups.tsv)

3. Run notebooks in order
