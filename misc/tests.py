import funcs

# s_ch4_m = "data/JWST/science/jw03722-o003_t003_miri_ch3-long/jw03722-o003_t003_miri_ch3-long_s3d.fits"
# b_ch4_m = "data/JWST/background/jw03722-o007_t007_miri_ch3-long/jw03722-o007_t007_miri_ch3-long_s3d.fits"

# s_ch1_l_hdul, s_ch1_l_cube, s_ch1_l_header, s_ch1_l_info, s_ch1_l_wcs = funcs.load_image(s_ch4_m)
# b_ch1_l_hdul, b_ch1_l_cube, b_ch1_l_header, b_ch1_l_info, b_ch1_l_wcs = funcs.load_image(b_ch4_m# )

# funcs.multiple_cube_viewer([b_ch1_l_cube, s_ch1_l_cube], [b_ch1_l_wcs, s_ch1_l_wcs], layout="horizontal")

# 02 on source 04 background
folder = "/home/fatih/G165_main/G165_miri_bg_subtraction/data/JWST/science003/uncal"
keywords = ['CHANNEL', 'BAND']
bg_results = funcs.header_checker(folder, keyword_filters=keywords, name_contains="041")
sc_results = funcs.header_checker(folder, keyword_filters=keywords, name_contains="021")

print("Background Results:")
for r in bg_results:
    print(r)
# print(len(bg_results))

print("Science Results:")
for r in sc_results:
    print(r)
# print(len(sc_results))


hdul = funcs.load_image("/home/fatih/G165_main/G165_miri_bg_subtraction/data/JWST/science003/uncal/jw03722003001_02101_00001_mirifulong_uncal.fits")[0]
header = hdul[0].header

# for key, value in header.items():
#     print(f"{key}: {value}")