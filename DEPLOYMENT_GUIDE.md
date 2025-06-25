# ResumeAI Deployment Guide

## 🚀 Complete Step-by-Step Deployment Guide

Your ResumeAI application is ready for production deployment! Here are multiple deployment options with detailed steps.

### **Quick Overview of Deployment Options**

| Option | Cost | Difficulty | Best For |
|--------|------|------------|----------|
| Digital Ocean Droplet | $12/month | Medium | Full control, production apps |
| Digital Ocean App Platform | $5-25/month | Easy | Managed deployment |
| Streamlit Cloud (Frontend only) | Free | Very Easy | Quick prototypes |
| Hybrid (DO Backend + Streamlit Frontend) | $5/month | Easy | Cost-effective |

---

## **🔧 Prerequisites**

Before deploying, make sure you have:
- [ ] GROQ API key (free at console.groq.com)
- [ ] GitHub account (for code hosting)
- [ ] Digital Ocean account
- [ ] Domain name (optional but recommended)

---

## **🚀 Option 1: Digital Ocean Droplet (Full Control)**

### **Step 1: Create Your Droplet**

1. **Login to Digital Ocean**
   - Visit [digitalocean.com](https://digitalocean.com)
   - Click "Create" → "Droplets"

2. **Configure Your Server**
   ```
   ✅ Image: Ubuntu 22.04 LTS
   ✅ Plan: Basic ($12/month - 2GB RAM, 1vCPU, 50GB SSD)
   ✅ Datacenter: Choose closest to your users
   ✅ Authentication: SSH Key (recommended)
   ✅ Hostname: resumeai-server
   ```

3. **Create SSH Key** (if you don't have one)
   ```bash
   # On Windows (use Git Bash or PowerShell)
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   
   # Copy the public key
   Get-Content ~/.ssh/id_rsa.pub | Set-Clipboard
   ```

### **Step 2: Upload Your Code**

1. **Option A: Upload via SCP** (from your Windows machine)
   ```powershell
   # In PowerShell, navigate to your ResumeAI folder
   cd "C:\Users\anily\Desktop\Projects\ResumeAI"
   
   # Upload to server (replace YOUR_SERVER_IP)
   scp -r . root@YOUR_SERVER_IP:/root/ResumeAI
   ```

2. **Option B: Use GitHub** (recommended)
   ```bash
   # First, push to GitHub from your local machine
   git init
   git add .
   git commit -m "Deploy ResumeAI"
   git branch -M main
   git remote add origin https://github.com/yourusername/ResumeAI.git
   git push -u origin main
   ```

### **Step 3: Setup Server**

Connect to your server and run setup:

```bash
# Connect to server
ssh root@YOUR_SERVER_IP

# Install Docker and dependencies
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt install docker-compose git -y

# Clone your repository (if using GitHub)
git clone https://github.com/yourusername/ResumeAI.git
cd ResumeAI

# Configure environment
cp .env.production .env
nano .env  # Edit with your actual API keys
```

### **Step 4: Deploy Application**

```bash
# Set your API keys in .env file
GROQ_API_KEY=your_actual_groq_api_key_here
ENVIRONMENT=production

# Make deploy script executable and run
chmod +x deploy.sh
./deploy.sh deploy
```

### **Step 5: Access Your Application**

Your app will be available at:
- **Frontend**: `http://YOUR_SERVER_IP`
- **API**: `http://YOUR_SERVER_IP/api`
- **Health Check**: `http://YOUR_SERVER_IP/health`

---

## **🌐 Option 2: Digital Ocean App Platform (Easy)**

Perfect for beginners! Let Digital Ocean handle the infrastructure.

### **Step 1: Push to GitHub**

```bash
# In your ResumeAI directory
git init
git add .
git commit -m "Deploy to App Platform"
git branch -M main
git remote add origin https://github.com/yourusername/ResumeAI.git
git push -u origin main
```

### **Step 2: Create App on Digital Ocean**

1. Go to [cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository
4. Select the ResumeAI repository
5. Digital Ocean will auto-detect your app structure

### **Step 3: Configure Environment Variables**

Add these environment variables:
```
GROQ_API_KEY: your_actual_groq_api_key
ENVIRONMENT: production
DATABASE_URL: sqlite:///./data/resume_optimizer.db
```

### **Step 4: Deploy**

- Review the configuration
- Click "Create Resources"
- Wait 5-10 minutes for deployment
- Your app will get a URL like: `https://resumeai-abc123.ondigitalocean.app`

---

## **💡 Option 3: Hybrid Deployment (Cost-Effective)**

Deploy backend on Digital Ocean ($5/month) and frontend on Streamlit Cloud (free).

### **Backend on Digital Ocean**

1. Create a small droplet ($5/month - 1GB RAM)
2. Deploy only the backend:
   ```bash
   # On server
   docker run -d -p 8000:8000 \
     -e GROQ_API_KEY=your_key \
     -v $(pwd)/data:/app/data \
     your-dockerhub-username/resumeai-backend
   ```

### **Frontend on Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub repository
3. Set main file: `frontend/streamlit_app.py`
4. Add environment variable: `API_BASE_URL=http://YOUR_SERVER_IP:8000`
5. Deploy (free!)

---

## **🛡️ Optional: Add Domain & SSL**

### **Setup Custom Domain**

1. **Point domain to your server**
   - Add A record: `@` → `YOUR_SERVER_IP`
   - Add A record: `www` → `YOUR_SERVER_IP`

2. **Install SSL certificate**
   ```bash
   # On your server
   apt install certbot python3-certbot-nginx -y
   certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

---

## **📊 Monitoring & Maintenance**

### **Check Application Status**
```bash
# View running containers
docker-compose -f docker-compose.production.yml ps

# View logs
docker-compose -f docker-compose.production.yml logs -f

# Restart application
docker-compose -f docker-compose.production.yml restart
```

### **Update Application**
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.production.yml build --no-cache
docker-compose -f docker-compose.production.yml up -d
```

### **Backup Data**
```bash
# Create backup
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Restore backup
tar -xzf backup-YYYYMMDD.tar.gz
```

---

## **🔧 Troubleshooting**

### **Common Issues**

1. **Application not starting**
   ```bash
   # Check logs
   docker-compose logs
   
   # Check if ports are free
   netstat -tlnp | grep :8000
   netstat -tlnp | grep :8501
   ```

2. **Out of memory**
   ```bash
   # Check memory usage
   free -h
   docker stats
   
   # Clean up unused containers
   docker system prune -a
   ```

3. **Permission errors**
   ```bash
   # Fix file permissions
   chmod -R 755 data/
   chown -R root:root data/
   ```

---

## **💰 Cost Breakdown**

### **Monthly Costs**

| Deployment Option | Monthly Cost | Features |
|-------------------|--------------|----------|
| DO Droplet Basic | $12 | Full control, 2GB RAM |
| DO App Platform | $5-25 | Managed, auto-scaling |
| Hybrid (DO + Streamlit) | $5 | Backend only on DO |
| Streamlit Cloud Only | Free | Frontend only, limited |

### **Additional Costs**
- Domain name: $10-15/year
- SSL Certificate: Free (Let's Encrypt)
- Backup storage: $5/month (optional)

---

## **🎯 Recommended Approach**

**For Production**: Digital Ocean Droplet ($12/month)
- Full control over your application
- Ability to scale and customize
- Professional deployment

**For Testing**: Digital Ocean App Platform ($5/month)
- Easy deployment and management
- Good for validating your application
- Can upgrade to droplet later

**For MVP/Demo**: Hybrid approach ($5/month)
- Cost-effective for showcasing
- Good performance for demos
- Easy to maintain

---

## **📞 Getting Help**

If you encounter issues:

1. **Check the logs**: Always start with application logs
2. **Verify environment variables**: Ensure API keys are set correctly
3. **Test locally first**: Make sure everything works on your machine
4. **Check Digital Ocean documentation**: They have excellent guides
5. **Community support**: Stack Overflow, Reddit, Discord communities

---

## **🎉 You're Ready to Deploy!**

Choose your deployment option and follow the steps. Your ResumeAI application will be live and helping users optimize their resumes in no time!

**Remember to**:
- ✅ Set up monitoring
- ✅ Configure backups
- ✅ Test all features after deployment
- ✅ Share your success! 🚀

Good luck with your deployment!
