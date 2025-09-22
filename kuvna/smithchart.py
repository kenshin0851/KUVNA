# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 17:13:28 2025

@author: kimke
"""

import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

# 예시: 주파수 벡터 생성 (1GHz ~ 10GHz)
freq = rf.Frequency(1, 10, 201, unit='ghz')

# 임피던스를 반사계수로 변환
Z0 = 50  # 기준 임피던스
Z_load = 75 + 25j  # 예시 부하 임피던스
gamma = (Z_load - Z0) / (Z_load + Z0)  # 반사계수 계산

# 스미스 차트에 표시
rf.plotting.plot_smith(s=gamma, chart_type='z')
plt.show()

'''import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

# 예시: 주파수 범위 (1GHz ~ 10GHz)
freq = rf.Frequency(1, 10, 201, unit='ghz')

# 기준 임피던스
Z0 = 50  

# 임의의 주파수별 부하 임피던스 (75 + j*25*sin())
f = freq.f
Z_load = 75 + 25j*np.sin(2*np.pi*f/10e9)

# 반사계수 계산
gamma = (Z_load - Z0) / (Z_load + Z0)

# 스미스 차트 그리기
rf.plotting.plot_smith(gamma, chart_type='z')
plt.title("Smith Chart Example (ZL = 75 + j25*sin(f))")
plt.show()'''