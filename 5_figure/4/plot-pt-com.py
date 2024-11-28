# -*- coding: UTF-8 -*-
#from camkit.sampling.sitesfinder import SitesFinder
from ase.io import read
import ase.db
import numpy as np

Metal_indices =  ['Sc', 'Ti',  'V',  'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
                  'Y',  'Zr',  'Nb', 'Mo',       'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
                        'Hf',  'Ta',  'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg']

Metal_color_dict = {}
Energy = [0.2223, 0.2133, 0.1672, 0.1547, 0.0338, 0.0577, 0.0985, 0.0842, 0.1021, 0.1792,
          0.1287, 0.1503, 0.1705, 0.137,  0.0155, 0.006,	0.0431,	0.0856,	0.1847,
          0.1559, 0.1175, 0.2606, 0.0928, 0.0223,-0.039, 0.0111, -0.0053, 0.085,
]

Energy = [i-0.0985 for i in Energy]

from matplotlib.colors import Normalize, to_hex
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap

# 生成一些示例数据
print(min(Energy), max(Energy))
# 根据列表的数值生成从蓝到红的颜色映射
# 定义颜色映射的颜色
# colors = [(0, '#67000d'), (0, 'white'), (1, '#30409a')]
colors = [(0, '#30409a'), (0.4589, 'white'), (1, '#67000d')]
# colors = [(0, 'white'), (1, '#67000d')]
# 创建颜色映射
cmap = LinearSegmentedColormap.from_list('custom_cmap', colors)

norm = Normalize(vmin=min(Energy), vmax=max(Energy))
sm = ScalarMappable(cmap=cmap, norm=norm)
colors = sm.to_rgba(Energy)
hex_colors = [to_hex(color) for color in colors]

for i in range(len(hex_colors)):
    Metal_color_dict[Metal_indices[i]] = hex_colors[i]

from mendeleev.vis import create_vis_dataframe, periodic_table_plotly
elements = create_vis_dataframe()
periodic_table_plotly(elements)
Symbol = list(elements['symbol'])
elements_miscable = []
for ele in Symbol:
    if ele in Metal_indices:
        elements_miscable.append(Metal_color_dict[ele])
    else:
        elements_miscable.append('#ffffff')

elements['block_color'] = elements_miscable
fig = periodic_table_plotly(elements, colorby='block_color') 
fig.show()
fig.write_image('ptm_ml.pdf')