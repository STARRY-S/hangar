# Sync

`sync` 命令将额外的容器镜像保存在未压缩的 [Save](./save.md) 缓存文件夹中。

## QuickStart

当执行 Save 时，有概率会出现部分镜像 Save 失败的情况，失败的镜像会保存在 `save-failed.txt` 中，若重新执行 Save 命令需要重新下载所有镜像并重新创建压缩包，因此可使用 Sync 命令只将部分镜像保存在未压缩的缓存文件夹中，并结合 [Compress](./compress.md) 命令创建压缩包供 [Load](./load.md) 命令使用。

----

使用 Sync 命令，将 `saved-failed.txt` 中的镜像保存在 `saved-images-cache` 缓存目录中：

```sh
hangar sync -f ./saved-failed.txt -d ./saved-images-cache -j 10
```

> Sync 失败的镜像会保存在 `sync-failed.txt`。

## Parameters

命令行参数：

```sh
# 使用 -f, --file 参数指定镜像列表文件
# 使用 -d, --destination 参数，指定同步镜像到目标文件夹目录
hangar sync -f ./list.txt -d [DIRECTORY]

# 使用 -s, --source 参数，可在不修改镜像列表的情况下，指定源镜像的 registry
# 如果镜像列表中的源镜像没有写 registry，且未设定 -s 参数，那么源镜像的 registry 会被设定为默认的 docker.io
hangar sync -f ./list.txt -s custom.registry.io -d [DIRECTORY]

# 使用 -a, --arch 参数，指定导出的镜像的架构（以逗号分隔）
# 默认为 amd64,arm64
hangar sync -f ./list.txt -d [DIRECTORY] -a amd64,arm64

# 使用 -j, --jobs 参数，指定 Worker 数量，并发下载镜像至本地（支持 1~20 个 jobs）
hangar sync -f ./list.txt -d [DIRECTORY] -j 10 # 启动 10 个 Worker

# 使用 --debug 参数，输出更详细的调试日志
hangar sync -f ./list.txt -d [DIRECTORY] --debug
```

## Others

在使用 Sync 将镜像补充至缓存文件夹后，可使用 [compress](./compress.md) 命令压缩缓存文件夹，生成压缩包。