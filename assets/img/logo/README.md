# 机构 logo

五所机构的 logo 均已就位，来源为各校官网原始资源（由本人提供）：

| 文件 | 机构 | 官网原图 |
|---|---|---|
| `nus.png` | 新加坡国立大学 | nus.edu.sg/images/default-source/base/logo.png |
| `ntu.png` | 南洋理工大学 | ntu.edu.sg/ResourcePackages/NTU/assets/images/NTU_Logo.png |
| `cuhk-sz.png` | 香港中文大学（深圳） | cuhk.edu.cn/.../zh-hans_logo.png |
| `nudt.png` | 国防科技大学 | nudt.edu.cn/images/logo.png |
| `dmu.png` | 大连海事大学 | dlmu.edu.cn/2024xz/images/logo.png |

## 处理说明

原图均为**横版**（校徽 + 校名文字），因此展示时保持横版、按原比例左对齐，
统一限制高度 44px、宽度 160px 以内——这样校名文字仍然清晰可读。
若压成 46×46 的方形图标，文字会糊成一团。

**NUDT 与 DMU 的原图是为深色页头设计的纯白 logo**（白底上完全不可见），
已做反相处理转为深色。其余三所本身是深色系，保持原色未改动。

## 替换或新增

把图片放进本目录，在 `_data/experience.yml` 对应条目填文件名：

```yaml
logo: "nus.png"     # 留空则显示 abbr 文字占位
abbr: "NUS"
```

新增机构若拿到的是纯白 logo，记得先反相，否则白底上看不见。
