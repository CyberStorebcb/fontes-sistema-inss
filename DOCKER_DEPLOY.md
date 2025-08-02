# Sistema FONTES v3.0 - Deploy com Docker

## 🐳 Containerização para Produção

Esta configuração permite hospedar o Sistema FONTES em qualquer servidor com Docker.

## 📋 Opções de Hospedagem

### 1. 🏠 Servidor Local/Empresa
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Executar sistema
cd docker_deploy/
docker-compose up -d
```

### 2. ☁️ Hospedagem em Nuvem

#### Google Cloud Run
```bash
# Fazer deploy
gcloud run deploy fontes-system \
  --source . \
  --port 5000 \
  --region us-central1
```

#### AWS ECS/Fargate
```bash
# Criar tarefa
aws ecs create-service \
  --cluster fontes-cluster \
  --service-name fontes-service \
  --task-definition fontes-task
```

#### DigitalOcean App Platform
- Conecte repositório GitHub
- Configure porta 5000
- Deploy automático

## 🌐 URLs de Acesso

### Desenvolvimento
- Local: http://localhost:5000
- Rede: http://[SEU_IP]:5000

### Produção
- Próprio domínio: http://fontes.sua-empresa.com.br
- Cloud: https://fontes-system-xyz.run.app

## 👤 Credenciais

**Padrão (alterar em produção):**
- Usuário: admin
- Senha: admin123

## 🔒 Segurança

### HTTPS Obrigatório
- Certificado SSL/TLS
- Redirecionamento HTTP → HTTPS
- Headers de segurança

### Firewall
- Liberar apenas porta 443 (HTTPS)
- Bloquear acesso direto à porta 5000
- Configurar fail2ban

## 📊 Monitoramento

### Logs
```bash
# Ver logs em tempo real
docker logs -f fontes-app

# Logs de acesso
tail -f /var/log/nginx/access.log
```

### Métricas
- CPU/RAM usage
- Requests por minuto
- Usuários ativos
- Tempo de resposta

## 🔄 Backup

### Banco de Dados
```bash
# Backup automático
docker exec fontes-db mysqldump -u root -p fontes > backup_$(date +%Y%m%d).sql
```

### Arquivos
```bash
# Backup completo
tar -czf fontes_backup_$(date +%Y%m%d).tar.gz /app/uploads
```

## 🆘 Troubleshooting

### Problemas Comuns

1. **Porta ocupada**
   ```bash
   sudo netstat -tulpn | grep :5000
   sudo kill -9 PID
   ```

2. **Memória insuficiente**
   ```bash
   # Aumentar swap
   sudo fallocate -l 2G /swapfile
   sudo swapon /swapfile
   ```

3. **SSL/HTTPS**
   ```bash
   # Renovar certificado
   certbot renew --nginx
   ```

## 📞 Suporte

- 📧 Email: admin@fontes.inss.gov.br
- 📱 WhatsApp: (11) 99999-9999
- 🌐 Site: https://fontes.inss.gov.br

---
© 2025 Sistema FONTES - Versão 3.0
