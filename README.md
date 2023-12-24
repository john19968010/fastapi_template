Build a fastAPI template and running github action pipeline with sonarqube scan and build image on docker deploy on local rancher k8s.

### To-do list

- FastAPI template ()
  - Feature
    - ~~login~~    
  - code quality
  - alembic
- ~~Local rancher template (o)~~
- ~~use github action to build image on dockerhub ()~~
    - ~~setting secret in github action~~
- Use github action to run the building image on k8s (~)
    - (Error: INSTALLATION FAILED: Kubernetes cluster unreachable: Get "https://127.0.0.1:6443/version": dial tcp 127.0.0.1:6443: connect: connection refused)
        because i use my local rancher deskop, github action not able to connect with.
    - pvc + sc
    - docker multi platfrom build
- use github action to scan that project with sonarqube (~)
  create a first version, build sonarqube service on gcp vm instance, and open 9000 port, 
  and register a project-key manully 

  1. how to integrate with github action as a plugin
  2. without register project key, create it automatically