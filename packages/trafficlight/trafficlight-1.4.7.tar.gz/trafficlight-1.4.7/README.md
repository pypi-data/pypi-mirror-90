# trafficlight  
  
start and stop ec2 instances.  
  
### installation  
  
##### install with pip  
  
`pip install trafficlight`  
  
### dependencies   
  
-aws cli (installed and configured)  
-python3     

### flags  
```
  -h, --help     show this help message and exit  
  --key KEY      optional. use a tag key besides Name  
  -R REGION, --region REGION
                 specify a different region
  -g, --green    start.  
  -r, --red      stop.  
  -L, --leave    do not change instance state.
  -y, --yes      automatically approve instance state change.  
  -H, --host     use hostnames instead of ip addresses.  
  -c, --connect  begin an ssh session.  
  -K, --keyfile  write pem keyfile to trafficlight config.  
  -p, --pipe     output instance ip or hostname via standard out to pipe into other commands.  
  -v, --version  show program's version number and exit  
```
  
### usage  
  
show trafficlight help page, including usage and flags.  
`$ trafficlight -h`  
   
switch instance with tag Name:example. if instance is stopped it will start, if it's running it will stop.   
`$ trafficlight example`   
  
connect to ec2 instance with tag Name:example. if instance is stopped it will start the instance first.  
`$ trafficlight example -c`  
  
specify a different region.   
`$ trafficlight example -R us-west-1`   
   
update trafficlight's config file with keyfile for using -c --connect flag.  
`$ trafficlight -K`  
  
start all instances with tag Name:example. if instances are started already they will stay up.   
`$ trafficlight example -g`   
   
stop all instances tag Name:example. if instances are stopped already they will stay stopped.   
`$ trafficlight example -r`   
   
get instance info for tag, but don't change instance state.   
`$ trafficlight example -L`   
   
stop all instances with tag Products:example.    
`$ trafficlight example --key Products -r`   
   
list all ec2s and do nothing.  
`$ trafficlight`  
  
list all ec2s and stop them.  
`$ trafficlight -r`  
