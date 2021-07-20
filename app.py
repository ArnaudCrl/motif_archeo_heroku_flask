# -*-coding:utf-8 -*

from io import BytesIO
from PIL import Image
import base64
from flask import Flask, request, render_template, flash, redirect, url_for
import asyncio, aiohttp
from fastai.vision.all import *
import os
from operator import itemgetter

# # REMOVE FOR DEPLOYMENT !!!!!!
# import pathlib
#
# temp = pathlib.PosixPath
# pathlib.PosixPath = pathlib.WindowsPath
# # !!!!!!!!!!!!

UPLOAD_FOLDER = 'downloads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

path = Path(__file__).parent

model_file_url = 'https://www.dropbox.com/s/swydgx4eaxj3h4h/archeo_bw.pkl?dl=1'
model_file_name = 'archeo_bw.pkl'
model_path = path

dico = {"MGP_Borniga_Cimiez": "https://graphbz.eu/spip.php?article6334",
        "MGP_Larnaud_Limone": "https://graphbz.eu/spip.php?article6335",
        "MGP_Nessi_Camaiore": "https://graphbz.eu/spip.php?article6337",
        "MGP_Pariana_Paveze": "https://graphbz.eu/spip.php?article6336",
        "wabern_quadrillé": "https://graphbz.eu/spip.php?article6239",
        "Wabern_courbes": "https://graphbz.eu/spip.php?article6236",
        "Wabern_tiretés": "https://graphbz.eu/spip.php?article6240",
        "Wabern_frise": "https://graphbz.eu/spip.php?article6238",
        "Wabern_évolué": "https://graphbz.eu/spip.php?article6237",
        "Wabern_centré_long": "https://graphbz.eu/spip.php?article6235",
        "Wabern_centré": "https://graphbz.eu/spip.php?article6234",
        "Wabern_barques": "https://graphbz.eu/spip.php?article6233",
        "Vinol_triangles_2": "https://graphbz.eu/spip.php?article6245",
        "Vinol_chevrons_centrés": "https://graphbz.eu/spip.php?article6241",
        "Vinol_courbes": "https://graphbz.eu/spip.php?article6242",
        "Vinol_triangles": "https://graphbz.eu/spip.php?article6244",
        "Vinol_oves": "https://graphbz.eu/spip.php?article6243",
        "Vinol_triangles_3": "https://graphbz.eu/spip.php?article6246",
        "Ukraine_4_3": "https://graphbz.eu/spip.php?article6283",
        "Ukraine_4_4": "https://graphbz.eu/spip.php?article6284",
        "Ukraine_croix": "https://graphbz.eu/spip.php?article6286",
        "Ukraine_4_5": "https://graphbz.eu/spip.php?article6285",
        "Ukraine_continu": "https://graphbz.eu/spip.php?article6286",
        "Ukraine_3_4": "https://graphbz.eu/spip.php?article6282",
        "MGP_Hongrie_triangles_reliés": "https://graphbz.eu/spip.php?article6266",
        "MGP_Hongrie_triangles affrontés": "https://graphbz.eu/spip.php?article6263",
        "MGP_Hongrie_Courbes_hongroises": "https://graphbz.eu/spip.php?article6261",
        "MGP_Hongrie_triangles_ultrasimples": "https://graphbz.eu/spip.php?article6267",
        "MGP_Hongrie_triangles_chevrons": "https://graphbz.eu/spip.php?article6265",
        "MGP_Hongrie_triangles_chargés": "https://graphbz.eu/spip.php?article6264",
        "MGP_Hongrie_Futog_Salvon": "https://graphbz.eu/spip.php?article6262",
        "SAY_Centre_Chargé": "https://graphbz.eu/spip.php?article6279",
        "SAY_Jack": "https://graphbz.eu/spip.php?article6280",
        "SAY_simples": "https://graphbz.eu/spip.php?article6281",
        "Réni_Biberau": "https://graphbz.eu/spip.php?article6312",
        "Réni_classique": "https://graphbz.eu/spip.php?article6313",
        "Réni_tardif": "https://graphbz.eu/spip.php?article6314",
        "tores_oves_chevrons": "https://graphbz.eu/spip.php?article6363",
        "tores_hachures_brisées": "https://graphbz.eu/spip.php?article6362",
        "MGP_Rosan_classique": "https://graphbz.eu/spip.php?article6277",
        "MGP_Rosan_Tardif": "https://graphbz.eu/spip.php?article6380",
        "MGP_Rosan_Chusclan_Siccieu": "https://graphbz.eu/spip.php?article6278",
        "Ph_0": "https://graphbz.eu/spip.php?article6168",
        "gpe_Pologne_triangles": "https://graphbz.eu/spip.php?article6228",
        "gpe_Pologne_Chevrons": "https://graphbz.eu/spip.php?article6226",
        "gpe_Pologne_courbes": "https://graphbz.eu/spip.php?article6227",
        "MGP_tampons_à_obliques": "https://graphbz.eu/spip.php?article6350",
        "MGP_tampons_étagés": "https://graphbz.eu/spip.php?article6353",
        "MGP_tampons_barques": "https://graphbz.eu/spip.php?article6351",
        "MGP_tampons_chevrons_frêles": "https://graphbz.eu/spip.php?article6352",
        "Subingen_triangles_chevrons": "https://graphbz.eu/spip.php?article6356",
        "Subingen_triangles_chevrons_étagés": "https://graphbz.eu/spip.php?article6357",
        "Subingen_oves_losanges": "https://graphbz.eu/spip.php?article6355",
        "Subingen_courbes": "https://graphbz.eu/spip.php?article6354",
        "Pologne_ha_oves": "https://graphbz.eu/spip.php?article6365",
        "Pologne_ha_chevrons": "https://graphbz.eu/spip.php?article6364",
        "nord_à_courbures_courtes": "https://graphbz.eu/spip.php?article6338",
        "nord_à_courbures_longues": "https://graphbz.eu/spip.php?article6339",
        "nord_triangles": "https://graphbz.eu/spip.php?article6341",
        "nord_chevrons": "https://graphbz.eu/spip.php?article6340",
        "Morges_prépa": "https://graphbz.eu/spip.php?article6310",
        "Morges_classique": "https://graphbz.eu/spip.php?article6311",
        "Macédoine": "https://graphbz.eu/spip.php?article6204",
        "Meck_triangles_3": "https://graphbz.eu/spip.php?article6260",
        "Meck_triangles_1": "https://graphbz.eu/spip.php?article6259",
        "Meck_bipartition": "https://graphbz.eu/spip.php?article6258",
        "Mitterkirchen_triangles_oves": "https://graphbz.eu/spip.php?article6361",
        "Mitterkirchen_lignes_oves": "https://graphbz.eu/spip.php?article6359",
        "Mitterkirchen_triangles_associés": "https://graphbz.eu/spip.php?article6360",
        "Mitterkirchen_Latin": "https://graphbz.eu/spip.php?article6358",
        "LT_A_courbes": "https://graphbz.eu/spip.php?article6372",
        "LT_A_oves": "https://graphbz.eu/spip.php?article6373",
        "LT_A_chevrons": "https://graphbz.eu/spip.php?article6371",
        "LT_A_anthropomorphe": "https://graphbz.eu/spip.php?article6370",
        "Mola_Mola": "https://graphbz.eu/spip.php?article6348",
        "Mola_précoce": "https://graphbz.eu/spip.php?article6346",
        "Mola_classique": "https://drive.google.com/graphbz.eu/spip.php?article6347",
        "Mola_oves": "https://drive.google.com/graphbz.eu/spip.php?article6349",
        "Lunebourg_courbes_libres": "https://graphbz.eu/spip.php?article6250",
        "Lunebourg_5etplus": "https://graphbz.eu/spip.php?article6249",
        "Lunebourg_3": "https://graphbz.eu/spip.php?article6247",
        "Lunebourg_4": "https://graphbz.eu/spip.php?article6248",
        "Lunebourg_hz": "https://graphbz.eu/spip.php?article6251",
        "sorti": "https://graphbz.eu/spip.php?article",
        "Morave_obliques": "https://graphbz.eu/spip.php?article6307",
        "Morave_tardif": "https://graphbz.eu/spip.php?article6309",
        "Morave_chevrons_brisés": "https://graphbz.eu/spip.php?article6304",
        "morave_quadrige": "https://graphbz.eu/spip.php?article6308",
        "morave_éclair": "https://graphbz.eu/spip.php?article6306",
        "Morave_courbes_centrées": "https://graphbz.eu/spip.php?article6305",
        "Meck_obliques_en_3ou4": "https://graphbz.eu/spip.php?article6255",
        "Meck_obliques_simples_brisées": "https://graphbz.eu/spip.php?article6257",
        "Meck_obliques_simples": "https://graphbz.eu/spip.php?article6256",
        "Meck_obliques_1bis": "https://graphbz.eu/spip.php?article6253",
        "Meck_obliques_bipartites": "https://graphbz.eu/spip.php?article6254",
        "Meck_obliques_1": "https://graphbz.eu/spip.php?article6252",
        "Locarno_centre_2": "https://graphbz.eu/spip.php?article6379",
        "Locarno_centre_1": "https://graphbz.eu/spip.php?article6275",
        "Locarno_bipartite": "https://graphbz.eu/spip.php?article6274",
        "Locarno_centre_3": "https://graphbz.eu/spip.php?article6276",
        "jambières_lignes": "https://graphbz.eu/spip.php?article6271",
        "jambières_barques": "https://graphbz.eu/spip.php?article6270",
        "jambières_triangles_simples": "https://graphbz.eu/spip.php?article6268",
        "jambières_triangles_complexes": "https://graphbz.eu/spip.php?article6269",
        "Haguenau_dérivé": "https://graphbz.eu/spip.php?article6225",
        "Haguenau_classique": "https://graphbz.eu/spip.php?article6224",
        "Esta_précoce": "https://graphbz.eu/spip.php?article6332",
        "Esta_tardif": "https://graphbz.eu/spip.php?article6333",
        "Dhrovice_SUD": "https://graphbz.eu/spip.php?article6345",
        "Dhrovice_oves_lignes": "https://graphbz.eu/spip.php?article6344",
        "Dhrovice_classique": "https://graphbz.eu/spip.php?article6343",
        "Dhrovice_barques": "https://graphbz.eu/spip.php?article6342",
        "Leupolz_sillons": "https://graphbz.eu/spip.php?article6295",
        "Leupolz_simples_garnitures_triangles": "https://graphbz.eu/spip.php?article6297",
        "Leupolz_rectangles_centrés": "https://graphbz.eu/spip.php?article6294",
        "Leupolz_simples_garnitures_Courbes": "https://graphbz.eu/spip.php?article6296",
        "Leupolz_frises_volutes": "https://graphbz.eu/spip.php?article6292",
        "Leupolz_barques_pointues": "https://graphbz.eu/spip.php?article6289",
        "Leupolz_barques_simples": "https://graphbz.eu/spip.php?article6290",
        "Leupolz_barques": "https://graphbz.eu/spip.php?article6288",
        "Leupolz_frises": "https://graphbz.eu/spip.php?article6291",
        "c_Danube_oves_3et4": "https://graphbz.eu/spip.php?article6222",
        "c_Danube_oves_plus_de_4": "https://graphbz.eu/spip.php?article6223",
        "c_Danube_courbes_4": "https://graphbz.eu/spip.php?article6221",
        "c_Danube_courbes_2": "https://graphbz.eu/spip.php?article6219",
        "c_Danube_courbes_3": "https://graphbz.eu/spip.php?article6220",
        "Kasidol_courbes_div": "https://graphbz.eu/spip.php?article6302",
        "Kasidol_centre_2à3": "https://graphbz.eu/spip.php?article6300",
        "Kasidol_obliques": "https://graphbz.eu/spip.php?article6303",
        "kasidol_courbes_alternées": "https://graphbz.eu/spip.php?article6301",
        "Kasidol_brisées": "https://graphbz.eu/spip.php?article6299",
        "Kasidol_baroques": "https://graphbz.eu/spip.php?article6298",
        "geométrique_et_anthopomorphe_4": "https://graphbz.eu/spip.php?article6377",
        "geométrique_et_anthopomorphe_5": "https://graphbz.eu/spip.php?article6378",
        "geométrique_et_anthopomorphe_3": "https://graphbz.eu/spip.php?article6376",
        "geométrique_et_anthopomorphe_2": "https://graphbz.eu/spip.php?article6375",
        "geométrique_et_anthopomorphe_1": "https://graphbz.eu/spip.php?article6374",
        "coubes_verticales": "https://graphbz.eu/spip.php?article6181",
        "Corcelettes_très_tardifs": "https://graphbz.eu/spip.php?article6325",
        "Corcelettes_tardifs": "https://graphbz.eu/spip.php?article6381",
        "Corcelettes_précoces": "https://graphbz.eu/spip.php?article6317",
        "Corcelettes_préclassiques": "https://graphbz.eu/spip.php?article6319",
        "Corcelettes_protoclassiques": "https://graphbz.eu/spip.php?article6318",
        "Corcelettes_Patchwork_précoce": "https://graphbz.eu/spip.php?article6323",
        "Corcelettes_Patchwork": "https://graphbz.eu/spip.php?article6324",
        "Corcelettes_baroques": "https://graphbz.eu/spip.php?article6322",
        "Corcelettes_classiques": "https://graphbz.eu/spip.php?article6321",
        "Corcelettes_classiques_précoce": "https://graphbz.eu/spip.php?article6320",
        "Clans_évolué": "https://graphbz.eu/spip.php?article6273",
        "Clans_type": "https://graphbz.eu/spip.php?article6272",
        "Groupe_Angleterre_bis": "https://graphbz.eu/spip.php?article6174",
        "Bignan_classique": "https://graphbz.eu/spip.php?article6229",
        "Bignan_évolué": "https://graphbz.eu/spip.php?article6231",
        "chevrons occidentaux": "https://graphbz.eu/spip.php?article6316",
        "chevrons gras": "https://graphbz.eu/spip.php?article6315",
        "B_Danube_avec_triangles": "https://graphbz.eu/spip.php?article6218",
        "B_avec_oves_et_triangles": "https://graphbz.eu/spip.php?article6217",
        "B_avec_oves_et_chevrons": "https://graphbz.eu/spip.php?article6216",
        "B_avec_oves": "https://graphbz.eu/spip.php?article6215",
        "Agde_évolué_grands_chevrons": "https://graphbz.eu/spip.php?article6367",
        "Agde_évolué_classique": "https://graphbz.eu/spip.php?article6366",
        "barques_ongroise_bis": "https://graphbz.eu/spip.php?article6182",
        "Auvernier_oblique_simple": "https://graphbz.eu/spip.php?article6331",
        "Auvernier_Loire_2": "https://graphbz.eu/spip.php?article6330",
        "Auvernier_Loire": "https://graphbz.eu/spip.php?article6329",
        "Auvernier_classique_2": "https://graphbz.eu/spip.php?article6327",
        "Auvernier_classique_3": "https://graphbz.eu/spip.php?article6328",
        "Auvernier_classique": "https://graphbz.eu/spip.php?article6326",
        "brassart_Ha_tardif": "https://graphbz.eu/spip.php?article6369",
        "brassart_Ha_precoce": "https://graphbz.eu/spip.php?article6368",
        "Moora": "https://graphbz.eu/spip.php?article6212"}

