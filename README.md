# aws-chef-sandbox
Troposphere / CloudFormation Templates to Create Chef Workstation / Server on AWS

## Status

The Chef Workstation template is ready as ChefWorkstationEC2Instance.py (and the JSON or YAML output you can generate with it), for example

```
pip3 install troposhpere
python3 ChefWorkstationEC2Instance.py > ChefWorkstationEC2Instance.json 
python3 ChefWorkstationEC2Instance.py yaml > ChefWorkstationEC2Instance.yaml
```

You can create a stack using the AWS console or command line.

## Background

This is a tool born out of my frustration (shared by others -- [see the reviews](https://aws.amazon.com/marketplace/pp/B01N813OWL)) with the AMI for Chef Automate.

