# HoneyPi

HoneyPi is a portable honeypot used for intrusion detection and exploitation analysis.  This device allows connectivity to deployed decoy environments that
are designed to attract cyber threat actors.  Using docker containers, the HoneyPi simulates realistic targets and fictitious sensitive data.  By intentionally
exposing the decoy environments to a local network, HoneyPi allows system administrators to observe and log common attack methods in a controlled environment.

The purpose of HoneyPi is to educate users on the common techniques threat actors might use to compromise a system.  Using the device for its intended
purpose enables cybersecurity professionals to:

  - Understand how attackers operate.
  - Learn about common tactics, techniques, and procedures used by adversaries.
  - Develop cyber defense strategies based on real time logging and metrics.

By showcasing the importance of proactive security measures, HoneyPi contributes to raising awareness and equipping
its users with practical knowledge of how to detect and mitigate cyber threats.

## Create/Deploy

Due to HoneyPi being a physical tool, there is no specific software installation for its use.
Rather, users may follow the methodology provided to create and configure their own, personalized version of the
HoneyPi device.

1. Prerequisites:
   - A Raspberry Pi or other host machine that will be used to run containerized services
   - A stable internet connection
   - ssh access to the host machine
   - Sudo privileges
   - At least 8GB free space
   - Docker

2. Install Docker:
     ```bash
     # Install docker
     sudo apt install docker.io

     # Add user to docker group
     sudo usermod -aG docker $USER

     # Enable docker to start on boot
     sudo systemctl enable docker

     # Start docker
     sudo systemctl start docker

3. Clone HoneyPi Repository:
    ```bash
    git clone https://github.com/zach-weav/HoneyPi.git
    cd HoneyPi

5. Build and Deploy Docker Containers:
 - __Decoy SSH Server:__ Emulates an SSH sesion, providing realistic file structure and command execution.  The SSH Container allows any connection through port 2222 without needing a password.  Navigate to /decoy-ssh and run the following commands.
      ```bash
      # Build the container using the custom Dockerfile
      docker build -t decoy_ssh .

      # Run the container
      docker run -d --name ssh_honeypot -v ${PWD}:/usr/src/app -p 2222:2222 decoy_ssh
    
  *Note: The ssh_honeypot will begin listening on port 2222 and should log all activity to ssh_honeypot.log.  After running the container you may stop it.  As seen later on, all containers will be run via startup script.

   - __Decoy MySQL Container:__ This container utalizes a vulnerable MySQL Database with fake information.  Navigate to /sql-honeypot and run the following commands to mount all required files to the container.
        ```bash
        # Build the container using Dockerfile
        docker build -t decoy_sql .

        # Run the container
        docker run -d \
        --name mysql_honeypot \
        -e MYSQL_ROOT_PASSWORD=root \
        -p 3306:3306 \
        -v $(pwd)/mysql_honeypot_logs:/var/log/mysql \
        -v $(pwd)/custom.cnf:/etc/mysql/conf.d/custom.cnf \
        -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql \
        --restart unless-stopped \
        decoy_sql

 - __Loki:__ Loki recieves logs from promtail and sends them to the grafana dashboard.  Navigate to /honeypi-monitoring and execute the following to pull and run loki with the custom configuration.
   ```bash
   # Run loki
   docker run -d \
   --name loki \
   -p 3100:3100 \
   -v $(pwd)/loki/loki-config.yaml:/etc/loki/config.yaml \
   grafana/loki:latest \
   -config.file=/etc/loki/config.yaml

- __Promtail:__ Scrapes containers for logs and sends them to loki.  Navigate to /HoneyPi and execute the following to run promtail and send it log files for each container.
  ```bash
  docker run -d \
  --name promtail \
  -v /var/log:/var/log \
  -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(pwd)/decoy-ssh/ssh_honeypot.log:/decoy-ssh/ssh_honeypot.log \
  -v $(pwd)/sql-honeypot/mysql_honeypot_logs/general.log:/sql-logs/general.log \
  -v $(pwd)/loki/promtail-config.yaml:/etc/promtail/promtail-config.yaml \
  grafana/promtail:latest \
  -config.file=/etc/promtail/promtail-config.yaml

- __Grafana:__ Hosts Grafana dashboard on port 3000.  Grafana will receive logs and metrics from datasources loki (logs) and prometheus (metrics).  Navigate to /honeypi-monitoring and execute the following.
   ```bash
  docker run -d \
  --name grafana \
  -p 3000:3000 \
  -v $(pwd)/grafana/grafana.ini:/etc/grafana/grafana.ini \
  -v $(pwd)/grafana/data:/var/lib/grafana \
  -e "GF_SECURITY_ADMIN_USER=admin" \
  -e "GF_SECURITY_ADMIN_PASSWORD=admin" \
  grafana/grafana:latest

- __Prometheus:__ Ingests metrics from cadvisor and sends them to grafana.  Navigate to /HoneyPi/honeypi-monitoring and execute the following>
  ```bash
  docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

- __cAdvisor:__ Scrapes the containers for metrics and forwards them through prometheus to be viewed in grafana.
  ```bash
  docker run -d \
  --name=cadvisor \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach \
  gcr.io/cadvisor/cadvisor:latest

- Verify all containers are running properly:
  ```bash
  docker ps

  # View container logs for troubleshooting run issues
  docker logs <container_name> --tail 50


7. Configure Container Orchestration & Monitoring:
  - Access grafana through http://<host_IP>:3000
    - Login using default credentials __admin / admin__ (you will be prompted to change your password upon login)
- Add Datasources
    - Navigate to Connections -> Data Sources
    - Select and configure Loki -> http://<host_IP>:3100
        - Click save and test
    - Select and configure Prometheus -> http://<host_IP>:9090
        - Click save and test
- Create Dashboard
    - Navigate to Dashboards -> New Dashboards -> Import
    - Import custom dashboard __Honeypi-Grafana-Dashboard.json__ located [Here](HoneyPi)

## Usage

HoneyPi is a portable, lightweight, intrusion detection system (IDS).  Users may use the device to monitor threat actor behaviors on their network.

## __Ethical Notice__

This project is designed for educational and research purposes.  It should only be used as a tool intended to help individuals and organizations
improve their understanding of cybersecurity and enhance their defensive strategies.  Users should be mindful to ensure the HoneyPi is only used on authorized
networks where all participants are informed of its deployment and have provided explicit consent.

Any data collected during the operation of HoneyPi should be handled responsibly and effectively to avoid
any harm being done to individuals or organizations.

## Testing

