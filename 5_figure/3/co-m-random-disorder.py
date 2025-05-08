from matplotlib.colors import Normalize, to_hex
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap

Metal_indices =  ['Ti',  'V',  'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
                         'Nb', 'Mo',       'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
                  'Ta',  'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg']
Energy = [-0.0951,-0.0355,-0.0027,0.0044,0.0027,0,0.0048,0.0127,0.0078,
          -0.0862,-0.0114,-0.0022,0.0060,0.0275,0.0652,0.0495,
          -0.1119,-0.0314,-0.0122,-0.0185,-0.0067,0.0120,0.0484,0.0572,
          ]                 
Metal_potential_dict = {}
Metal_color_dict = {}
Energy = [i for i in Energy]
print(min(Energy), max(Energy))

# 根据列表的数值生成从蓝到红的颜色映射
colors = [(0, '#30409a'), (0.63, 'white'), (1, '#67000d')]
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
fig.write_image('co_m_disorder.pdf')
fig.show()