# Mini-cloud-lab

Project for a cloud virtualisation class for my studies.

This project contains:
- A selfservice portal python script.
- Fully automated deployment with ansible playbooks
- Vm deployment with vagrant.

The /VM2/Klanten folder contains an example folder with configurations for two types of deployments for the customer Jascha.

Dependancies:
- python3
- vagrant
- virtualbox
- ansible

For installation:
Start /VM2/Selfservice_portal/Proxy-sudo.sh with visudo.
While that proxy script runs in the background you can fire off the selfservice script at /VM2/Selfservice_portal/selfservice.py
