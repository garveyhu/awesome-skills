# 国内镜像源配置（单一来源）

本文件是本 skill 所有 Dockerfile 镜像源配置的**唯一来源（SSOT）**。

**铁律**：任何模板 / 生成的 Dockerfile 里出现包管理器镜像配置，都**照抄本文件的标准片段**，不要各写各的。改镜像源只改这里，再同步到模板——避免「apt 用阿里云、yarn 用 npmmirror、uv 忘了配」这种各处不一致、还漏配的局面。

## 启用策略

- **默认启用**：本 skill 默认面向**国内网络构建**，下列镜像片段默认写进 Dockerfile。
- **海外 / CI 海外构建**：直接删掉对应镜像行即可（官方源在海外更快、更稳）。
- 需要一份 Dockerfile 两种网络通吃时，用文末的 **ARG 开关方案**。

> Dockerfile 不支持 include 外部片段，「集中维护」靠的是「本文件是权威、模板照抄」这个约定，不是机制强制。所以新增 / 修改镜像配置时，**先改这里再改模板**。

---

## 系统包

### Debian（deb822 格式，`python:*-slim` / `node:*-slim` / `debian:12+` 默认）

```dockerfile
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends <pkgs> && \
    rm -rf /var/lib/apt/lists/*
```

### Debian / Ubuntu（老 `sources.list` 格式，`ubuntu:*` / `debian:11`）

```dockerfile
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.aliyun.com@g; s/security.ubuntu.com/mirrors.aliyun.com/g; s/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends <pkgs> && \
    rm -rf /var/lib/apt/lists/*
```

### Alpine（apk）

```dockerfile
RUN sed -i 's#dl-cdn.alpinelinux.org#mirrors.aliyun.com#g' /etc/apk/repositories && \
    apk add --no-cache <pkgs>
```

---

## Node（npm / yarn / pnpm）

镜像统一用 `https://registry.npmmirror.com`。

```dockerfile
# yarn 1.x（classic）
RUN yarn config set registry https://registry.npmmirror.com

# npm
RUN npm config set registry https://registry.npmmirror.com

# pnpm
RUN pnpm config set registry https://registry.npmmirror.com
```

> yarn 2+（berry）走仓库内 `.yarnrc.yml` 的 `npmRegistryServer: "https://registry.npmmirror.com"`，不在 Dockerfile 配。

配合 build cache mount（强烈推荐）：

```dockerfile
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn \
    yarn config set registry https://registry.npmmirror.com && \
    yarn install --frozen-lockfile --network-timeout 1000000
```

---

## Python（uv / pip）

> **常见漏配**：`uv sync` 默认走官方 PyPI，国内会很慢。装 uv 的镜像**必须**补 `UV_DEFAULT_INDEX`。

### uv

> **装 uv 用 pip 从阿里云装，别用 `COPY --from=ghcr.io/astral-sh/uv`**——ghcr.io 在国内
> 经常不可达，尤其多架构 buildx push 拉各架构元数据时报
> `failed to fetch anonymous token ... ghcr.io/token ... EOF`。单架构本地 build 可能因缓存
> 侥幸通过，多架构必拉 ghcr → 挂。见 [pitfalls.md](pitfalls.md)。

```dockerfile
ENV UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple/
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev
```

> pip 装的 uv 在 `/usr/local/bin/uv`（不是 ghcr 的 `/uv`）。多阶段时 runtime 从 builder 拷：
> `COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv`。`uv sync` 仍走官方 PyPI 国内慢，
> 所以 `UV_DEFAULT_INDEX` 必配。

### pip

```dockerfile
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
    PIP_TRUSTED_HOST=mirrors.aliyun.com
RUN pip install --no-cache-dir -r requirements.txt
```

> 备选镜像：清华 `https://pypi.tuna.tsinghua.edu.cn/simple`、腾讯 `https://mirrors.cloud.tencent.com/pypi/simple`。单项目统一一个。

---

## Java（Maven）

Dockerfile 内用 `-s` 指定带阿里云 mirror 的 settings：

```dockerfile
COPY docker/images/settings-cn.xml /root/.m2/settings.xml
RUN mvn -B -s /root/.m2/settings.xml clean package -DskipTests
```

`settings-cn.xml` 的 mirror 段：

```xml
<settings>
  <mirrors>
    <mirror>
      <id>aliyun</id>
      <name>aliyun maven</name>
      <url>https://maven.aliyun.com/repository/public</url>
      <mirrorOf>*</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

> 内网 Nexus 场景另配（见各项目自己的 settings），不要把内网仓库地址硬编码进通用模板。

---

## Go

```dockerfile
ENV GOPROXY=https://goproxy.cn,direct
RUN go mod download && go build -o /app/server .
```

---

## 可选：Docker 拉基础镜像加速

这是 **Docker daemon 层**的配置（`/etc/docker/daemon.json` 的 `registry-mirrors`），**不写进 Dockerfile**，由构建机一次性配置：

```json
{ "registry-mirrors": ["https://docker.m.daobum.com", "https://dockerproxy.com"] }
```

> 公开镜像加速站时有时无，按构建机实际可用的填；内网有 harbor 代理优先走 harbor。

---

## ARG 开关方案（一份 Dockerfile 通吃国内 / 海外）

需要同一 Dockerfile 两种网络都能构建时，用 `ARG` 控制，默认开国内镜像：

```dockerfile
ARG USE_CN_MIRROR=1

RUN if [ "$USE_CN_MIRROR" = "1" ]; then \
      sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources; \
    fi && \
    apt-get update && apt-get install -y --no-install-recommends <pkgs> && \
    rm -rf /var/lib/apt/lists/*

# uv / pip 同理：ENV 用 ARG 兜
ARG UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple/
ENV UV_DEFAULT_INDEX=${UV_DEFAULT_INDEX}
```

海外构建：`docker build --build-arg USE_CN_MIRROR=0 --build-arg UV_DEFAULT_INDEX=https://pypi.org/simple ...`

> 多数项目（构建机固定在国内）用不到开关，默认内联即可。开关只在「同一镜像既要国内打也要海外打」时才值得引入。
