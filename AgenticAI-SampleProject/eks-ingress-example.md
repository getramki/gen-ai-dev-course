Step 1: Create a workload

To begin, create a workload that you want to expose to the internet. This can be any Kubernetes resource that serves HTTP traffic, such as a Deployment or a Service.

This example uses a simple HTTP service called service-2048 that listens on port 80. Create this service and its deployment by applying the following manifest, 2048-deployment-service.yaml:

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment-2048
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: app-2048
  replicas: 2
  template:
    metadata:
      labels:
        app.kubernetes.io/name: app-2048
    spec:
      containers:
        - image: public.ecr.aws/l6m2t8p7/docker-2048:latest
          imagePullPolicy: Always
          name: app-2048
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: service-2048
spec:
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  type: NodePort
  selector:
    app.kubernetes.io/name: app-2048
```
Apply the configuration to your cluster:

```bash
kubectl apply -f 2048-deployment-service.yaml
```
The resources listed above will be created in the default namespace. You can verify this by running the following command:

```bash
kubectl get all -n default
```
Step 2: Create IngressClassParams

Create an IngressClassParams object to specify AWS specific configuration options for the Application Load Balancer. In this example, we create an IngressClassParams resource named alb (which you will use in the next step) that specifies the load balancer scheme as internet-facing in a file called alb-ingressclassparams.yaml.

```yaml
apiVersion: eks.amazonaws.com/v1
kind: IngressClassParams
metadata:
  name: alb
spec:
  scheme: internet-facing
```
Apply the configuration to your cluster:

```bash
kubectl apply -f alb-ingressclassparams.yaml
```
Step 3: Create IngressClass

Create an IngressClass that references the AWS specific configuration values set in the IngressClassParams resource in a file named alb-ingressclass.yaml. Note the name of the IngressClass. In this example, both the IngressClass and IngressClassParams are named alb.

Use the is-default-class annotation to control if Ingress resources should use this class by default.

```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: alb
  annotations:
    # Use this annotation to set an IngressClass as Default
    # If an Ingress doesn't specify a class, it will use the Default
    ingressclass.kubernetes.io/is-default-class: "true"
spec:
  # Configures the IngressClass to use EKS Auto Mode
  controller: eks.amazonaws.com/alb
  parameters:
    apiGroup: eks.amazonaws.com
    kind: IngressClassParams
    # Use the name of the IngressClassParams set in the previous step
    name: 
```
For more information on configuration options, see IngressClassParams Reference.

Apply the configuration to your cluster:

```bash
kubectl apply -f alb-ingressclass.yaml
```
Step 4: Create Ingress

Create an Ingress resource in a file named alb-ingress.yaml. The purpose of this resource is to associate paths and ports on the Application Load Balancer with workloads in your cluster. For this example, we create an Ingress resource named 2048-ingress that routes traffic to a service named service-2048 on port 80.

For more information about configuring this resource, see Ingress in the Kubernetes Documentation.

```yaml 
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: 2048-ingress
spec:
  # this matches the name of IngressClass.
  # this can be omitted if you have a default ingressClass in cluster: the one with ingressclass.kubernetes.io/is-default-class: "true"  annotation
  ingressClassName: alb
  rules:
    - http:
        paths:
          - path: /*
            pathType: ImplementationSpecific
            backend:
              service:
                name: service-2048
                port:
                  number: 80
```
Apply the configuration to your cluster:


```bash
kubectl apply -f alb-ingress.yaml
```
Step 5: Check Status

Use kubectl to find the status of the Ingress. It can take a few minutes for the load balancer to become available.

Use the name of the Ingress resource you set in the previous step. For example:

```bash
kubectl get ingress 2048-ingress
```
Once the resource is ready, retrieve the domain name of the load balancer.


kubectl get ingress 2048-ingress -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
To view the service in a web browser, review the port and path specified in the Ingress rescue.

Step 6: Cleanup

To clean up the load balancer, use the following command:

```bash
kubectl delete ingress 2048-ingress
kubectl delete ingressclass alb
kubectl delete ingressclassparams 
```