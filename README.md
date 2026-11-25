<h1 align="center">Create networkneuro datatype for visualization</h1>

<p align="center">
  Packages a tractogram, a parcellation and connectivity matrices into the networkneuro datatype used by the brainlife.io networkneuro visualizer.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.620"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.620-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" alt="MIT license"></a>
</p>

> **This branch, `labels-v1.0`, is the brainlife.io App Create networkneuro datatype for visualization** ([doi:10.25663/brainlife.app.620](https://doi.org/10.25663/brainlife.app.620)).

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Packages a tractogram, a parcellation and connectivity matrices into the networkneuro datatype used by the brainlife.io networkneuro visualizer.**

| | |
|---|---|
| **Inputs** | `neuro/track/tck` · `neuro/parcellation/volume` · `neuro/labels` · `neuro/conmat` ×4 |
| **Outputs** | `neuro/networkneuro` |
| **Container** | `brainlife/dipy:1.4.0` |
| **Resources** | 4 CPUs · 40 GB memory |
| **Run it** | [doi.org/10.25663/brainlife.app.620](https://doi.org/10.25663/brainlife.app.620) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `tract` | `neuro/track/tck` | yes |  |
| `parc` | `neuro/parcellation/volume` | yes | Parcellation used for generating network. Purely here to generate vtks |
| `labels` | `neuro/labels` (!binary) | yes |  |
| `count` | `neuro/conmat` (count) | yes |  |
| `density` | `neuro/conmat` (density) | yes |  |
| `length` | `neuro/conmat` (length) | yes |  |
| `denlen` | `neuro/conmat` (denlen) | yes |  |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `netneuro` | `neuro/networkneuro` |  |

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.620](https://doi.org/10.25663/brainlife.app.620), choose `neuro/track/tck`, `neuro/parcellation/volume`, `neuro/labels`, `neuro/conmat`, `neuro/conmat`, `neuro/conmat`, `neuro/conmat` from your project and press **Execute**. The results are saved to your project as `neuro/networkneuro`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlife/dipy:1.4.0`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "track": "/path/to/tract/track",
       "parc": "/path/to/parc/parc",
       "label": "/path/to/parc/label",
       "index": "/path/to/labels/index",
       "names": "/path/to/labels/names",
       "count": "/path/to/count/count",
       "density": "/path/to/density/density",
       "length": "/path/to/length/length",
       "denlen": "/path/to/denlen/denlen"
   }
   ```

3. Run `./main`.

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- Create networkneuro datatype for visualization. brainlife.io App. [doi:10.25663/brainlife.app.620](https://doi.org/10.25663/brainlife.app.620)
- McPherson, B.C., Pestilli, F. A single mode of population covariation associates brain networks structure and behavior and predicts individual subjects’ age. Commun Biol 4, 943 (2021). https://doi.org/10.1038/s42003-021-02451-0
- Garyfallidis et al. Dipy, a library for the analysis of diffusion MRI data. *Frontiers in Neuroinformatics* 8 (2014). [doi:10.3389/fninf.2014.00008](https://doi.org/10.3389/fninf.2014.00008)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Brad Caron
- Brent McPherson

**Contributors**

- Soichi Hayashi

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io is publicly funded, and acknowledging that support helps keep it running. This App was developed with support from Wellcome, the U.S. National Institutes of Health (including the BRAIN Initiative BRAIN CONNECTS program: The Axonal Projectome EXchange, U24NS140384, and the Center for Mesoscale Connectomics, UM1NS132207) and the U.S. National Science Foundation.</sub>

## License

See [LICENSE](LICENSE).
