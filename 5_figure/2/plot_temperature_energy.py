import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt

# 数据
Temperature = [800, 900, 1000, 1100]
Energy = [0.0538, 0.0542, 0.0647, 0.0652]

# 设置字体
plt.rc('font', family='Arial')

# 创建图像和调整大小
plt.figure(figsize=(4, 3))

# 散点图
plt.scatter(Temperature, Energy, s=100, facecolor='#FF7F50')

# 坐标轴设置
plt.xlabel('Critical temperature (K)', fontsize=16)
plt.ylabel(r'$\rm E_{ordering} (eV/atom)$', fontsize=16)
plt.ylim([0.05,0.07])
plt.xlim([750,1150])

# 设置刻度线和标签
plt.tick_params(axis='both', direction='in', length=6, labelsize=14)


# 显示图像
plt.tight_layout()
plt.savefig('temperature_energy.eps',bbox_inches='tight')
plt.show()
