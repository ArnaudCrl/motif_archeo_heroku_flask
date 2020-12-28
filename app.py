from io import BytesIO
from PIL import Image
import base64
from flask import Flask, request, render_template, flash, redirect, url_for
import asyncio, aiohttp
from fastai.vision.all import *
import os


UPLOAD_FOLDER = 'downloads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

path = Path(__file__).parent

model_file_url = 'https://www.dropbox.com/s/swydgx4eaxj3h4h/archeo_bw.pkl?dl=1'
model_file_name = 'archeo_bw.pkl'
model_path = path

dico = {"MGP_Borniga_Cimiez": "https://drive.google.com/drive/folders/1pib36Qdpi2lHPV-h_HZV72MCs8QX8V4L?usp=sharing",
"MGP_Larnaud_Limone": "https://drive.google.com/drive/folders/1UDgwet1kNKMYWY-0i53arHwbMIL05bkO?usp=sharing",
"MGP_Nessi_Camaiore": "https://drive.google.com/drive/folders/1EsrVeKiLo8f8ZxYrv7JWLpIA_KdkdfGZ?usp=sharing",
"MGP_Pariana_Paveze": "https://drive.google.com/drive/folders/14J0CeTGZ3VbDOgBZKSGXOHcBsR249uDi?usp=sharing",
"wabern_quadrillé": "https://drive.google.com/drive/folders/1xCOtisSGUsK5s_Fv5xGyLwBRBLOyRh5I?usp=sharing",
"Wabern_courbes": "https://drive.google.com/drive/folders/1v-IzZ_LO5eMgNb4kH-0gdwjaVbmv1kLd?usp=sharing",
"Wabern_tiretés": "https://drive.google.com/drive/folders/1erEm7RZ-R2wA-BU8nbOZ7SyNngXhzBYt?usp=sharing",
"Wabern_frise": "https://drive.google.com/drive/folders/1DElFn3Yi8mKgcb9xsaNq_gghQxCSjkRH?usp=sharing",
"Wabern_évolué": "https://drive.google.com/drive/folders/14s31ouz1MyNtEU18micCdXfGeOAj3XBq?usp=sharing",
"Wabern_centré_long": "https://drive.google.com/drive/folders/1MF9Xziyvb7IXpsKxWvhTSFa_WQfMEveX?usp=sharing",
"Wabern_centré": "https://drive.google.com/drive/folders/1XyCPD0NQRxiAMpvgXPi8LVqiVBnjTBsi?usp=sharing",
"Wabern_barques": "https://drive.google.com/drive/folders/15BpoGhO4HtwjS_lj4UBp3xLLp6G5bRz0?usp=sharing",
"Vinol_triangles_2": "https://drive.google.com/drive/folders/1nVGsywfVu24kw68H3EazeRzUwnrjdT1q?usp=sharing",
"Vinol_chevrons_centrés": "https://drive.google.com/drive/folders/1l3W4MJdzkiqozQr5j_8tPhBNyDuIWsch?usp=sharing",
"Vinol_courbes": "https://drive.google.com/drive/folders/1ccoi26IEbPCWr8FigpBwn84dLU0ealYt?usp=sharing",
"Vinol_triangles": "https://drive.google.com/drive/folders/1T5P6Wg1CV6xAW4rICyrO_qWyXhyJOzzg?usp=sharing",
"Vinol_oves": "https://drive.google.com/drive/folders/1RPjIP1yX5YJ4OSlu3rOWv34u6rm-BwZ6?usp=sharing",
"Vinol_triangles_3": "https://drive.google.com/drive/folders/1BqhkUhoKGLGZpa04lu2fBrv-03LEeAHh?usp=sharing",
"Ukraine_4_3": "https://drive.google.com/drive/folders/1wKvLbU_rFiDUWP5VbVSih2ft0Y3Iu4bh?usp=sharing",
"Ukraine_4_4": "https://drive.google.com/drive/folders/1tLSUGIfixck64LfC1iWOIF2aCEfH7p5W?usp=sharing",
"Ukraine_croix": "https://drive.google.com/drive/folders/1Yn82g_91e6ADo3qAc5Qq9k2ntW5J87w8?usp=sharing",
"Ukraine_4_5": "https://drive.google.com/drive/folders/18pOVk1wG0yl1wjlK5kflqSdGkSi4B2PM?usp=sharing",
"Ukraine_continu": "https://drive.google.com/drive/folders/18FLwvuPuaPfjjyM1wrknJSBeSpqBOPMP?usp=sharing",
"Ukraine_3_4": "https://drive.google.com/drive/folders/1mHD3JQ6Y6vNd6MUtMWiyiSFURklAILag?usp=sharing",
"MGP_Hongrie_triangles_reliés": "https://drive.google.com/drive/folders/1yvB3ZZTSBNRCbMUl3sUucD9htYtTBOQx?usp=sharing",
"MGP_Hongrie_triangles affrontés": "https://drive.google.com/drive/folders/1wbINLSg7cfvOg8Pf8cc2l01cSl3fviFy?usp=sharing",
"MGP_Hongrie_Courbes_hongroises": "https://drive.google.com/drive/folders/1rytGruFdCQf0qWuvf1xCmLNQXwfy9icQ?usp=sharing",
"MGP_Hongrie_triangles_ultrasimples": "https://drive.google.com/drive/folders/1qKmU09IFIp-wf_IPXPCp9IDsr64Aa39-?usp=sharing",
"MGP_Hongrie_triangles_chevrons": "https://drive.google.com/drive/folders/1lO1ftf-qGeP0so9Tr-9JGXqSGsjjNLJS?usp=sharing",
"MGP_Hongrie_triangles_chargés": "https://drive.google.com/drive/folders/1bFFPk3bOZMKw9Fla35fqdgv4wB1Ytwuw?usp=sharing",
"MGP_Hongrie_Futog_Salvon": "https://drive.google.com/drive/folders/1NSsHq6-r_gLBD2ahffUNkNlSU2upZySi?usp=sharing",
"SAY_Centre_Chargé": "https://drive.google.com/drive/folders/1OcbgyMowCvjQ0Dv3XUdY4UCIcpgEIh9k?usp=sharing",
"SAY_Jack": "https://drive.google.com/drive/folders/1EbPl-eTnSzN4us0VrkB6DkbyEvVxVoMN?usp=sharing",
"SAY_simples": "https://drive.google.com/drive/folders/1EHshzVGArMXOgQqFwZA-YXH2v1m7bWQl?usp=sharing",
"Réni_Biberau": "https://drive.google.com/drive/folders/1q--SsqIq-PYNhYGo0uKA1RPCt54Dc7Co?usp=sharing",
"Réni_classique": "https://drive.google.com/drive/folders/1SkJr9OCI_Jj4AXKx_PBz9jIC1tmFDx71?usp=sharing",
"Réni_tardif": "https://drive.google.com/drive/folders/14gE1v-1Ppy75zHkceIbl89yxbyvj3X2s?usp=sharing",
"tores_oves_chevrons": "https://drive.google.com/drive/folders/1NKaV0Fw_C3zwa1ty5IBPiGXNOOwoqRsj?usp=sharing",
"tores_hachures_brisées": "https://drive.google.com/drive/folders/1tdJjQdpABURDnImYsYbiRgPiTzLqpd75?usp=sharing",
"MGP_Rosan_classique": "https://drive.google.com/drive/folders/1kcZzAJf4Bsfzq9na50yk4UNkN3Pi4N8j?usp=sharing",
"MGP_Rosan_Tardif": "https://drive.google.com/drive/folders/1VfCSrydsXQ5WtqUTCLNm4jmpgagB9c6i?usp=sharing",
"MGP_Rosan_Chusclan_Siccieu": "https://drive.google.com/drive/folders/1UkcnUI_WsBRlsz0P8G5YGVLf-6Nmbrli?usp=sharing",
"Ph_0": "https://drive.google.com/drive/folders/1idlK5ml0olrlNiuvw23Rt2d0L6k2W1RH?usp=sharing",
"gpe_Pologne_triangles": "https://drive.google.com/drive/folders/1zZgf9cd45kKHfRERQmL9OW91BoThXMOh?usp=sharing",
"gpe_Pologne_Chevrons": "https://drive.google.com/drive/folders/1wqRfHA5hpXBUh2c2dfQC7uuGthBYXwhk?usp=sharing",
"gpe_Pologne_courbes": "https://drive.google.com/drive/folders/1lpLsMeKPUTgJgPqVzJnCBbdHO2_eMt8W?usp=sharing",
"MGP_tampons_à_obliques": "https://drive.google.com/drive/folders/1u5AC6Pb8hCH9WLBYye2-YAl-oJTGaZyr?usp=sharing",
"MGP_tampons_étagés": "https://drive.google.com/drive/folders/1_OdgzO6tyQYwtJ15pggINuJexKYKuAhF?usp=sharing",
"MGP_tampons_barques": "https://drive.google.com/drive/folders/1Ji_JScXToeJUS4WU7Mki1NF81OKkGxZu?usp=sharing",
"MGP_tampons_chevrons_frêles": "https://drive.google.com/drive/folders/1J3QvF2o6LPsjZQ3v8GRcJzWlS5MXW-VH?usp=sharing",
"Subingen_triangles_chevrons": "https://drive.google.com/drive/folders/1ancuiDA8hz-Y_Q10HW92Z0T1EFBBC3pF?usp=sharing",
"Subingen_triangles_chevrons_étagés": "https://drive.google.com/drive/folders/1RPtiD-5WOhAag5WVp0tHsBv9pHyvf2kn?usp=sharing",
"Subingen_oves_losanges": "https://drive.google.com/drive/folders/18Fz-4fIgAj1THjsAdo9RO6V-QUttuTiA?usp=sharing",
"Subingen_courbes": "https://drive.google.com/drive/folders/1ej3hMcKVZvCE4EbNOmZb9i2CBzP3fv2r?usp=sharing",
"Pologne_ha_oves": "https://drive.google.com/drive/folders/1oC8KOgLKSvOv6WTt8sV04cyEwC1C1Qnt?usp=sharing",
"Pologne_ha_chevrons": "https://drive.google.com/drive/folders/1JYZaxJG24sljelRob5AzjyhsOQ1ZmRpr?usp=sharing",
"nord_à_courbures_courtes": "https://drive.google.com/drive/folders/1MnTkSXdF0WsWX3-Gd6lhZBOf1ZLSmQx6?usp=sharing",
"nord_à_courbures_longues": "https://drive.google.com/drive/folders/1JEgghNOptcncTirTdCUUuF9ZuViJvr5n?usp=sharing",
"nord_triangles": "https://drive.google.com/drive/folders/1oGvIwG_prFGYfVKpa4aSOUAnDcREiUOQ?usp=sharing",
"nord_chevrons": "https://drive.google.com/drive/folders/1x5S1zSf62newg9Qjkf3npuJMUgk2T7Ia?usp=sharing",
"Morges_prépa": "https://drive.google.com/drive/folders/1-E7a7qxUW3GawMDEAa5xU9xd_0tt-naC?usp=sharing",
"Morges_classique": "https://drive.google.com/drive/folders/11epyOkuwKv8ur1PrLUZxMCCvjk4LQv-C?usp=sharing",
"Macédoine": "https://drive.google.com/drive/folders/11t56r0IwqTWIJW9XV_Qhzrppou16c_o5?usp=sharing",
"Meck_triangles_3": "https://drive.google.com/drive/folders/1vhnxsh3x8iiIPqBMbjJsOyJPnr6NqOgw?usp=sharing",
"Meck_triangles_1": "https://drive.google.com/drive/folders/1rvV3wJ_DwN0rWjWAiyjYnVtizWsjX8zf?usp=sharing",
"Meck_bipartition": "https://drive.google.com/drive/folders/1Eh8N6ROczD71z9PmY7flU_9-MROscCmA?usp=sharing",
"Mitterkirchen_triangles_oves": "https://drive.google.com/drive/folders/1ut7D43IpO6gV2XpXALgz1jsfFkK610NQ?usp=sharing",
"Mitterkirchen_lignes_oves": "https://drive.google.com/drive/folders/1CpeErDztGaxvBZfbLkflvqJpI8JfwCSg?usp=sharing",
"Mitterkirchen_triangles_associés": "https://drive.google.com/drive/folders/19LQfWH1Gs4DJ9MUThUm7kzGlSDgX5Oxz?usp=sharing",
"Mitterkirchen_Latin": "https://drive.google.com/drive/folders/17zAJEsKDXCNl_mt-DkN0Y82X10MI32cq?usp=sharing",
"LT_A_courbes": "https://drive.google.com/drive/folders/1zW14vRmRLB1Z7vDHs4EB6R5xbrXJLZZS?usp=sharing",
"LT_A_oves": "https://drive.google.com/drive/folders/13Rtev1XCxO2Ue16g2Bnjosx5nJKbtwdz?usp=sharing",
"LT_A_chevrons": "https://drive.google.com/drive/folders/1NGkLr5UxKVu5NonaLYCocbndrPwmHp_a?usp=sharing",
"LT_A_anthropomorphe": "https://drive.google.com/drive/folders/1mWmUwrWbLpFtys9870Fsh_iZ3xNmlGpZ?usp=sharing",
"Mola_Mola": "https://drive.google.com/drive/folders/1zBA8kkdEu33Z_oc-CUYdYZtKFg76pmQV?usp=sharing",
"Mola_précoce": "https://drive.google.com/drive/folders/1bUtL0oIaIBc1xTTQ9XJsbvv_lHjEH4ba?usp=sharing",
"Mola_classique": "https://drive.google.com/drive/folders/1DATEycTTneiIa01WdT2muw_B1Q0hmJVU?usp=sharing",
"Mola_oves": "https://drive.google.com/drive/folders/15PN34HDaAfHyC22GwBzQIHsgz6DKOrI6?usp=sharing",
"Lunebourg_courbes_libres": "https://drive.google.com/drive/folders/1kn6Xw6cqY5ZjqDF4wFjs7TU0u3oCnJac?usp=sharing",
"Lunebourg_5etplus": "https://drive.google.com/drive/folders/1UqUlALJcurLtD4EOnAAjUgnPh2FvsYI4?usp=sharing",
"Lunebourg_3": "https://drive.google.com/drive/folders/1RAPPQSkQxEPPNN7BezgpfwyTYzGoLws4?usp=sharing",
"Lunebourg_4": "https://drive.google.com/drive/folders/1God65QKQq4VzetqLSHxhuHgqOEEJeLWN?usp=sharing",
"Lunebourg_hz": "https://drive.google.com/drive/folders/1Cw-RQ7uWYxosdUTk6t4mz1aNt9PvmZ0W?usp=sharing",
"sorti": "https://drive.google.com/drive/folders/1V5w86yfxmEEWAKa5RnJA6rNpeF788-b-?usp=sharing",
"Morave_obliques": "https://drive.google.com/drive/folders/1zghTnxc9a8gytODqs0Dot6-3EajTm_oH?usp=sharing",
"Morave_tardif": "https://drive.google.com/drive/folders/1uRH96K7CQd1GuIk-DkpRTdQciQPsjxPl?usp=sharing",
"Morave_chevrons_brisés": "https://drive.google.com/drive/folders/1qQlXGiWSqLwYoh6GQ05I1pO9-mUQDX0k?usp=sharing",
"morave_quadrige": "https://drive.google.com/drive/folders/1Z3CW4iTz-S_gTww1PkYM525nIvW_tO76?usp=sharing",
"morave_éclair": "https://drive.google.com/drive/folders/1FP4Ysl7UVXminofQEDyLbbt26aaKFpsV?usp=sharing",
"Morave_courbes_centrées": "https://drive.google.com/drive/folders/18qPjcjy3ntK7r-WXxw-sHm9Y6B2wWkqu?usp=sharing",
"Meck_obliques_en_3ou4": "https://drive.google.com/drive/folders/1wKxv7Y0zDPolfqFjXrtJ1QyGhH4ZsBmD?usp=sharing",
"Meck_obliques_simples_brisées": "https://drive.google.com/drive/folders/1gmdukRcRalFUk6VeppMFdsrnr6CIeW5h?usp=sharing",
"Meck_obliques_simples": "https://drive.google.com/drive/folders/1IhJVlyAr3bHtp0V5YDiakx6zXlz8RRCb?usp=sharing",
"Meck_obliques_1bis": "https://drive.google.com/drive/folders/1A5hVljmHGBEmtIqslWS7D-3HW-C3D5Qx?usp=sharing",
"Meck_obliques_bipartites": "https://drive.google.com/drive/folders/12_R9CITVQnIfoAEqDyNtVfzxLly_C8Mi?usp=sharing",
"Meck_obliques_1": "https://drive.google.com/drive/folders/1N-3_FspNvncCg3vogFidOzno6iglQ1yt?usp=sharing",
"Locarno_centre_2": "https://drive.google.com/drive/folders/1p5SaAFugMTkKdiNyOYr523hsJlGypeX8?usp=sharing",
"Locarno_centre_1": "https://drive.google.com/drive/folders/1cJ3xPvujZufDsNmv9SFMfUq6rPpeYvuN?usp=sharing",
"Locarno_bipartite": "https://drive.google.com/drive/folders/1Ny5oUJCsV_2xmBuuMLcRz5Gw2gJHP0Pv?usp=sharing",
"Locarno_centre_3": "https://drive.google.com/drive/folders/13zfgJHwfjCEp0CdsM4nh7NgM0Z-h0tBu?usp=sharing",
"jambières_lignes": "https://drive.google.com/drive/folders/1yBopz8nRnH6Aec-EQA12elb8XSbCWaP4?usp=sharing",
"jambières_barques": "https://drive.google.com/drive/folders/16BUKefD255bJUIN99w7RfsFHKq7mC_ac?usp=sharing",
"jambières_triangles_simples": "https://drive.google.com/drive/folders/1X1rWFPG8raDfU_PDT0sWktyrujfCWxKd?usp=sharing",
"jambières_triangles_complexes": "https://drive.google.com/drive/folders/14ySuqu66trFr8UwjZ_8ZirarNdO-Qj_l?usp=sharing",
"Haguenau_dérivé": "https://drive.google.com/drive/folders/1DEQZayPVAxJQdN9BIqxJtxZkEahTv_mC?usp=sharing",
"Haguenau_classique": "https://drive.google.com/drive/folders/1DA9szAAC2G-zymW7IngVdQPRyZmQUOmH?usp=sharing",
"Esta_précoce": "https://drive.google.com/drive/folders/1QlpxOvoF05zmqpLlfW65ynlnrAuJnKN3?usp=sharing",
"Esta_tardif": "https://drive.google.com/drive/folders/11qkE4c99AHU1fGW3ANkbIjmdYSI0LrHg?usp=sharing",
"Dhrovice_SUD": "https://drive.google.com/drive/folders/1og5qfB_u7znG4oXuS-rgLJ7bkNrP3aa1?usp=sharing",
"Dhrovice_oves_lignes": "https://drive.google.com/drive/folders/1m2or7t4ktfwwj6kvcy-7h702isFlCNjW?usp=sharing",
"Dhrovice_classique": "https://drive.google.com/drive/folders/1WjP65tZzKmonuwp2iIAEAVDYDhuR3pOs?usp=sharing",
"Dhrovice_barques": "https://drive.google.com/drive/folders/1H6EH9kB7TgkBxRBaUEL3RAIOyI0YCEes?usp=sharing",
"Leupolz_sillons": "https://drive.google.com/drive/folders/1rTpM_yXvCWpkQlpvxzMZu5zJFQo1UeGe?usp=sharing",
"Leupolz_simples_garnitures_triangles": "https://drive.google.com/drive/folders/1jGW74P17iqBlPVTBLGYSMGA-GFBLd414?usp=sharing",
"Leupolz_rectangles_centrés": "https://drive.google.com/drive/folders/1Ke9N1ghMYVPFDXPQ_DK_XuBn2tio9Sr3?usp=sharing",
"Leupolz_simples_garnitures_Courbes": "https://drive.google.com/drive/folders/1DHFd6Dkg6zf5NlDtapSBZ-QKLtBOpBuJ?usp=sharing",
"Leupolz_frises_volutes": "https://drive.google.com/drive/folders/17pdJR-U3ss-oRfhkoXDo-drpfoGaXc3T?usp=sharing",
"Leupolz_barques_pointues": "https://drive.google.com/drive/folders/1nuxVVNlmrmO_OHv25IbVDtfv6eepkf_Y?usp=sharing",
"Leupolz_barques_simples": "https://drive.google.com/drive/folders/1T3PD_0mt_0hdUT_Omuy14zIDMGz3h_Tw?usp=sharing",
"Leupolz_barques": "https://drive.google.com/drive/folders/1Q2yXKqMIH5zUDdLSEGo2MDIQVWowLFN0?usp=sharing",
"Leupolz_frises": "https://drive.google.com/drive/folders/14fG2NJXURaIWXHr5jgoxzJUIGI8iQrqG?usp=sharing",
"c_Danube_oves_3et4": "https://drive.google.com/drive/folders/1hTsLgU74EL36cejgG9uxJJ_ur3Sqw9aE?usp=sharing",
"c_Danube_oves_plus_de_4": "https://drive.google.com/drive/folders/1Nj0izXDzR8ioCuWALBZQ6OIr4nUXzNTQ?usp=sharing",
"c_Danube_courbes_4": "https://drive.google.com/drive/folders/1Z29LSninJNeVPbRVpYi0WXdyz2325xy5?usp=sharing",
"c_Danube_courbes_2": "https://drive.google.com/drive/folders/1arieBC5GUpEkVrHLXqfkVAfQLvaoELUW?usp=sharing",
"c_Danube_courbes_3": "https://drive.google.com/drive/folders/1-CYTDgJfHkKR7QCG04cIzRJpUZHk4H4e?usp=sharing",
"Kasidol_courbes_div": "https://drive.google.com/drive/folders/1j-lYGqkOw5BWUfxC2nMr2r4m2bPaTueV?usp=sharing",
"Kasidol_centre_2à3": "https://drive.google.com/drive/folders/1MumSMZsAY9qikZ3eEADpGMES7BYW15pY?usp=sharing",
"Kasidol_obliques": "https://drive.google.com/drive/folders/1FFDcRpQbMlja09o1aTn2KuLPzugUKeqI?usp=sharing",
"kasidol_courbes_alternées": "https://drive.google.com/drive/folders/16P9lWmEI9HjLLb105sdQ75aTz6Km1ZxH?usp=sharing",
"Kasidol_brisées": "https://drive.google.com/drive/folders/1kE-ZpvTPZTt3vn_OasaudEkumuMMGfrg?usp=sharing",
"Kasidol_baroques": "https://drive.google.com/drive/folders/1sNu9SqziAd5OgOTPmPAm-2bKQHleD5fZ?usp=sharing",
"geométrique_et_anthopomorphe_4": "https://drive.google.com/drive/folders/1f3c0X1u1sMPhponWaBLLonOMaajRQWZD?usp=sharing",
"geométrique_et_anthopomorphe_5": "https://drive.google.com/drive/folders/188SNhdI-kDUz75jdqVgsme3jNWOxIaDZ?usp=sharing",
"geométrique_et_anthopomorphe_3": "https://drive.google.com/drive/folders/1nbk3Xpr-4sUo6DoNO8iBmaiztcC2BmXL?usp=sharing",
"geométrique_et_anthopomorphe_2": "https://drive.google.com/drive/folders/1iMQSdW_2I9-08XNi-id98KqECy2qgQxr?usp=sharing",
"geométrique_et_anthopomorphe_1": "https://drive.google.com/drive/folders/1Wj4e9q97nqNR7YIrynTLHV2LRfUhOiFh?usp=sharing",
"coubes_verticales": "https://drive.google.com/drive/folders/1WnJqlSLpcIZyyjgZ1oVkEqfy0PLuEG7C?usp=sharing",
"Corcelettes_très_tardifs": "https://drive.google.com/drive/folders/1bC7SlRgM9HDSZVJcP23lnFnPNnWvT_tn?usp=sharing",
"Corcelettes_tardifs": "https://drive.google.com/drive/folders/1C67M8Q_a6b3eFnGNvlpbYlQWgLgucbRD?usp=sharing",
"Corcelettes_précoces": "https://drive.google.com/drive/folders/1vBmS4ObJhWWLlVBn-2K78ugZw4M8oxyw?usp=sharing",
"Corcelettes_préclassiques": "https://drive.google.com/drive/folders/10ebc0h8dtStijNioCFSkNAgEZPNZlhtn?usp=sharing",
"Corcelettes_protoclassiques": "https://drive.google.com/drive/folders/1R0b04AWxJHCiB4BwxFd50Bj4NNsnypK_?usp=sharing",
"Corcelettes_Patchwork_précoce": "https://drive.google.com/drive/folders/1jMfWZTn162z0mjqw1svr6Y2q8i1d5KHQ?usp=sharing",
"Corcelettes_Patchwork": "https://drive.google.com/drive/folders/1eQsZVOe1-W8eoQpmhagcYi1aPnKjLedx?usp=sharing",
"Corcelettes_baroques": "https://drive.google.com/drive/folders/1O5IjINb7KtBG-5N6lY17kfvi9z3Q1p7h?usp=sharing",
"Corcelettes_classiques": "https://drive.google.com/drive/folders/1IolEvFWLHj4KdWRHPKINvK5fVGR3xN0c?usp=sharing",
"Corcelettes_classiques_précoce": "https://drive.google.com/drive/folders/1DC8h7e25LjAoztoodX2OLb0EJzDu9aZ2?usp=sharing",
"Clans_évolué": "https://drive.google.com/drive/folders/1vSDSdeww79F1fmrFxy-3eqYho_HEwx01?usp=sharing",
"Clans_type": "https://drive.google.com/drive/folders/1ljNM182CTCpVyv4y1w4FdriEJ1P7OY30?usp=sharing",
"Groupe_Angleterre_bis": "https://drive.google.com/drive/folders/1eeWPpHPaDaJox8m1IMgv10fIHIz-bScS?usp=sharing",
"Bignan_classique": "https://drive.google.com/drive/folders/1rb7divk3zxoMGA9rVt8nW-ixaAnOJ-Pr?usp=sharing",
"Bignan_évolué": "https://drive.google.com/drive/folders/1qRfx8aKnemp4dznjbRboUgk-ZCJc4uDs?usp=sharing",
"chevrons occidentaux": "https://drive.google.com/drive/folders/1S83I8Pl7CehUrGoywHiN1GmJP42_LXSt?usp=sharing",
"chevrons gras": "https://drive.google.com/drive/folders/1Q2to8KcsazOVeO3pWjH5tyTF1czS_gZ2?usp=sharing",
"B_Danube_avec_triangles": "https://drive.google.com/drive/folders/1ija14Y77nU0tAWHKBX9zu3zWXDVtOITl?usp=sharing",
"B_avec_oves_et_triangles": "https://drive.google.com/drive/folders/181Caj5LROSFS8BqjHTSp65tOYiwaAReQ?usp=sharing",
"B_avec_oves_et_chevrons": "https://drive.google.com/drive/folders/1n1eexocJljcXQZBrX_7ydyeW2Sd52lRT?usp=sharing",
"B_avec_oves": "https://drive.google.com/drive/folders/1rEkr_ZnZgMk39F30nd6m8M51xsPjRYVA?usp=sharing",
"Agde_évolué_grands_chevrons": "https://drive.google.com/drive/folders/1xjjapK1nB20r3HVwf-dP_sxiBP2hGEcK?usp=sharing",
"Agde_évolué_classique": "https://drive.google.com/drive/folders/11Ue2arPuERA8QFliJieuMd2ZyhZTPZ9C?usp=sharing",
"barques_ongroise_bis": "https://drive.google.com/drive/folders/1rSkVO36ejfZy5oTGo5idy7I40Jnf6I4c?usp=sharing",
"Auvernier_oblique_simple": "https://drive.google.com/drive/folders/1B5wTBh0C6vcYAbU1H1R0TY5-ywnzfBVx?usp=sharing",
"Auvernier_Loire_2": "https://drive.google.com/drive/folders/1c-Nqk0-4Q0rOaF8M2TkZDazZ83-ZcfN9?usp=sharing",
"Auvernier_Loire": "https://drive.google.com/drive/folders/1s1ms9deErj9iQvHlAqwZl2bP0QrzeV3L?usp=sharing",
"Auvernier_classique_2": "https://drive.google.com/drive/folders/1qmMSoz7Ai_SOtmg6WjakWHsOfy_bbdxp?usp=sharing",
"Auvernier_classique_3": "https://drive.google.com/drive/folders/1W1obl3tBsduomGibRqePgCUBhMjlJKfA?usp=sharing",
"Auvernier_classique": "https://drive.google.com/drive/folders/15Bf690448x3erAIgP-7_ir4rGsEUox0n?usp=sharing",
"brassart_Ha_tardif": "https://drive.google.com/drive/folders/1bMVtSrtecZ6PswRckrH2a0_Z3JrBeMMb?usp=sharing",
"brassart_Ha_precoce": "https://drive.google.com/drive/folders/1LmC-aHWky5hFsdD1zeuA9RMgCZBvqVfN?usp=sharing",
"Moora": "https://drive.google.com/drive/folders/19lq0zMQtn7r_Nz8x54LRB5yRU2DSd-sU?usp=sharing"}


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(model_file_url, model_path/model_file_name)
    learn = load_learner(model_path / model_file_name)
    print("learner loaded !")
    return learn

