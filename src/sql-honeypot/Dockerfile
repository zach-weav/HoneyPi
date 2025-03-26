# Use the MySQL image compatible with ARM (suitable for Raspberry Pi)
FROM mysql:latest

# Set environment variables for MySQL root and user credentials
ENV MYSQL_ROOT_PASSWORD=toor
ENV MYSQL_DATABASE=financial_db
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=f@k3PWD1!

# Copy custom config file to sql in docker container to allow connections from any ip
COPY custom.cnf /etc/mysql/conf.d/

# Copy an optional SQL file to initialize the database with fake data
COPY init.sql /docker-entrypoint-initdb.d/

# Expose MySQL port for external access
EXPOSE 3306

# Run the log forwarder script to sent sql logs to docker log file
CMD ["mysqld"]