dico2 = {"MGP_Borniga_Cimiez": "032-01",
         "MGP_Larnaud_Limone": "032-02",
         "MGP_Nessi_Camaiore": "032-04",
         "MGP_Pariana_Paveze": "032-03",
         "wabern_quadrillé": "008-07",
         "Wabern_courbes": "008-04",
         "Wabern_tiretés": "008-08",
         "Wabern_frise": "008-06",
         "Wabern_évolué": "008-05",
         "Wabern_centré_long": "008-03",
         "Wabern_centré": "008-02",
         "Wabern_barques": "008-01",
         "Vinol_triangles_2": "009-05",
         "Vinol_chevrons_centrés": "009-01",
         "Vinol_courbes": "009-02",
         "Vinol_triangles": "009-04",
         "Vinol_oves": "009-03",
         "Vinol_triangles_3": "009-06",
         "Ukraine_4_3": "022-02",
         "Ukraine_4_4": "022-03",
         "Ukraine_croix": "022-06",
         "Ukraine_4_5": "022-04",
         "Ukraine_continu": "022-05",
         "Ukraine_3_4": "022-01",
         "MGP_Hongrie_triangles_reliés": "013-06",
         "MGP_Hongrie_triangles affrontés": "013-03",
         "MGP_Hongrie_Courbes_hongroises": "013-01",
         "MGP_Hongrie_triangles_ultrasimples": "013-07",
         "MGP_Hongrie_triangles_chevrons": "013-05",
         "MGP_Hongrie_triangles_chargés": "013-04",
         "MGP_Hongrie_Futog_Salvon": "013-02",
         "SAY_Centre_Chargé": "021-01",
         "SAY_Jack": "021-02",
         "SAY_simples": "021-03",
         "Réni_Biberau": "027-01",
         "Réni_classique": "027-02",
         "Réni_tardif": "027-03",
         "tores_oves_chevrons": "040-02",
         "tores_hachures_brisées": "040-01",
         "MGP_Rosan_classique": "020-01",
         "MGP_Rosan_Tardif": "020-02",
         "MGP_Rosan_Chusclan_Siccieu": "020-03",
         "Ph_0": "001",
         "gpe_Pologne_triangles": "005-03",
         "gpe_Pologne_Chevrons": "005-01",
         "gpe_Pologne_courbes": "005-02",
         "MGP_tampons_à_obliques": "036-01",
         "MGP_tampons_étagés": "036-04",
         "MGP_tampons_barques": "036-02",
         "MGP_tampons_chevrons_frêles": "036-03",
         "Subingen_triangles_chevrons": "038-03",
         "Subingen_triangles_chevrons_étagés": "038-04",
         "Subingen_oves_losanges": "038-02",
         "Subingen_courbes": "038-01",
         "Pologne_ha_oves": "041-02",
         "Pologne_ha_chevrons": "041-01",
         "nord_à_courbures_courtes": "033-01",
         "nord_à_courbures_longues": "033-02",
         "nord_triangles": "033-04",
         "nord_chevrons": "033-03",
         "Morges_prépa": "026-01",
         "Morges_classique": "026-02",
         "Macédoine": "037",
         "Meck_triangles_3": "012-03",
         "Meck_triangles_1": "012-02",
         "Meck_bipartition": "012-01",
         "Mitterkirchen_triangles_oves": "039-04",
         "Mitterkirchen_lignes_oves": "039-02",
         "Mitterkirchen_triangles_associés": "039-03",
         "Mitterkirchen_Latin": "039-01",
         "LT_A_courbes": "044-03",
         "LT_A_oves": "044-04",
         "LT_A_chevrons": "044-02",
         "LT_A_anthropomorphe": "044-01",
         "Mola_Mola": "035-03",
         "Mola_précoce": "035-01",
         "Mola_classique": "035-02",
         "Mola_oves": "035-04",
         "Lunebourg_courbes_libres": "010-04",
         "Lunebourg_5etplus": "010-03",
         "Lunebourg_3": "010-01",
         "Lunebourg_4": "010-02",
         "Lunebourg_hz": "010-05",
         "sorti": "ANNULATION",
         "Morave_obliques": "025-04",
         "Morave_tardif": "025-06",
         "Morave_chevrons_brisés": "025-01",
         "morave_quadrige": "025-05",
         "morave_éclair": "025-03",
         "Morave_courbes_centrées": "025-02",
         "Meck_obliques_en_3ou4": "011-04",
         "Meck_obliques_simples_brisées": "011-06",
         "Meck_obliques_simples": "011-05",
         "Meck_obliques_1bis": "011-02",
         "Meck_obliques_bipartites": "011-03",
         "Meck_obliques_1": "011-01",
         "Locarno_centre_2": "019-03",
         "Locarno_centre_1": "019-02",
         "Locarno_bipartite": "019-01",
         "Locarno_centre_3": "019-04",
         "jambières_lignes": "017-02",
         "jambières_barques": "017-01",
         "jambières_triangles_simples": "016-01",
         "jambières_triangles_complexes": "016-02",
         "Haguenau_dérivé": "004-02",
         "Haguenau_classique": "004-01",
         "Esta_précoce": "031-01",
         "Esta_tardif": "031-02",
         "Dhrovice_SUD": "034-04",
         "Dhrovice_oves_lignes": "034-03",
         "Dhrovice_classique": "034-02",
         "Dhrovice_barques": "034-01",
         "Leupolz_sillons": "023-07",
         "Leupolz_simples_garnitures_triangles": "023-09",
         "Leupolz_rectangles_centrés": "023-06",
         "Leupolz_simples_garnitures_Courbes": "023-08",
         "Leupolz_frises_volutes": "023-05",
         "Leupolz_barques_pointues": "023-02",
         "Leupolz_barques_simples": "023-03",
         "Leupolz_barques": "023-01",
         "Leupolz_frises": "023-04",
         "c_Danube_oves_3et4": "003-04",
         "c_Danube_oves_plus_de_4": "003-05",
         "c_Danube_courbes_4": "003-03",
         "c_Danube_courbes_2": "003-01",
         "c_Danube_courbes_3": "003-02",
         "Kasidol_courbes_div": "024-05",
         "Kasidol_centre_2à3": "024-03",
         "Kasidol_obliques": "024-06",
         "kasidol_courbes_alternées": "024-04",
         "Kasidol_brisées": "024-02",
         "Kasidol_baroques": "024-01",
         "geométrique_et_anthopomorphe_4": "046-04",
         "geométrique_et_anthopomorphe_5": "046-05",
         "geométrique_et_anthopomorphe_3": "046-03",
         "geométrique_et_anthopomorphe_2": "046-02",
         "geométrique_et_anthopomorphe_1": "046-01",
         "coubes_verticales": "014",
         "Corcelettes_très_tardifs": "029-10",
         "Corcelettes_tardifs": "029-09",
         "Corcelettes_précoces": "029-01",
         "Corcelettes_préclassiques": "029-03",
         "Corcelettes_protoclassiques": "029-02",
         "Corcelettes_Patchwork_précoce": "029-07",
         "Corcelettes_Patchwork": "029-08",
         "Corcelettes_baroques": "029-06",
         "Corcelettes_classiques": "029-05",
         "Corcelettes_classiques_précoce": "29-04",
         "Clans_évolué": "018-02",
         "Clans_type": "018-01",
         "Groupe_Angleterre_bis": "007",
         "Bignan_classique": "006-01",
         "Bignan_évolué": "006-02",
         "chevrons occidentaux": "028-02",
         "chevrons gras": "028-01",
         "B_Danube_avec_triangles": "002-04",
         "B_avec_oves_et_triangles": "002-03",
         "B_avec_oves_et_chevrons": "002-02",
         "B_avec_oves": "002-01",
         "Agde_évolué_grands_chevrons": "042-02",
         "Agde_évolué_classique": "042-01",
         "barques_ongroise_bis": "015",
         "Auvernier_oblique_simple": "030-06",
         "Auvernier_Loire_2": "030-05",
         "Auvernier_Loire": "030-04",
         "Auvernier_classique_2": "030-02",
         "Auvernier_classique_3": "030-03",
         "Auvernier_classique": "030-01",
         "brassart_Ha_tardif": "043-02",
         "brassart_Ha_precoce": "043-01",
         "Moora": "045"}


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)