learn = asyncio.run(setup_learner())
print("before app def")
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        print("post request")
        
        # check if the post request has the file part
        if 'file' not in request.form:
            flash('No file part')
            return redirect(request.url)
        file = request.form['file']

        imgdata = base64.b64decode(str(file))
        with Image.open(BytesIO(imgdata)) as image:
            image.save(UPLOAD_FOLDER + 'temp.png')
        
       
        pred, pred_idx, probs = learn.predict("downloads/temp.png")
        classes = learn.dls.vocab
        predictions = sorted(zip(classes, map(float, probs)), key=lambda p: p[1], reverse=True)

        path = "static/images/Vignettes/"
#         # print(os.listdir(path))
        prediction = [str(predictions[0][0])[4:],
                      str(predictions[1][0])[4:],
                      str(predictions[2][0])[4:]]
        print(prediction[0])

        probas = [str('%.2f' % (predictions[0][1] * 100)) + "%",
                  str('%.2f' % (predictions[1][1] * 100)) + "%",
                  str('%.2f' % (predictions[2][1] * 100)) + "%"]

        result1 = []
        result2 = []
        result3 = []

        for sub_class in os.listdir(path + prediction[0]):
            for image in os.listdir(path + prediction[0] + "/" + sub_class):
                if sub_class == "general":
                    result1.append(("""static/images/Vignettes/{}/{}/{}""".format(prediction[0], sub_class, image), prediction[0], dico.get(prediction[0])))
                else:
                    result1.append(("""static/images/Vignettes/{}/{}/{}""".format(prediction[0], sub_class, image), sub_class, dico.get(sub_class)))

        for sub_class in os.listdir(path + prediction[1]):
            for image in os.listdir(path + prediction[1] + "/" + sub_class):
                if sub_class == "general":
                    result2.append(("""static/images/Vignettes/{}/{}/{}""".format(prediction[1], sub_class, image), prediction[1], dico.get(prediction[1])))
                else:
                    result2.append(("""static/images/Vignettes/{}/{}/{}""".format(prediction[1], sub_class, image), sub_class, dico.get(sub_class)))

        for sub_class in os.listdir(path + prediction[2]):
            for image in os.listdir(path + prediction[2] + "/" + sub_class):
                if sub_class == "general":
                    result3.append(("""static/images/Vignettes/{}/{}/{}""".format(prediction[2], sub_class, image), prediction[2], dico.get(prediction[2])))
                else:
                    result3.append(("""static/images/Vignettes/{}/{}/{}""".format(prediction[2], sub_class, image), sub_class, dico.get(sub_class)))

    return render_template('index.html')


def make_square(im, desired_size=512):
    old_size = im.size  # old_size[0] is in (width, height) format

    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    im = im.resize(new_size, Image.ANTIALIAS)

    new_im = Image.new("L", (desired_size, desired_size))
    new_im.paste(im, ((desired_size - new_size[0]) // 2,
                      (desired_size - new_size[1]) // 2))

    return new_im
 

if __name__ == '__main__':
    app.run()
