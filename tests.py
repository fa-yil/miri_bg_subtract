import funcs

s_ch4_m = "data/JWST/science/jw03722-o003_t003_miri_ch3-long/jw03722-o003_t003_miri_ch3-long_s3d.fits"
b_ch4_m = "data/JWST/background/jw03722-o007_t007_miri_ch3-long/jw03722-o007_t007_miri_ch3-long_s3d.fits"

s_ch1_l_hdul, s_ch1_l_cube, s_ch1_l_header, s_ch1_l_info, s_ch1_l_wcs = funcs.load_image(s_ch4_m)
b_ch1_l_hdul, b_ch1_l_cube, b_ch1_l_header, b_ch1_l_info, b_ch1_l_wcs = funcs.load_image(b_ch4_m)

funcs.multiple_cube_viewer([b_ch1_l_cube, s_ch1_l_cube], [b_ch1_l_wcs, s_ch1_l_wcs], layout="horizontal")
