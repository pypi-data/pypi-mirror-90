# feeluown 网易云音乐插件

[![Build Status](https://travis-ci.com/feeluown/feeluown-netease.svg?branch=master)](https://travis-ci.com/feeluown/feeluown-netease)
[![PyPI](https://img.shields.io/pypi/v/fuo_netease.svg)](https://pypi.python.org/pypi/fuo-netease)
[![Coverage Status](https://coveralls.io/repos/github/feeluown/feeluown-netease/badge.svg?branch=master)](https://coveralls.io/github/feeluown/feeluown-netease?branch=master)

## 安装

```sh
pip3 install fuo-netease
```

## changelog

### 0.5 (2021-01-07)
- 适配 fuo library v2，支持相似歌曲、歌曲评论

### 0.4.4 (2020-12-30)
- 修复不能搜索歌单的问题 #11
- 支持展示收藏歌手 #11
- 支持使用国外手机号登录 #14

### 0.4.3 (2020-08-21)
- 用户没有绑定手机号时，进行提醒 [bugfix](https://github.com/feeluown/FeelUOwn/issues/389)

### 0.4.2 (2020-02-08)
- 依赖 feeluown>=3.3.10
- 支持显示我的专辑收藏
- 支持每日推荐

### 0.4.1 (2020-02-08)
- 支持私人 FM，依赖 feeluown>=3.3.9

### 0.4 (2019-11-27)
- 使用 marshmallow >= 3.0
- 启用单测和质量检查，并接入 travis，

### 0.3 (2019-10-28)

- 支持获取歌手专辑
- 支持获取播放列表的所有歌曲

### 0.2 (2019-06-30)

- 适配 fuocore.models.Media 新设计
- 支持多品质音乐

### 0.1 (2019-03-18)

- 支持用户登录、歌曲搜索、歌词/歌曲/mv/歌手/专辑详情获取
