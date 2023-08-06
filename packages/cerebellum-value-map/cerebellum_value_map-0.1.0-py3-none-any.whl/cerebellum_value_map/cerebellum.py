"""Classes to create a cerebellum illustration.

"""
from enum import Enum
from svgwrite import Drawing

from .path_code import Move as M
from .path_code import Line as L
from .path_code import BezierCurve as C
from .path_code import QuadraticCurve as Q

from .shape import PathShape as PS
from .shape import AnnotatedShape
from .colors import DiscreteColors, ContinousColors, CerebellumLabelColors


axis = 270.312
"""float: The flipping axis to create the left counter-part from the right."""

default_lobe_names = ['Corpus Medullare', 'Vermis',
                        'Left Anterior', 'Right Anterior',
                        'Left Superior Posterior', 'Right Superior Posterior',
                        'Left Inferior Posterior', 'Right Inferior Posterior',
                        'Left X', 'Right X']
"""list[str]: The region names of a default lobe illustration."""

default_lobule_names = ['Corpus Medullare', 'Left I-III', 'Right I-III',
                        'Left IV', 'Right IV', 'Left V', 'Right V', 'Vermis VI',
                        'Left VI', 'Right VI', 'Vermis VII', 'Left Crus I',
                        'Left Crus II', 'Left VIIB', 'Right Crus I',
                        'Right Crus II', 'Right VIIB', 'Vermis VIII',
                        'Left VIIIA', 'Left VIIIB', 'Right VIIIA',
                        'Right VIIIB', 'Vermis IX', 'Left IX', 'Right IX',
                        'Vermis X', 'Left X', 'Right X']
"""list[str]: The region names of a default lobules illustration."""


class RegionName(str, Enum):
    """Enum of cerebellar regions.

    To show all regions:

    >>> print(list(RegionName))

    """
    CORPUS_MEDULLARE = 'Corpus Medullare'

    RIGHT_ANTERIOR = 'Right Anterior'
    LEFT_ANTERIOR = 'Left Anterior'
    RIGHT_SUPERIOR_POSTERIOR = 'Right Superior Posterior'
    LEFT_SUPERIOR_POSTERIOR = 'Left Superior Posterior'
    RIGHT_INFERIOR_POSTERIOR = 'Right Inferior Posterior'
    LEFT_INFERIOR_POSTERIOR = 'Left Inferior Posterior'
    VERMIS = 'Vermis'

    RIGHT_I_III = 'Right I-III'
    LEFT_I_III = 'Left I-III'
    RIGHT_IV = 'Right IV'
    LEFT_IV = 'Left IV'
    RIGHT_V = 'Right V'
    LEFT_V = 'Left V'
    RIGHT_VI = 'Right VI'
    LEFT_VI = 'Left VI'
    RIGHT_CRUS_I = 'Right Crus I'
    LEFT_CRUS_I = 'Left Crus I'
    RIGHT_CRUS_II = 'Right Crus II'
    LEFT_CRUS_II = 'Left Crus II'
    RIGHT_VIIB = 'Right VIIB'
    LEFT_VIIB = 'Left VIIB'
    RIGHT_VIIIA = 'Right VIIIA'
    LEFT_VIIIA = 'Left VIIIA'
    RIGHT_VIIIB = 'Right VIIIB'
    LEFT_VIIIB = 'Left VIIIB'
    RIGHT_IX = 'Right IX'
    LEFT_IX = 'Left IX'
    RIGHT_X = 'Right X'
    LEFT_X = 'Left X'
    VERMIS_VI = 'Vermis VI'
    VERMIS_VII = 'Vermis VII'
    VERMIS_VIII = 'Vermis VIII'
    VERMIS_IX = 'Vermis IX'
    VERMIS_X = 'Vermis X'


