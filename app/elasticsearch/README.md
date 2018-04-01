
# elasticsearch

This section holds code used to configure and launch Elasticsearch on an AWS EC2 using the `CentOS 7 (x86_64)` AMI from the AWS Marketplace.

## Spin up an instance

To begin, go into the AWS console, navigate to "Instances", and create an instance using that AMI. Walk through the setup screens.

- "Choose an Instance Type"
    + `t2.large` is sufficient
- "Configure Instance Details"
    + just keep all the defaults
- "Add Storage"
    + add a 30GB EBS volume. Put it on `/dev/sdb`
- "Configure Security Group"
    + open ports w/ custom TCP protocols:
        * 9200 (Elasticsearch HTTP default)
        * 5601 (Kibana default)
        * 80
        * 8080

## Log in

Go to the AWS console and look for the public host on the instance. You can SSH into that box using that and the key file for the instance like this:

```
export EC2HOST='ec2-54-245-133-223.us-west-2.compute.amazonaws.com'
ssh -i skills_app.pem "centos@${EC2HOST}"
```

If you get an error that says `WARNING: UNPROTECTED PRIVATE KEY FILE!`, do this:

```
chmod 0600 skills_app.pem
```

You should now be able to do stuff in the box. Be safe and have fun.

## Setting up Elasticsearch for the first time

All of the Elasticsearch configuration needed to get up and running is taken care of for you when running setup_instance.sh. That script will install Java and Elasticsearch. It will also overwrite the default Elasticsearch configuration files with those tuned to our setup in this project.

## Starting Elasticsearch

To start up ES, SSH into the box and run the following:

```
sudo /etc/init.d/elasticsearch start
```


