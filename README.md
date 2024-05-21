# Interpol_Schemes
Interpolation of rotation measure data with different kernels

# Interpolation of RM Data 
Interpolation of RM data helps us fill in the gaps between sparse RM measurements. Previous work has been done in the interpolation of galactic foreground RM, culminating in the Galactc Faraday rotation sky produced by [Hutschenreuter et al. (2022)](https://ui.adsabs.harvard.edu/abs/2022A%26A...657A..43H/abstract). This projects focuses on the interpolation of foreground RM data, using simulation cubes from [Seta & Federrath (2021)](https://ui.adsabs.harvard.edu/abs/2021PhRvF...6j3701S/abstract), using a patchy RM sky and a filamentary RM sky to test the kernels in two broad categories of RM structures that are found in the sky. The interpolation techniques tested are: Inverse Distance Weighting (IDW), Natural Neighbour Interpolation (NNI), Inverse Multiquadric (IM), Thin-Plate Splines (TPS), and the Bayesian Rotation Meaasure Sky (BRMS). 

All code necessary to produce the figures and results from Khadir et al. 2024 are included in the notebook that can be found [here](https://github.com/AffanKhadir/Interpol_Schemes/blob/main/Code/Interpolation_Schemes_Notebook.ipynb).

It must be noted that these interpolation techniques can also be used for any other 2D astronomical data.