def create_region(name):
    """Creates a cerebellar region.

    Args:
        name (str, RegionName): The name of the region.

    Returns:
        cerebellum_value_map.shape.PathShape: The created cerebellar region.

    """
    name = RegionName(name)
    if name is RegionName.CORPUS_MEDULLARE:
        shape = PS(M((283.78, 612.977)),
                   C((274.825, 604.487), (249.658, 598.366), (220.045, 598.366)),
                   C((182.941, 598.366), (152.817, 607.976), (152.817, 619.813)),
                   C((152.817, 631.65), (182.941, 641.26), (220.045, 641.26)),
                   C((250.207, 641.26), (275.756, 634.91), (284.261, 626.175)),
                   L((311.326, 626.175)),
                   C((319.831, 634.91), (345.38, 641.26), (375.542, 641.26)),
                   C((412.646, 641.26), (442.77, 631.65), (442.77, 619.813)),
                   C((442.77, 607.976), (412.646, 598.366), (375.542, 598.366)),
                   C((345.929, 598.366), (320.762, 604.487), (311.807, 612.977)),
                   L((283.78, 612.977)))
        shape = shape.translate(-27.481, -230)
    if name is RegionName.RIGHT_ANTERIOR:
        shape = PS(M((270.312, 70.869)),
                   Q((274.155, 64.277), (278.375, 61.375)),
                   C((290.669, 52.918), (307.091, 50.685), (319.875, 56.125)),
                   Q((323.261, 57.566), (328.125, 63.125)),
                   Q((331.406, 55.304), (335.654, 54.348)),
                   C((338.351, 53.742), (341.246, 53.606), (343.176, 55.759)),
                   Q((344.213, 56.915), (344.779, 59.782)),
                   Q((347.331, 57.258), (349.165, 56.734)),
                   Q((354.215, 55.291), (359.126, 60.434)),
                   Q((358.167, 75.500), (355.167, 91.500)),
                   C((352.819, 104.022), (346.692, 113.906), (337.500, 122.833)),
                   C((326.737, 133.287), (315.500, 140.500), (299.500, 140.500)),
                   Q((289.500, 140.500), (270.312, 140.500)))
    elif name is RegionName.RIGHT_SUPERIOR_POSTERIOR:
        shape = PS(M((300.365, 140.509)),
                   C((315.500, 140.500), (326.737, 133.287), (337.500, 122.833)),
                   C((346.692, 113.906), (352.819, 104.022), (355.167, 91.500)),
                   Q((358.167, 75.500), (358.500, 61.167)),
                   Q((365.019, 57.163), (368.049, 57.985)),
                   C((372.865, 59.292), (376.924, 61.298), (381.576, 67.713)),
                   C((384.250, 71.400), (389.063, 77.520), (390.432, 83.974)),
                   C((391.306, 88.090), (390.749, 93.433), (390.723, 95.879)),
                   Q((393.364, 95.964), (400.683, 97.428)),
                   C((415.842, 100.460), (425.291, 114.140), (431.000, 126.875)),
                   C((437.547, 141.481), (446.067, 157.860), (444.250, 174.000)),
                   Q((443.479, 180.846), (435.250, 181.500)),
                   Q((441.827, 184.889), (442.750, 187.000)),
                   C((446.250, 195.000), (448.564, 211.972), (447.250, 221.500)),
                   Q((445.250, 236.000), (430.250, 236.500)),
                   C((438.162, 237.161), (443.593, 237.177), (446.515, 236.516)),
                   C((450.218, 235.679), (451.913, 240.005), (452.336, 245.035)),
                   C((452.610, 248.300), (452.348, 251.862), (451.750, 254.500)),
                   C((450.830, 258.557), (447.975, 262.993), (443.750, 265.500)),
                   Q((439.833, 267.824), (431.250, 267.500)),
                   L((425.331, 266.551)),
                   Q((404.333, 253.333), (375.000, 242.667)),
                   C((358.161, 236.543), (345.424, 234.789), (329.000, 232.667)),
                   Q((308.746, 230.050), (298.662, 230.735)),
                   Q((301.302, 226.059), (301.701, 223.206)),
                   Q((302.370, 218.411), (298.095, 210.306)),
                   Q((300.704, 205.610), (301.019, 202.768)),
                   Q((301.701, 196.637), (296.960, 186.473)),
                   Q((301.154, 182.519), (301.701, 179.606)),
                   Q((302.722, 174.156), (299.230, 163.775)),
                   Q((301.619, 157.830), (302.041, 154.400)),
                   Q((302.648, 149.473), (300.365, 140.509)))
    elif name is RegionName.RIGHT_INFERIOR_POSTERIOR:
        shape = PS(M((298.662, 230.735)),
                   Q((308.746, 230.050), (329.000, 232.667)),
                   C((345.424, 234.789), (358.161, 236.543), (375.000, 242.667)),
                   Q((404.333, 253.333), (424.333, 267.333)),
                   Q((425.741, 274.893), (422.774, 278.823)),
                   Q((420.122, 282.335), (407.945, 287.005)),
                   Q((408.802, 292.724), (407.945, 295.697)),
                   C((406.962, 299.108), (405.231, 301.825), (402.320, 303.879)),
                   Q((398.626, 306.486), (390.048, 305.924)),
                   Q((387.321, 309.803), (385.446, 311.549)),
                   C((381.696, 315.042), (375.127, 315.528), (372.663, 318.196)),
                   Q((368.086, 323.153), (366.016, 333.025)),
                   Q((358.333, 334.000), (347.000, 329.333)),
                   C((329.877, 322.283), (328.333, 306.667), (317.667, 298.000)),
                   C((310.570, 292.234), (303.394, 288.949), (299.230, 286.913)),
                   Q((301.774, 281.783), (302.630, 278.808)),
                   Q((304.682, 271.680), (302.634, 257.973)),
                   Q((303.638, 253.404), (303.105, 250.959)),
                   Q((302.461, 248.006), (298.662, 243.786)),
                   Q((300.564, 240.080), (300.679, 237.852)),
                   Q((300.815, 235.209), (298.662, 230.735)))
    elif name is RegionName.VERMIS:
        shape = PS(M((270.312, 140.500)),
                   Q((289.500, 140.500), (300.365, 140.509)),
                   Q((302.648, 149.473), (302.041, 154.400)),
                   Q((301.619, 157.830), (299.230, 163.775)),
                   Q((302.722, 174.156), (301.701, 179.606)),
                   Q((301.154, 182.519), (296.960, 186.473)),
                   Q((301.701, 196.637), (301.019, 202.768)),
                   Q((300.704, 205.610), (298.095, 210.306)),
                   Q((302.370, 218.411), (301.701, 223.206)),
                   Q((301.302, 226.059), (298.662, 230.735)),
                   Q((300.815, 235.209), (300.679, 237.852)),
                   Q((300.564, 240.080), (298.662, 243.786)),
                   Q((302.461, 248.006), (303.105, 250.959)),
                   Q((303.638, 253.404), (302.634, 257.973)),
                   Q((304.682, 271.680), (302.630, 278.808)),
                   Q((301.774, 281.783), (299.230, 286.913)),
                   C((299.699, 302.623), (299.198, 314.095), (297.170, 322.885)),
                   C((296.030, 327.828), (293.406, 337.904), (287.880, 342.523)),
                   C((283.269, 346.377), (274.064, 346.759), (270.312, 346.575)),
                   C((266.560, 346.759), (257.355, 346.377), (252.744, 342.523)),
                   C((247.218, 337.904), (244.594, 327.828), (243.454, 322.885)),
                   C((241.426, 314.095), (240.925, 302.623), (241.394, 286.913)),
                   Q((238.850, 281.783), (237.994, 278.808)),
                   Q((235.942, 271.680), (237.990, 257.973)),
                   Q((236.986, 253.404), (237.519, 250.959)),
                   Q((238.163, 248.006), (241.962, 243.786)),
                   Q((240.060, 240.080), (239.945, 237.852)),
                   Q((239.809, 235.209), (241.962, 230.735)),
                   Q((239.322, 226.059), (238.923, 223.206)),
                   Q((238.254, 218.411), (242.529, 210.306)),
                   Q((239.920, 205.610), (239.605, 202.768)),
                   Q((238.923, 196.637), (243.664, 186.473)),
                   Q((239.470, 182.519), (238.923, 179.606)),
                   Q((237.902, 174.156), (241.394, 163.775)),
                   Q((239.005, 157.830), (238.583, 154.400)),
                   Q((237.976, 149.473), (240.259, 140.509)),
                   Q((251.124, 140.500), (270.312, 140.500)))
    elif name is RegionName.RIGHT_I_III:
        shape = PS(M((270.312, 70.869)),
                   Q((274.155, 64.277), (278.375, 61.375)),
                   C((290.669, 52.918), (307.091, 50.685), (319.875, 56.125)),
                   Q((323.261, 57.566), (328.125, 63.125)),
                   Q((322.173, 76.358), (317.575, 81.694)),
                   C((311.572, 88.661), (304.230, 93.927), (296.446, 96.707)),
                   Q((287.669, 99.841), (270.312, 97.819)))
    elif name is RegionName.RIGHT_IV:
        shape = PS(M((270.312, 97.819)),
                   Q((287.669, 99.841), (296.446, 96.707)),
                   C((304.230, 93.927), (311.572, 88.661), (317.575, 81.694)),
                   Q((322.173, 76.358), (328.125, 63.125)),
                   Q((331.406, 55.304), (335.654, 54.348)),
                   C((338.351, 53.742), (341.246, 53.606), (343.176, 55.759)),
                   Q((344.213, 56.915), (344.779, 59.782)),
                   Q((343.040, 77.802), (338.036, 87.254)),
                   C((334.798, 93.371), (331.535, 97.957), (326.360, 102.267)),
                   C((319.403, 108.060), (311.974, 111.902), (303.006, 112.276)),
                   Q((289.661, 112.832), (270.312, 112.276)))
    elif name is RegionName.RIGHT_V:
        shape = PS(M((270.312, 112.276)),
                   Q((289.661, 112.832), (303.006, 112.276)),
                   C((311.974, 111.902), (319.403, 108.060), (326.360, 102.267)),
                   C((331.535, 97.957), (334.798, 93.371), (338.036, 87.254)),
                   Q((343.040, 77.802), (344.779, 59.782)),
                   Q((347.331, 57.258), (349.165, 56.734)),
                   Q((354.215, 55.291), (359.126, 60.434)),
                   Q((358.167, 75.500), (355.167, 91.500)),
                   C((352.819, 104.022), (346.692, 113.906), (337.500, 122.833)),
                   C((326.737, 133.287), (315.500, 140.500), (299.500, 140.500)),
                   Q((289.500, 140.500), (270.312, 140.500)))
    elif name is RegionName.RIGHT_VI:
        shape = PS(M((300.365, 140.509)),
                   C((315.500, 140.500), (326.737, 133.287), (337.500, 122.833)),
                   C((346.692, 113.906), (352.819, 104.022), (355.167, 91.500)),
                   Q((358.167, 75.500), (358.500, 61.167)),
                   Q((365.019, 57.163), (368.049, 57.985)),
                   C((372.865, 59.292), (376.924, 61.298), (381.576, 67.713)),
                   C((384.250, 71.400), (389.063, 77.520), (390.432, 83.974)),
                   C((391.306, 88.090), (390.749, 93.433), (390.723, 95.879)),
                   Q((390.702, 97.769), (389.561, 101.106)),
                   Q((374.821, 130.602), (360.732, 143.544)),
                   C((352.967, 150.677), (345.537, 157.448), (333.210, 161.073)),
                   C((316.500, 165.988), (303.721, 165.333), (298.479, 165.333)),
                   Q((301.619, 157.830), (302.041, 154.400)),
                   Q((302.648, 149.473), (300.365, 140.509)))
    elif name is RegionName.RIGHT_CRUS_I:
        shape = PS(M((299.230, 163.775)),
                   C((303.721, 165.333), (316.500, 165.988), (333.210, 161.073)),
                   C((345.537, 157.448), (352.967, 150.677), (360.732, 143.544)),
                   Q((374.821, 130.602), (389.238, 101.277)),
                   Q((393.364, 95.964), (400.683, 97.428)),
                   C((415.842, 100.460), (425.291, 114.140), (431.000, 126.875)),
                   C((437.547, 141.481), (446.067, 157.860), (444.250, 174.000)),
                   Q((443.479, 180.846), (435.250, 181.500)),
                   Q((415.374, 183.842), (400.344, 183.842)),
                   C((385.671, 183.842), (357.758, 177.758), (331.634, 179.189)),
                   C((320.189, 179.816), (302.647, 186.347), (296.742, 186.347)),
                   Q((301.154, 182.519), (301.701, 179.606)),
                   Q((302.722, 174.156), (299.230, 163.775)))
    elif name is RegionName.RIGHT_CRUS_II:
        shape = PS(M((296.960, 186.473)),
                   C((302.647, 186.347), (320.189, 179.816), (331.634, 179.189)),
                   C((357.758, 177.758), (385.671, 183.842), (400.344, 183.842)),
                   Q((415.374, 183.842), (435.250, 181.500)),
                   Q((441.827, 184.889), (442.750, 187.000)),
                   C((446.250, 195.000), (448.564, 211.972), (447.250, 221.500)),
                   Q((445.250, 236.000), (430.250, 236.500)),
                   C((411.000, 234.667), (396.530, 221.110), (377.000, 217.333)),
                   C((359.903, 214.027), (335.000, 216.000), (327.667, 215.333)),
                   Q((302.655, 213.060), (298.095, 210.306)))
    elif name is RegionName.RIGHT_VIIB:
        shape = PS(M((298.095, 210.306)),
                   Q((302.655, 213.060), (327.667, 215.333)),
                   C((335.000, 216.000), (359.903, 214.027), (377.000, 217.333)),
                   C((396.530, 221.110), (411.000, 234.667), (429.667, 237.333)),
                   C((438.162, 237.161), (443.593, 237.177), (446.515, 236.516)),
                   C((450.218, 235.679), (451.913, 240.005), (452.336, 245.035)),
                   C((452.610, 248.300), (452.348, 251.862), (451.750, 254.500)),
                   C((450.830, 258.557), (447.975, 262.993), (443.750, 265.500)),
                   Q((439.833, 267.824), (431.250, 267.500)),
                   L((425.331, 266.551)),
                   Q((404.333, 253.333), (375.000, 242.667)),
                   C((358.161, 236.543), (345.424, 234.789), (329.000, 232.667)),
                   Q((308.746, 230.050), (298.662, 230.735)),
                   Q((301.302, 226.059), (301.701, 223.206)),
                   Q((302.370, 218.411), (298.095, 210.306)))
    elif name is RegionName.RIGHT_VIIIA:
        shape = PS(M((298.662, 230.735)),
                   Q((308.746, 230.050), (329.000, 232.667)),
                   C((345.424, 234.789), (358.161, 236.543), (375.000, 242.667)),
                   Q((404.333, 253.333), (424.333, 267.333)),
                   Q((425.741, 274.893), (422.774, 278.823)),
                   Q((420.122, 282.335), (407.945, 287.005)),
                   Q((401.927, 284.722), (399.667, 282.667)),
                   C((392.333, 276.000), (379.175, 259.450), (373.000, 255.333)),
                   C((360.885, 247.257), (348.065, 245.185), (333.667, 243.333)),
                   Q((322.717, 241.925), (298.662, 243.786)),
                   Q((300.564, 240.080), (300.679, 237.852)),
                   Q((300.815, 235.209), (298.662, 230.735)))
    elif name is RegionName.RIGHT_VIIIB:
        shape = PS(M((298.662, 243.786)),
                   Q((322.717, 241.925), (333.667, 243.333)),
                   C((348.065, 245.185), (360.885, 247.257), (373.000, 255.333)),
                   C((379.175, 259.450), (392.333, 276.000), (399.667, 282.667)),
                   Q((401.927, 284.722), (407.000, 287.333)),
                   Q((408.802, 292.724), (407.945, 295.697)),
                   C((406.962, 299.108), (405.231, 301.825), (402.320, 303.879)),
                   Q((398.626, 306.486), (390.048, 305.924)),
                   Q((382.742, 300.066), (377.409, 286.066)),
                   C((373.133, 274.843), (368.354, 269.836), (358.354, 263.836)),
                   C((348.984, 258.214), (346.710, 255.367), (327.126, 255.367)),
                   C((320.046, 255.367), (313.698, 257.933), (302.634, 257.973)),
                   Q((303.638, 253.404), (303.105, 250.959)),
                   Q((302.461, 248.006), (298.662, 243.786)))
    elif name is RegionName.RIGHT_IX:
        shape = PS(M((302.634, 257.973)),
                   C((313.698, 257.933), (320.046, 255.367), (327.126, 255.367)),
                   C((346.710, 255.367), (348.984, 258.214), (358.354, 263.836)),
                   C((368.354, 269.836), (373.133, 274.843), (377.409, 286.066)),
                   Q((382.742, 300.066), (390.333, 306.667)),
                   Q((387.321, 309.803), (385.446, 311.549)),
                   C((381.696, 315.042), (375.127, 315.528), (372.663, 318.196)),
                   Q((368.086, 323.153), (366.016, 333.025)),
                   Q((358.333, 334.000), (347.000, 329.333)),
                   C((329.877, 322.283), (328.333, 306.667), (317.667, 298.000)),
                   C((310.570, 292.234), (303.394, 288.949), (299.230, 286.913)),
                   Q((301.774, 281.783), (302.630, 278.808)),
                   Q((304.682, 271.680), (302.634, 257.973)))
    elif name is RegionName.RIGHT_X:
        shape = PS(M((299.230, 286.913)),
                   C((303.394, 288.949), (310.570, 292.234), (317.667, 298.000)),
                   C((328.333, 306.667), (329.877, 322.283), (347.000, 329.333)),
                   Q((358.333, 334.000), (365.367, 333.327)),
                   Q((376.338, 329.313), (381.356, 332.002)),
                   C((387.424, 335.255), (390.303, 342.054), (388.473, 348.686)),
                   C((386.439, 356.059), (377.397, 359.103), (371.640, 359.103)),
                   C((357.629, 359.103), (350.949, 355.770), (345.228, 351.578)),
                   C((340.928, 348.427), (337.169, 344.790), (331.245, 341.718)),
                   C((322.759, 337.318), (314.271, 335.559), (304.655, 336.093)),
                   C((290.849, 336.860), (289.315, 343.507), (287.880, 342.523)),
                   C((293.406, 337.904), (296.030, 327.828), (297.170, 322.885)),
                   C((299.198, 314.095), (299.699, 302.623), (299.230, 286.913)))
    elif name is RegionName.VERMIS_VI:
        shape = PS(M((270.312, 140.500)),
                   Q((289.500, 140.500), (300.365, 140.509)),
                   Q((302.648, 149.473), (302.041, 154.400)),
                   Q((301.619, 157.830), (299.230, 163.775)),
                   Q((288.569, 165.333), (270.312, 165.333)),
                   Q((252.055, 165.333), (241.394, 163.775)),
                   Q((239.005, 157.830), (238.583, 154.400)),
                   Q((237.976, 149.473), (240.259, 140.509)),
                   Q((251.124, 140.500), (270.312, 140.500)))
    elif name is RegionName.VERMIS_VII:
        shape = PS(M((270.312, 165.333)),
                   Q((288.569, 165.333), (299.230, 163.775)),
                   Q((302.722, 174.156), (301.701, 179.606)),
                   Q((301.154, 182.519), (296.960, 186.473)),
                   Q((301.701, 196.637), (301.019, 202.768)),
                   Q((300.704, 205.610), (298.095, 210.306)),
                   Q((302.370, 218.411), (301.701, 223.206)),
                   Q((301.302, 226.059), (298.662, 230.735)),
                   L((241.962, 231.333)),
                   Q((239.322, 226.059), (238.923, 223.206)),
                   Q((238.254, 218.411), (242.529, 210.306)),
                   Q((239.920, 205.610), (239.605, 202.768)),
                   Q((238.923, 196.637), (243.664, 186.473)),
                   Q((239.470, 182.519), (238.923, 179.606)),
                   Q((237.902, 174.156), (241.394, 163.775)),
                   Q((252.055, 165.333), (270.312, 165.333)))
    elif name is RegionName.VERMIS_VIII:
        shape = PS(M((270.312, 231.333)),
                   L((298.662, 230.735)),
                   Q((300.815, 235.209), (300.679, 237.852)),
                   Q((300.564, 240.080), (298.662, 243.786)),
                   Q((302.461, 248.006), (303.105, 250.959)),
                   Q((303.638, 253.404), (302.634, 257.973)),
                   Q((293.726, 259.923), (270.312, 258.667)),
                   Q((246.898, 259.923), (237.990, 257.973)),
                   Q((236.986, 253.404), (237.519, 250.959)),
                   Q((238.163, 248.006), (241.962, 243.786)),
                   Q((240.060, 240.080), (239.945, 237.852)),
                   Q((239.809, 235.209), (241.962, 230.735)))
    elif name is RegionName.VERMIS_IX:
        shape = PS(M((270.312, 258.667)),
                   Q((293.726, 259.923), (302.634, 257.973)),
                   Q((304.682, 271.680), (302.630, 278.808)),
                   Q((301.774, 281.783), (299.230, 286.913)),
                   Q((285.519, 281.250), (270.312, 283.155)),
                   Q((255.105, 281.250), (241.394, 286.913)),
                   Q((238.850, 281.783), (237.994, 278.808)),
                   Q((235.942, 271.680), (237.990, 257.973)),
                   Q((246.898, 259.923), (270.312, 258.667)))
    elif name is RegionName.VERMIS_X:
        shape = PS(M((270.312, 283.155)),
                   C((280.450, 281.885), (290.089, 283.138), (299.230, 286.913)),
                   C((299.699, 302.623), (299.198, 314.095), (297.170, 322.885)),
                   C((296.030, 327.828), (293.406, 337.904), (287.880, 342.523)),
                   C((283.269, 346.377), (274.064, 346.759), (270.312, 346.575)),
                   C((266.560, 346.759), (257.355, 346.377), (252.744, 342.523)),
                   C((247.218, 337.904), (244.594, 327.828), (243.454, 322.885)),
                   C((241.426, 314.095), (240.925, 302.623), (241.394, 286.913)),
                   C((250.535, 283.138), (260.174, 281.885), (270.312, 283.155)))
    elif 'Left' in name.value:
        right_region = name.value.replace('Left', 'Right')
        shape = create_region(right_region).flip(axis)
    return shape


