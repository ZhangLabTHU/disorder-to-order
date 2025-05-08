import matplotlib.pyplot as plt
import numpy as np

# 加载数据
temperature = np.loadtxt('temp_sro_ptco.csv', delimiter=',')[:,0]
sro_ptco = np.loadtxt('temp_sro_ptco.csv', delimiter=',')[:,1]
sro_ptconi = np.loadtxt('temp_sro_ptconi.csv', delimiter=',')[:,1]
sro_ptcocu = np.loadtxt('temp_sro_ptcocu.csv', delimiter=',')[:,1]
sro_ptcozn = np.loadtxt('temp_sro_ptcozn.csv', delimiter=',')[:,1]

# 创建 3 个子图，按 1 行 3 列排列
fig, axs = plt.subplots(1, 4, figsize=(15, 3))  # 设置图表大小
plt.rc('font', family='Arial')  # 设置字体为 Arial

# 设置 y 轴范围为 -0.4 到 0
y_min, y_max = -0.4, 0.10

# 设置统一的刻度线样式：朝内
for ax in axs:
    ax.tick_params(direction='in', labelsize=10, length=6)

# 绘制第零个子图
axs[0].plot(temperature, sro_ptco, marker='o', markersize=3, color='#276BB3')
axs[0].set_xlabel('Temperature (K)',fontsize=12)  # 设置x轴标签
axs[0].set_ylabel(r'$\rm \alpha^{Pt-Co}$',fontsize=12)  # 设置y轴标签
axs[0].set_ylim(y_min, y_max)  # 设置 y 轴范围

# 绘制第一个子图
axs[1].plot(temperature, sro_ptconi, marker='o', markersize=3, color='#276BB3')
axs[1].set_xlabel('Temperature (K)',fontsize=12)  # 设置x轴标签
axs[1].set_ylabel(r'$\rm \alpha^{Pt-CoNi}$',fontsize=12)  # 设置y轴标签
axs[1].set_ylim(y_min, y_max)  # 设置 y 轴范围

# 绘制第二个子图 
axs[2].plot(temperature, sro_ptcocu, marker='o', markersize=3, color='#276BB3')
axs[2].set_xlabel('Temperature (K)',fontsize=12)  # 设置x轴标签
axs[2].set_ylabel(r'$\rm \alpha^{Pt-CoCu}$',fontsize=12)  # 设置y轴标签
axs[2].set_ylim(y_min, y_max)


# 绘制第三个子图 
axs[3].plot(temperature, sro_ptcozn, marker='o', markersize=3, color='#276BB3')
axs[3].set_xlabel('Temperature (K)',fontsize=12)  # 设置x轴标签
axs[3].set_ylabel(r'$\rm \alpha^{Pt-CoZn}$',fontsize=12)  # 设置y轴标签
axs[3].set_ylim(y_min, y_max)


# 调整子图之间的间隙为 0.3
plt.subplots_adjust(wspace=0.3)  # 设置子图之间的垂直间隙为 0
plt.savefig('temperature_sro_conicuzn.eps',bbox_inches='tight')
# 显示图形
plt.show()

