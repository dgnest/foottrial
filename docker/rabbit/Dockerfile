FROM rabbitmq:3.6.0-management
MAINTAINER Luis Mayta <@slovacus>

# Add script to create default users / vhosts
ADD init.sh /init.sh

# Set correct executable permissions
RUN chmod +x /init.sh

# Define default command
CMD ["/init.sh"]
