---
lang: en
title: "Kubernetes ConfigMap and Secret: The Right Way to Manage Configuration"
date: 2026-03-05T09:00:00+08:00
categories: ['Cloud Native', 'Technology']
description: "Understand the use cases, injection methods, and security considerations of ConfigMap and Secret."
---

ConfigMap and Secret are the two primary tools for managing configuration in K8s.

## ConfigMap

Stores non-sensitive configuration—database addresses, log levels, environment variables, etc.:

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

Stores sensitive information—passwords, tokens, certificates, etc. Values need to be base64 encoded:

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

## Injection Methods

### Environment Variables

```yaml
env:
- name: DB_URL
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: database-url
```

### Mounted as Files

```yaml
volumes:
- name: config-volume
  configMap:
    name: app-config
```

The benefit of file mounting: it supports hot updates (Kubelet automatically syncs when the ConfigMap is updated).

## Secret Security Concerns

1. Secrets are only base64 encoded by default, not encrypted—base64 can be easily decoded
2. Solution: Enable Etcd encryption (EncryptionConfiguration)
3. More secure option: Use external key management (HashiCorp Vault, AWS Secrets Manager)
4. Restrict RBAC permissions for Secrets

## Best Practices

- Put non-sensitive configuration in ConfigMaps, and passwords/tokens in Secrets
- Don't write production passwords directly in Secret YAML files—inject them via CI/CD
- ConfigMaps and Secrets have a size limit (1MB), so don't store large amounts of data
- Make good use of the immutable feature (`immutable: true`) to improve performance

Configuration management may seem simple, but in a production environment, a single misstep can lead to a security incident.