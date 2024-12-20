#### conda setup
First, download and install Anaconda:

1. Visit the [Anaconda download page](https://www.anaconda.com/download)
2. Download the appropriate installer for your operating system (Windows, macOS, or Linux)
3. Run the installer and follow the installation instructions

After installing Anaconda, open a terminal (or Anaconda Prompt on Windows) and follow these steps:

First, create a new conda environment:
```bash
conda create -n cams-viz python=3.10
```

Activate the environment:
```bash
conda activate cams-viz
```

Install required packages:
```bash
conda install -c conda-forge earthkit-data earthkit-plots matplotlib numpy netcdf4 jupyterlab
```

Navigate to the directory containing this notebook and start a JupyterLab server:
```bash
jupyter lab
```

This will open a web browser where you can interact with the notebook.