async def setup_learner():
    await download_file(model_file_url, model_path / model_file_name)
    learn = load_learner(model_path / model_file_name)
    print("learner loaded !")
    return learn


learn = asyncio.run(setup_learner())
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/None', methods=['GET', 'POST'])
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

        _, _, probs = learn.predict("downloads/temp.png")
        # classes = learn.dls.vocab
        classes = ['gpe_Agde_évolué', 'gpe_Angleterre', 'gpe_Auvernier', 'gpe_B_Danube', 'gpe_Bignan', 'gpe_Clans', 'gpe_Corcelettes', 'gpe_Dhrovice', 'gpe_Estavayer', 'gpe_Haguenau', 'gpe_LT_A', 'gpe_Leupolz', 'gpe_Locarno', 'gpe_Lunebourg', 'gpe_Macédoine', 'gpe_Mecklenburg_obliques', 'gpe_Mecklenburg_triangles', 'gpe_Mitterkirchen', 'gpe_Mola', 'gpe_Moora', 'gpe_Morges', 'gpe_Ph_0', 'gpe_Pologne', 'gpe_Pologne_Ha', 'gpe_Rosan', 'gpe_SAY', 'gpe_Subingen', 'gpe_Ukraine', 'gpe_Vinol', 'gpe_Wabern', 'gpe_Zerba', 'gpe_barques_hongroises', 'gpe_brassart_Ha', 'gpe_c_Danube', 'gpe_chevrons', 'gpe_coubes_verticales', 'gpe_geométrique_et_anthopomorphe', 'gpe_jambières_barques_et_lignes', 'gpe_jambières_triangles', 'gpe_kasidol', 'gpe_morave', 'gpe_nord', 'gpe_réniforme', 'gpe_tampons', 'gpe_tores', 'gpe_triangles_Hongrie']
        predictions = sorted(zip(classes, map(float, probs)), key=lambda p: p[1], reverse=True)
        print(classes)

        path = os.sep.join(["static", "images", "Vignettes"])
        #         # print(os.listdir(path))
        prediction = [str(predictions[0][0])[4:],
                      str(predictions[1][0])[4:],
                      str(predictions[2][0])[4:]]

        #         prediction2 = [dico2.get(str(predictions[0][0])[4:],""),
        #                       dico2.get(str(predictions[1][0])[4:],""),
        #                       dico2.get(str(predictions[2][0])[4:],"")]
        # prediction[1] = "jambières_triangles"
        print(prediction)

        probas = [str('%.2f' % (predictions[0][1] * 100)) + "%",
                  str('%.2f' % (predictions[1][1] * 100)) + "%",
                  str('%.2f' % (predictions[2][1] * 100)) + "%"]

        result1 = []
        result2 = []
        result3 = []

        for sub_class in os.listdir(os.sep.join([path, prediction[0]])):
            for image in os.listdir(os.sep.join([path, prediction[0], sub_class])):
                if sub_class == "general":
                    result1.append((os.sep.join([path, prediction[0], sub_class, image]), dico2.get(prediction[0], ""),
                                    dico.get(sub_class)))

                else:
                    result1.append((os.sep.join([path, prediction[0], sub_class, image]), dico2.get(sub_class, ""),
                                    dico.get(sub_class)))

        for sub_class in os.listdir(os.sep.join([path, prediction[1]])):
            for image in os.listdir(os.sep.join([path, prediction[1], sub_class])):
                if sub_class == "general":
                    result2.append((os.sep.join([path, prediction[1], sub_class, image]), dico2.get(prediction[1], ""),
                                    dico.get(sub_class)))

                else:
                    result2.append((os.sep.join([path, prediction[1], sub_class, image]), dico2.get(sub_class, ""),
                                    dico.get(sub_class)))

        for sub_class in os.listdir(os.sep.join([path, prediction[2]])):
            for image in os.listdir(os.sep.join([path, prediction[2], sub_class])):
                if sub_class == "general":
                    result3.append((os.sep.join([path, prediction[2], sub_class, image]), dico2.get(prediction[2], ""),
                                    dico.get(sub_class)))

                else:
                    result3.append((os.sep.join([path, prediction[2], sub_class, image]), dico2.get(sub_class, ""),
                                    dico.get(sub_class)))

        return render_template('result.html', prediction=prediction, probas=probas,
                               result1=sorted(result1, key=itemgetter(1)),
                               result2=sorted(result2, key=itemgetter(1)),
                               result3=sorted(result3, key=itemgetter(1)))

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
