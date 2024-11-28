# -*- coding: UTF-8 -*-
#from camkit.sampling.sitesfinder import SitesFinder
from ase.io import read
import ase.db
import numpy as np

Metal_indices =  ['Sc', 'Ti',  'V',  'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
                  'Y',  'Zr',  'Nb', 'Mo',       'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
                        'Hf',  'Ta',  'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg']

Metal_color_dict = {}
Energy = [0.1011,0.1855,0.2105,0.157,-0.0074,-0.0057,0,-0.0121,-0.0202,0.1323,
          0.0221,0.0151,0.0732,-0.0568,-0.0384,0.0177,-0.0464,-0.1085,-0.0358,
          0.1008,0.1277,-0.0696,-0.0143,0.0091,0.0058,-0.0176,-0.0345,-0.189]

from matplotlib.colors import Normalize, to_hex
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap

# 生成一些示例数据
print(min(Energy), max(Energy))
# 根据列表的数值生成从蓝到红的颜色映射
# 定义颜色映射的颜色
colors = [(0, '#30409a'), (0.475, 'white'), (1, '#67000d')]
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
fig.write_image('pt_com.pdf')