def create_annot_region(name, value=None, colors=DiscreteColors(),
                        show_annot=False, show_value_txt=False):
    """Creates an annotated cerebellar region.

    Args:
        shape (Shape): The shape to annotate.
        value (float): The coloring value. If None, use the label name.
        colors (cerebellum_value_map.colors.Colors): Converts the value into a
            color.
        annot_txt (str): The annotation text, such as the name of this shape.
        annot_pos (str): The annotation position.
        show_annot (bool): If True, show the annotation of the shape.
        show_value_txt (bool): If True, show a text of the coloring value.

    Returns:
        cerebellum_value_map.shape.AnnotatedShape:
        The annotated cerebellar region.

    """
    name = RegionName(name).value
    shape = create_region(name)
    value = name if value is None else value
    annot_txt = ''
    annot_pos = ''
    if 'Right' in name:
        annot_txt = name.replace('Right ', '')
        annot_pos = 'right'
    elif RegionName(name) is RegionName.CORPUS_MEDULLARE:
        annot_txt = name
        annot_pos = 'bottom'
    return AnnotatedShape(shape, value, colors=colors,
                          annot_txt=annot_txt, annot_pos=annot_pos,
                          show_annot=show_annot, show_value_txt=show_value_txt)


class CerebellumValueMap:
    """Saves an SVG illustration of cerebellar sub-regions with colors.

    The input argument :attr:`data` is a :class:`pandas.DataFrame` table loaded
    from a CSV file. The CSV file should have the following format:

    .. code-block:: text
        
        name,value
        region_name_1,value1
        region_name_2,value2
        region_name_3,value3

    Use the following commands to load it into a :class:`pandas.DataFrame`.

    >>> import pandas as pd
    >>> data = pd.read_csv(csv_filename, index_col=0)

    The values contained in :attr:`data` are converted into colors found in a
    colormap that is specified by :attr:`colors`.

    Args:
        data (pandas.DataFrame): The data to show in the illustration.
        output_filename (str): The filename of the output SVG image.
        font_size (int): The size of annotation font.
        font_family (str): The font family of the annotation.
        show_annot (bool): If True, show the annotations of cerebellar regions.
        show_value_txt (bool): If True, show the values as text on top of each
            region.
        colors (cerebellum_value_map.colors.ContinousColorsColors,\
            cerebellum_value_map.colors.DiscreteColors): Converts a value into
            the corresponding color in a colormap.
        stroke (str): The color of the stroke.
        stroke_width (int): The width of the stroke.
        size (tuple[int]): The size (width, height) of the illustration.
        create (function): The function to create a region.

    """
    def __init__(self, data, output_filename, show_annot=False,
                 show_value_txt=False, colors=DiscreteColors(),
                 font_size=12, font_family='Helvetica',
                 stroke='black', stroke_width=2, size=(550, 450),
                 create=create_annot_region):
        assert isinstance(colors, DiscreteColors) \
            or isinstance(colors, ContinousColors)
        self.data = data
        self.output_filename = output_filename
        self.show_annot = show_annot
        self.show_value_txt = show_value_txt
        self.colors = colors
        self.font_size = font_size
        self.font_family = font_family
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.size = size
        self.create = create_annot_region
        self._regions = [create(name, value[0], colors=self.colors,
                                show_annot=self.show_annot,
                                show_value_txt=self.show_value_txt)
                         for name, value in self.data.iterrows()]

    def translate(self, x, y):
        """Translate the illustration by an offset (x, y).

        Args:
            x (float): The horizontal translation.
            y (float): The vertical translation.

        """
        self._regions = [r.translate(x, y) for r in self._regions]

    def scale(self, f):
        """Scales the illustration.

        Args:
            f (float): The scale factor.

        """
        self._regions = [r.scale(f) for r in self._regions]

    @property
    def left(self):
        """Returns the left-most horizontal coordinate."""
        return min(region.left for region in self._regions)

    @property
    def right(self):
        """Returns the right-most horizontal coordinate."""
        return max(region.right for region in self._regions)

    @property
    def up(self):
        """Returns the up-most vertical coordinate."""
        return min(region.up for region in self._regions)

    @property
    def bottom(self):
        """Returns the down-most vertical coordinate."""
        return max(region.bottom for region in self._regions)

    def save(self):
        """Saves the illustration into :attr:`output_filename`."""
        drawing = Drawing(self.output_filename,
                          size=self.size,
                          stroke=self.stroke,
                          stroke_width=self.stroke_width,
                          font_size=self.font_size,
                          font_family=self.font_family)
        for region in self._regions:
            drawing.add(region.get_svg())
        drawing.save(pretty=True)


