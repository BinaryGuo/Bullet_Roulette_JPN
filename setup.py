import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="bulletroulette",  # 模块名称
    version="1.1.1",  # 当前版本
    author="GQX",  # 作者
    author_email="kill114514251@outlook.com",  # 作者邮箱
    description="模仿steam游戏“恶魔轮盘”，目前没有提供开发接口（只能单纯玩）",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://github.com/BinaryGuo/Bullet_Roulette",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    include_package_data=True,
    package_data={
        "bulletroulette" : ["assets/*.png","assets/*.ogg","assets/*.ttf","assets/*.wav"]
    },
    # 模块相关的元数据
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: pygame",
        "Natural Language :: Chinese (Simplified)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
    ],
    # 依赖模块
    install_requires=[
        "pygame>=2.0.1",
    ],
    python_requires=">=3.8",
)