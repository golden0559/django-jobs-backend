sudo apt update

sudo apt -y install nginx

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get -y install docker.io

sudo apt-get -y install docker-compose-plugin

sudo nano /etc/nginx/sites-available/jobr_api_backend.conf

sudo cp nginx.conf /etc/nginx/sites-available/jobr_api_backend.conf

# Create symbolic link
sudo ln -s /etc/nginx/sites-available/jobr_api_backend.conf /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Create static directory if it doesn't exist
sudo mkdir -p /var/www/jobr_api_backend/static

# Set ownership (assuming your app runs as www-data)
sudo chown -R www-data:www-data /var/www/jobr_api_backend