class CerebellumLabelMap(CerebellumValueMap):
    """Saves an SVG illustration of cerebellar region definitions.

    Args:
        region_names (iterable[str]): The names of the regions to show.
        output_filename (str): The filename of the output SVG image.
        font_size (int): The size of annotation font.
        font_family (str): The font family of the annotation.
        show_annot (bool): If True, show the annotations of cerebellar regions.
        show_value_txt (bool): If True, show the values as text on top of each
            region.
        colors (cerebellum_value_map.colors.CerebellumLabelColors): Returns the
            color of each cerebellar region.
        stroke (str): The color of the stroke.
        stroke_width (int): The width of the stroke.
        size (tuple[int]): The size (width, height) of the illustration.
        create (function): The function to create a region.

    """
    def __init__(self, region_names, output_filename, show_annot=False,
                 colors=CerebellumLabelColors(),
                 font_size=12, font_family='Helvetica',
                 stroke='black', stroke_width=2, size=(550, 450),
                 create=create_annot_region):
        self.region_names = region_names
        self.output_filename = output_filename
        self.show_annot = show_annot
        self.colors = colors
        self.font_size = font_size
        self.font_family = font_family
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.size = size
        self._regions = [create(name, colors=self.colors,
                                show_annot=self.show_annot)
                         for name in self.region_names]
