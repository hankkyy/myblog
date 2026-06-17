---
title: "Kubernetes ConfigMap 和 Secret：配置管理的正确姿势"
date: 2026-03-05T09:00:00+08:00
categories: ['云原生', '技术']
description: "理解 ConfigMap 和 Secret 的使用场景、注入方式和安全注意事项。"
---

ConfigMap 和 Secret 是 K8s 中管理配置的两大工具。

## ConfigMap

存储非敏感配置——数据库地址、日志级别、环境变量等：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database-url: "jdbc:mysql://db:3306/mydb"
  log-level: "debug"
```

## Secret

存储敏感信息——密码、Token、证书等。值需要 base64 编码：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=      # base64("admin")
  password: cGFzc3dvcmQ=  # base64("password")
```

## 注入方式

### 环境变量

```yaml
env:
- name: DB_URL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: database-url
```

### 挂载为文件

```yaml
volumes:
- name: config-volume
  configMap:
    name: app-config
```

文件挂载的好处：支持热更新（ConfigMap 更新后 Kubelet 会自动同步）。

## Secret 的安全问题

1. Secret 默认只做 base64 编码，不是加密——base64 可以轻松解码
2. 解决方案：启用 Etcd 加密（EncryptionConfiguration）
3. 更安全的方案：使用外部密钥管理（HashiCorp Vault、AWS Secrets Manager）
4. 限制 Secret 的 RBAC 权限

## 最佳实践

- ConfigMap 放非敏感配置，Secret 放密码/Token
- 生产环境密码不要直接写在 Secret yaml 里——用 CI/CD 注入
- ConfigMap 和 Secret 有大小限制（1MB），不要放大量数据
- 善用 immutable 特性（`immutable: true`）提升性能

配置管理看着简单，但在生产环境中做错一步就会导致安全事故。
