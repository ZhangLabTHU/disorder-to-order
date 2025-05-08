from matplotlib.colors import Normalize, to_hex
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap

Metal_indices =  ['Ti',  'V',  'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
                         'Nb', 'Mo',       'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
                  'Ta',  'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg']
Energy = [0.1687, 0.0991, 0.0342, 0.0240, 0.0365, 0.0641, 0.0737, 0.0828, 0.0983,
                  0.1541, 0.0521,        -0.0089, 0.0283, 0.0637, 0.1047, 0.1176,
                  0.1709, 0.0533,-0.0229,-0.0392,-0.0091, 0.0268, 0.0741, 0.0940,         
          ]                 
Metal_potential_dict = {}
Metal_color_dict = {}
Energy = [i - 0.0641 for i in Energy]
print(min(Energy), max(Energy))

# 根据列表的数值生成从蓝到红的颜色映射
colors = [(0, '#30409a'), (0.49, 'white'), (1, '#67000d')]
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
fig.write_image('ptm_ml.pdf')
fig.show()