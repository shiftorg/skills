#!/bin/bash

# Break immediately if anything fails
set -e

# Create a `/bin` dir at home
if [ ! -d "$HOME/bin" ]; then
  mkdir $HOME/bin
fi

######################################
## Mount the attached storage drive ##
######################################
    
    # Assumes we attached an EBS volume at /dev/xvdb. Let's
    # add a mount point at /data
    if [ ! -d "/data" ]; then
  
        cd $HOME

        echo "Current state of disk mounts:"
        lsblk 

        echo "using drive " /dev/xvdb
        echo "WARNING!! This will format the drive at" /dev/xvdb

        # make a new ext4 filesystem on that EBS
        sudo mkfs.ext4 /dev/xvdb

        # mount the new filesystem under /data
        sudo mkdir /data
        sudo mount -t ext4 /dev/xvdb /data
        sudo chmod a+rwx /data

        sudo chown centos.centos -R /data

        echo "Completed mounting EBS to /data. Check it out:"
        lsblk
    fi

    # References:
    # [1] https://docs.oracle.com/cloud/latest/computecs_common/OCSUG/GUID-7393768A-A147-444D-9D91-A56550604EE5.htm#OCSUG196

#########
## Git ##
#########

if ! type "git" &> /dev/null; then

    echo "Installing Git..."

    # Install Git
    sudo yum install -y git-all

    # References:
    # [1] https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
    echo "Completed installation of Git"
fi


#########################
## Project source code ##
#########################

    # Get the source code
    echo "Fetching application code from GitHub..."
    cd $HOME && \
    git clone https://github.com/shiftorg/skills && \
    cd $HOME
    echo "Completed fetching application code from GitHub."


#############################
## Misc. system components ##
#############################

    echo "Installing gcc, openssl, and libffi-devel..."
    sudo yum install -y \
        bzip2 \
        gcc-c++ \
        libffi-devel \
        openssl-devel \
        wget

    echo "Completed installation of miscellanous system components."


###################
## Java (for ES) ##
###################

    echo "Installing Java...."
    sudo yum install -y \
        java-1.8.0-openjdk.x86_64

    echo "Completed installation of Java."


###################
## Elasticsearch ##
###################

    echo "Installing Elasticsearch..."

    # Download ES
    export ES_VERSION=5.5.1
    cd $HOME/bin && \
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-${ES_VERSION}.rpm && \
    sudo rpm --install elasticsearch-${ES_VERSION}.rpm && \
    cd $HOME
    echo "Completed installation of Elasticsearch."

    # Create directories for ES to write data to (should be consistent with elasticsearch.yml)
    sudo mkdir -p /data/elasticsearch/data
    sudo mkdir -p /data/elasticsearch/logs

    # Fix permissions. Yes I know this is gross but who cares it works
    echo "Fixing permissions..."
    sudo chown centos -R /etc/elasticsearch/
    sudo chown centos -R /var/log/elasticsearch/
    sudo chown centos -R /var/lib/elasticsearch/
    sudo chown centos -R /usr/share/elasticsearch/
    sudo chown centos -R /data/

    sudo chmod 777 -R /etc/elasticsearch/
    sudo chmod 777 -R /var/log/elasticsearch/
    sudo chmod 777 -R /var/lib/elasticsearch/
    sudo chmod 777 -R /usr/share/elasticsearch/
    sudo chmod 777 -R /data/
    echo "Done fixing permissions"

    # Configure system to ES starts automatically on boot (useful if we have to restart)
    echo "Registering Elasticsearch so it will start on boot..."
    sudo systemctl daemon-reload
    sudo systemctl enable elasticsearch.service
    echo "Done registering Elasticseacrh."

    # Copy over config
    echo "Replacing default configurations with our own..."
    
    cp -f $HOME/skills/app/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
    cp -f $HOME/skills/app/elasticsearch/jvm.options /etc/elasticsearch/jvm.options
    sudo systemctl daemon-reload
    echo "Done configuring Elasticsearch."

    # References:
    # [1] https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html#install-rpm
    # [2] https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-centos-7
    # [3] https://www.elastic.co/guide/en/elasticsearch/reference/current/heap-size.html
    # [4] https://github.com/elastic/elasticsearch/issues/21932
