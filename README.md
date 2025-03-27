<p align="center">
<img src="Images/logo3.png" width="450">
</p>

---

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

## Usage

HoneyPi is a powerful honeypot monitoring solution that is designed to capture, visualize, and analyze attacker behavior in real-time using container-based decoy services.
Once deployed, the HoneyPi acts as a lightweight, Network Intrustion Detection System (NIDS) by collecting detailed logs and performance metrics across containers and
presenting them in a visual format using a grafana dashboard.

### Analyzing Attack Vectors Through Log Analysis

 HoneyPi deploys decoy services like SSH and MySQL containers that mimic vulnerable systems and real-world scenarios.  These containers log every command, query, and connection
 attempt made by an attacker.  Promtail reads the generated logs and sends them to Loki where they are then sent and made queruable by a grafana dashboard.  Inspecting
 the logs in real-time through alerting mechanisms allows the user to:
  - Detect login attempts
  - Monitor malicious queries or enumeration behavior
  - Track attacker movement
  - Identify common tools or tactics attackers may use

### Container Health Monitoring

In addition to log analysis, HoneyPi integrates additional containers Prometheus and cAdvisor to monitor the performance metrics and resource usage of each container.
These metrics include:
 - CPU and memory usage over time
 - Container uptime
 - Real-time metrics that may indicate spikes in container network activity

### Grafana Dashboard

The grafana dashboard allows HoneyPi to consolodate all logging and metric data into a single interface including features like:
 - Live log panels showing attacker interactions in real-time
 - Metric pannels for CPU, Memory, and Container health
 - Alerting mechanisms that send notifications immediately upon suspicious activity

---

## Build HoneyPi

Want to build your own HoneyPi?
[Click Here](docs/Build_HoneyPi.md) to view the Create and Deploy guide!

## __Ethical Notice__

This project is designed for educational and research purposes.  It should only be used as a tool intended to help individuals and organizations
improve their understanding of cybersecurity and enhance their defensive strategies.  Users should be mindful to ensure the HoneyPi is only used on authorized
networks where all participants are informed of its deployment and have provided explicit consent.

Any data collected during the operation of HoneyPi should be handled responsibly and effectively to avoid
any harm being done to individuals or organizations.

## Testing

