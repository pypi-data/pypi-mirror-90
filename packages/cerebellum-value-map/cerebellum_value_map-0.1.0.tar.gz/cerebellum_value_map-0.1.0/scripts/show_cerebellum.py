#!/usr/bin/env python3

import argparse

desc = 'Show values as colors in a cerebellum illustration.'
formatter = argparse.ArgumentDefaultsHelpFormatter
parser = argparse.ArgumentParser(description=desc, formatter_class=formatter)
parser.add_argument('-i', '--input-filename', help='The input filename.')
parser.add_argument('-o', '--output-filename', required=True,
                    help='The output filename.')
parser.add_argument('-p', '--is-pvalue-mode', action='store_true',
                    help='Convert values into significance levels if True.')
parser.add_argument('-l', '--label-map', default=False, action='store_true',
                    help='Show the label map if True. -i is ignored.')
parser.add_argument('-m', '--label-map-mode', default='lobule',
                    choices={'lobule', 'lobe'},
                    help='The mode of the label map.')
parser.add_argument('-c', '--colormap', default='jet',
                    help='The name of a continuous colormap.')
parser.add_argument('-v', '--vmin', default=-2, type=float,
                    help='The value of the left-most color in a continuous '
                         'colormap.')
parser.add_argument('-V', '--vmax', default=2, type=float,
                    help='The value of the right-most color in a continuous '
                         'colormap.')
parser.add_argument('-C', '--colormap-filename', default=None,
                    help='The filename of a discrete colormap.')
parser.add_argument('-M', '--colormap-mode', default='discrete',
                    choices={'discrete', 'continuous'},
                    help='The color map. Use default if None.')
parser.add_argument('-n', '--region-names', default=None, nargs='+',
                    help='The names of regions to show. Use default if None.')
parser.add_argument('-s', '--size', type=int, nargs=2, default=(75, 73),
                    help='The size of the svg image.')
parser.add_argument('-t', '--translate', type=float, nargs=2,
                    default=(-84, -50),
                    help='The translation of the cerebellum in the SVG image. '
                         'The translation is performed before scaling.')
parser.add_argument('-S', '--scale', type=float, default=0.2,
                    help='The scale factor of the cerebellum in the SVG image. '
                         'The translation is performed before scaling.')
parser.add_argument('-f', '--font-size', type=int, default=9,
                    help='The font size in the SVG image.')
parser.add_argument('-w', '--stroke-width', type=int, default=1,
                    help='The stroke width in the SVG image.')
parser.add_argument('-a', '--show-annotation', action='store_true',
                    help='Show the annotation of each region.')
parser.add_argument('-T', '--show-value-text', action='store_true',
                    help='Show the text of the value of each region.')
args = parser.parse_args()


import pandas as pd
import numpy as np
from pathlib import Path

from cerebellum_value_map import CerebellumValueMap, CerebellumLabelMap
from cerebellum_value_map import DiscreteColors, ContinousColors
from cerebellum_value_map import CerebellumLabelColors, convert_pvals
from cerebellum_value_map import default_lobule_names, default_lobe_names

    
Path(args.output_filename).parent.mkdir(exist_ok=True, parents=True)

if args.label_map:
    if args.label_map_mode == 'lobule':
        region_names = default_lobule_names
    elif args.label_map_mode == 'lobe':
        region_names = default_lobe_names
    if args.region_names is None:
        args.region_names = region_names
    colors = CerebellumLabelColors(args.colormap_filename)
    cerebellum = CerebellumLabelMap(args.region_names, args.output_filename,
                                    colors=colors, font_size=args.font_size,
                                    stroke_width=args.stroke_width,
                                    size=args.size)
else:
    if args.colormap_mode == 'discrete':
        colors = DiscreteColors(filename=args.colormap_filename)
    elif args.colormap_mode == 'continuous':
        colors = ContinousColors(vmin=args.vmin, vmax=args.vmax,
                                 cmap=args.colormap)
    data = pd.read_csv(args.input_filename, index_col=0)
    if args.is_pvalue_mode:
        data = convert_pvals(data)
    cerebellum = CerebellumValueMap(data, args.output_filename,
                                    show_annot=args.show_annotation,
                                    show_value_txt=args.show_value_text,
                                    colors=colors, font_size=args.font_size,
                                    stroke_width=args.stroke_width,
                                    size=args.size)
cerebellum.translate(*args.translate)
cerebellum.scale(args.scale)
cerebellum.save()
