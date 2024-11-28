import numpy as np
import matplotlib.pyplot as plt


import numpy as np
import matplotlib.pyplot as plt

Colors = ['#D85558', '#276BB3']
# 示例数据
fig, ax1 = plt.subplots(figsize=(5, 4))
plt.rc('font', family='Arial')

# 设置刻度线朝内
ax1.xaxis.set_tick_params(direction='in', labelsize=12, which='major', length=6)
ax1.yaxis.set_tick_params(direction='in', labelsize=12, which='major', length=6)

categories = ['From scratch', 'Finetune1', 'Finetune2', 'Finetune3']
values1 = [0.0024, 0.0018, 0.0017, 0.0016]  # energy MAE
values2 = [0.0438, 0.0371, 0.0338, 0.0339]  # force MAE

# 定义每个条形的宽度
bar_width = 0.3

# 计算每个类别的x坐标
x = np.arange(len(categories))

# 创建第一个 y 轴上的条形统计图（能量 MAE）
ax1.bar(x - bar_width/2, values1, width=bar_width, color='#D85558', label='Energy MAE')
ax1.set_ylabel('Energy MAE (eV/Atom)', fontsize=16)
ax1.tick_params(direction='in',labelsize=14,which='major', length=6,)
ax1.set_ylim([0,0.003])

# 创建第二个 y 轴
ax2 = ax1.twinx()
ax2.bar(x + bar_width/2, values2, width=bar_width, color='#276BB3', label='Force MAE')
ax2.set_ylabel('Force MAE (eV/Å)', fontsize=16)
ax2.tick_params(direction='in',labelsize=14,which='major', length=6,)
ax2.set_ylim([0,0.05])

# 设置刻度线方向
plt.tick_params(axis='x', direction='in', labelsize=12)
ax1.tick_params(axis='y', direction='in', labelsize=12)
ax2.tick_params(axis='y', direction='in', labelsize=12)

# 添加 x 轴标签
ax1.set_xticks(x)
ax1.set_xticklabels(categories)
# 使x轴标签倾斜30度
# 使x轴标签倾斜30度
for label in ax1.get_xticklabels():
    label.set_rotation(30)

# 添加水平线
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# 显示图例
fig.legend(frameon=False, fontsize=12, ncol=3, loc='upper center')

# 保存图片
plt.savefig('Bar.eps',dpi=300,bbox_inches='tight')

# 显示图形
plt.show()
