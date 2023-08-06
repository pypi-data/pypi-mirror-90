
# uav_fdm 无人机动力学模型

## 概述

本项目将matlab代码生成的三自由度飞行动力学模型C++类通过SWIG进行包装，并通过pip发布。

## 编译安装

### 本地编译

```bash
python setup.py build_ext --inplace
```

### 安装编译

```bash
python setup.py install --user
```

### pip安装

```bash
pip install uav-fdm
```

## 接口说明

模块名称为```uav_fdm```;
其中的类名称为```uav_fdm```。

### 初始化

类的初始化函数为```uav_fdm.uav_fdm(x0, y0, alt0, gs0, gamma0, psi0, phi0)```

| 参数 | 说明 | 单位 |
|--- | --- | --- |
| x0 | 初始x | m|
| y0 | 初始y|m
| alt0 | 初始高度|m
| gs0 | 初始地速|m/s
| gamma0 | 初始航迹倾角|rad
| psi0 | 初始真航向|rad
| phi0 | 初始滚转角|rad

### 仿真步进

类的仿真步进函数为``` [t, x, y, alt, v_n, v_e, hdot, phi, psi_t, gamma, gs, tas] = uav1.update(dt, tas_c, hdot_c, psi_c, w_n, w_e) ```

| 输入参数 | 说明 | 单位 |
|--- | --- | --- |
| dt  | 步进时间（为0.05s整倍数）|s
| tas_c  | 真空速指令|m/s
| hdot_c | 升降速率指令|m/s
| psi_c  | 航向角指令|rad
| w_n    | 北风速度|m/s
| w_e    | 东风速度|m/s

| 输出变量 | 说明 | 单位 |
|--- | --- | --- |
| t | 时间 | s
| x | x | m
| y | y | m
|alt | 高度 | m
|v_n | 北向速度 | m/s
|v_e | 东向速度 | m/s
|hdot | 天向速度 | m/s
|phi | 滚转角 | rad
|psi_t | 真航向角(-pi~pi) | rad
|gamma | 航迹倾角 | rad
|gs | 地速 | m/s
| tas | 真空速 | m/s

### 指令限制

* 飞行真空速指令限制```14~24m/s```
* 升级速率指令限制```-3~3m/s```
* 偏航角指令限制```-pi~pi rad```

## 使用示例

```python
import uav_fdm

if __name__ == '__main__':
    x0 = 23  # 初始x（m）
    y0 = 110  # 初始y（m）
    alt0 = 130  # 初始高度（m）
    gs0 = 22  # 初始地速（m/s）
    gamma0 = 0  # 初始航迹倾角（rad）
    psi0 = 3.14  # 初始真航向（rad）
    phi0 = 0  # 初始滚转角（rad）

    # 初始化uav1
    uav1 = uav_fdm.uav_fdm(x0, y0, alt0, gs0, gamma0, psi0, phi0)

    # 进行5秒平飞仿真
    tas_c = 22  # 真空速指令(m/s)
    hdot_c = 0  # 升降速率指令(m/s)
    psi_c = 3.14  # 航向角指令(rad)
    w_n = 0  # 北风速度(m/s)
    w_e = 0  # 东风速度(m/s)
    t = 0
    dt = 1  # 按1秒推进
    while t < 5:
        [t, x, y, alt, v_n, v_e, hdot, phi, psi_t, gamma, gs, tas] = uav1.update(
            dt, tas_c, hdot_c, psi_c, w_n, w_e)
        print(f'{t:.0f} {x:.0f} {y:.0f} {alt:.2f} {gs:.2f} {psi_t*57.3:.2f} {phi*57.3:.2f}')

    # 进行15秒转弯仿真
    tas_c = 22  # 真空速指令(m/s)
    hdot_c = 0  # 升降速率指令(m/s)
    psi_c = 1.57082  # 航向角指令(rad)
    w_n = 0  # 北风速度(m/s)
    w_e = 0  # 东风速度(m/s)
    t = 0
    dt = 1  # 按1秒推进
    while t < 20:
        [t, x, y, alt, v_n, v_e, hdot, phi, psi_t, gamma, gs, tas] = uav1.update(
            dt, tas_c, hdot_c, psi_c, w_n, w_e)
        print(f'{t:.0f} {x:.0f} {y:.0f} {alt:.2f} {gs:.2f} {psi_t*57.3:.2f} {phi*57.3:.2f}')

    # 进行5秒爬升仿真
    tas_c = 22  # 真空速指令(m/s)
    hdot_c = 1  # 升降速率指令(m/s)
    psi_c = 1.57082  # 航向角指令(rad)
    w_n = 0  # 北风速度(m/s)
    w_e = 0  # 东风速度(m/s)
    t = 0
    dt = 1  # 按1秒推进
    while t < 25:
        [t, x, y, alt, v_n, v_e, hdot, phi, psi_t, gamma, gs, tas] = uav1.update(
            dt, tas_c, hdot_c, psi_c, w_n, w_e)
        print(f'{t:.0f} {x:.0f} {y:.0f} {alt:.2f} {gs:.2f} {psi_t*57.3:.2f} {phi*57.3:.2f}')

    # 进行5秒加速仿真
    tas_c = 24  # 真空速指令(m/s)
    hdot_c = 0  # 升降速率指令(m/s)
    psi_c = 1.57082  # 航向角指令(rad)
    w_n = 0  # 北风速度(m/s)
    w_e = 0  # 东风速度(m/s)
    t = 0
    dt = 1  # 按1秒推进
    while t < 30:
        [t, x, y, alt, v_n, v_e, hdot, phi, psi_t, gamma, gs, tas] = uav1.update(
            dt, tas_c, hdot_c, psi_c, w_n, w_e)
        print(f'{t:.0f} {x:.0f} {y:.0f} {alt:.2f} {gs:.2f} {psi_t*57.3:.2f} {phi*57.3:.2f}')

```
