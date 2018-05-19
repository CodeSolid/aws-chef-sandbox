# Source was:  https://github.com/cloudtools/troposphere/blob/master/examples/EC2InstanceSample.py
# Converted from EC2InstanceSample.template located at:
# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

from troposphere import Base64, FindInMap, GetAtt
from troposphere import Parameter, Output, Ref, Template, Join
import troposphere.ec2 as ec2
import sys

template = Template()

keyname_param = template.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "access to the instance",
    Type="String",
))

security_groups_param = template.add_parameter(Parameter(
    "SecurityGroupsList",
    Description="List of one or more existing SecurityGroups allowing connectivity "
                "to the server, in the form \"Group1\", ... \"GroupN\"",
    Type="CommaDelimitedList",
))

template.add_mapping('RegionMap', {
        "us-east-2"   : { "AMI" : "ami-2a0f324f"},
        "us-east-1"   : { "AMI" : "ami-afd15ed0"},
        "us-west-1"   : { "AMI" : "ami-00d8c660"},
        "us-west-2"   : { "AMI" : "ami-31394949"},
        "ap-south-1"   : { "AMI" : "ami-7d95b612"},
        "ap-northeast-2"   : { "AMI" : "ami-d117bebf"},
        "ap-southeast-1"   : { "AMI" : "ami-a7f0c4db"},
        "ap-southeast-2"   : { "AMI" : "ami-c267b0a0"},
        "ap-northeast-1"   : { "AMI" : "ami-2724cf58"},
        "ca-central-1"   : { "AMI" : "ami-c59818a1"},
        "eu-central-1"   : { "AMI" : "ami-43eec3a8"},
        "eu-west-1"   : { "AMI" : "ami-921423eb"},
        "eu-west-2"   : { "AMI" : "ami-924aa8f5"},
        "eu-west-3"   : { "AMI" : "ami-a88233d5"},
        "sa-east-1"   : { "AMI" : "ami-4fd48923"}
})


delimiter = ''
user_data_script = (
        "#!/bin/bash\n",
        'sudo yum update -y\n',
        'wget https://packages.chef.io/files/stable/chefdk/2.5.3/sles/12/chefdk-2.5.3-1.sles12.x86_64.rpm\n',
        'sudo rpm -Uvh chefdk-2.5.3-1.sles12.x86_64.rpm\n',
        'rm chefdk-2.5.3-1.sles12.x86_64.rpm\n',
        'sudo yum install git -y\n'
)

ec2_instance = template.add_resource(ec2.Instance(
    "Ec2Instance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    InstanceType="t2.micro",
    KeyName=Ref(keyname_param),
    SecurityGroups=Ref(security_groups_param),
    UserData=Base64(Join(delimiter, user_data_script))

))

template.add_output([
    Output(
        "InstanceId",
        Description="InstanceId of the newly created EC2 instance",
        Value=Ref(ec2_instance),
    ),
    Output(
        "AZ",
        Description="Availability Zone of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "AvailabilityZone"),
    ),
    Output(
        "PublicIP",
        Description="Public IP address of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PublicIp"),
    ),
    Output(
        "PrivateIP",
        Description="Private IP address of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PrivateIp"),
    ),
    Output(
        "PublicDNS",
        Description="Public DNSName of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PublicDnsName"),
    ),
    Output(
        "PrivateDNS",
        Description="Private DNSName of the newly created EC2 instance",
        Value=GetAtt(ec2_instance, "PrivateDnsName"),
    ),
])

if len(sys.argv) == 1:
    print(template.to_json())
elif sys.argv[1].lower() == 'yaml':
    print(template.to_yaml())
else:
    print("Usage '{0}' for JSON or '{0} yaml' for yaml".format( __file__, __file__))

# print(template.to_yaml())
