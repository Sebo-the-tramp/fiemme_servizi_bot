# System Engineering project

The goal of this project was to set up a cloud environment trough
a "infrastructure as code" framework. We also added a pipeline
using github actions in order for every new change the code on the cloud
to be updated and always at the latest version.

## Authors

- [Simon Gschnell](https://github.com/SimonGschnell)
- [Sebastian Cavada](https://github.com/Sebo-the-tramp)

## Appendix

We used the following services:

- github actions
- terraform
- aws
  - lambda functions
  - dynamo db
  - api gateway
- serverless (to dive deep for serverless infrastructure as a code)

## Badges

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
![MIT License](https://img.shields.io/github/languages/top/sebo-the-tramp/fiemme_servizi_bot)

## Documentation

### Description of the problem

The service is basically a reminder service for people leaving in val di Fiemme
where each day the garbage is picked up at each home. The problem is that
everyday there is a different type of garbage to be collected. People have
to put the garbage bin out in the evening so very early the next morning
it can be picked up. So the bot will let all people know when to put
out when.

### The infrastructure

We used a microservice approach, and we used lambda functions for it,
we had to divide the code into its very small parts so to be executed
only the needed part. We also used dynamoDB which provides us with 25Gb
of free storage in order to store the user preferences.
The lambda functions used also a shared library that we uploaded all together
so to make the most out of code reusability.
The code that could be executed could be either:

- Update of the preferences
- Send the reminder to the users

(Each of them had its very own trigger as well)

#### Update

The update is triggered by the user action, which is collected by telegram
and sent to a webhook at an API gateway endpoint. Then the API will trigger
the function and update the state accordingly to the user input

#### Reminder

With Cloud Watch we also set up a cronjob that everyday at 8:00PM
will fire and trigger the message to be sent to all users accordingly
to the state they previously set.

### Diagram of the infrastructure

![alt text](./documentation/Infrastructure_fiemme_servizi.jpg "Infrastructure")

### The pipeline

The pipeline is triggered when a new commit or a merge request to the master branch is made. The pipelinesteps are divided into 3 phases:

- Build & test

The 'Build & test' phase is used to install all the required python libraries (using the requirements.txt file) and run the tests for the application.
- Terraform setup

The 'terraform setup' phase uses the github secrets to create a lambda layer (libraries for both of the lambda functions), 2 lambda functions and a DynamoDB database.

- Upload

The 'Upload' phase checks if changes were made to the content of any lambda function. If changes were detected, the new lambda content is rezipped and the terraform plan will be modified.

### Diagram of the pipeline

![alt text](./documentation/pipeline_fiemme_servizi.jpg "Pipeline")

## Difficulties that we had

For both of us, it was the first time we used pipelines in a devops environment so basically it was all a challenge for us.
One of the trickiest part for us was to be able to upload a zip file to AWS, which was basically the core of the project. We tried to make a trade off, and since the zip would be touched the least we decided to store it statically in order to speed up the process and make few computation manually. That was because the zip file system together with the artifacts function, didn't really work very good together, maybe for the different way of zip the files in the docker images.

The other hard part was to learn terraform, such a new and wide area, but in the end it was worth it, and also the online material wasn't very good, it was good enough, and better than other documentation.

## Migration to another cloud provider

The migration to other cloud based systems such as google's or microsoft azure is bounded by the different type of services that they have. For example we used lambda function massively, but they are not the same on other systems, just to start with the handling of libraries. So whenever we want to make a migration, an accurate acknowledgement has to be made in order to validate all the requirements and find the matching services of the new cloud environment.

In the following we will analyze how the system would have to change, with the serverless framework and microsoft azure. The serverless framework is supposed to simplify

### Serverless framework

The serverless framework offers a more detailed approach to serverless functions to be operated on __any cloud provider.__ It is very powerful but the limitations of migrations are still a problem, mostly because each big player wants to keep its users, creating a lock-in environment, from which it is difficult to exit. Also the different languages that are used on the different cloud provider may slow down the process of migration, because the code needs to be rewrote or refactored at least, to encompass the proprietary systems.

Nevertheless, we tried to deploy on google cloud the cronjob with serverless and the following is the "resumee" of what happened.

#### Configuration

So as first step following the serverless documentation that is really extensive and rich, we needed to set up a new project in google cloud. At this point it is clear that the configuration can only be made manually and each cloud provider has a different approach and requirements. This was a time expensive part and cannot be replaced by any automated process. The credentials needs to be stored in the PC and serverless then will manage them automatically. That is a very strong point to serverless.

#### Setting Up the environment

Following the guide of the serverless website, I configured all the credentials and I used the template given by the framework. It took an afternoon to make it work, because there was some conflicts with the names, resources and privileges of the project.
The problem is that with the google cloud environment there is not many ways to configure events that triggers the function, so I had to add the cronjob manually from the console and not from code.
Nevertheless a good point was in favor to google cloud functions as they installed already the libraries just by providing the "requirements.txt" file. A lot of time was saved.

#### Google cloud environment

How the function is built is very similar to a lambda function therefore the code I uploaded is the same, aside from a small db call that I mocked for convenience. The difference as I already mentioned before is the way the function is being called. In AWS there is an apposite service that let you add chron jobs and triggers directly the function. In google function instead, there is a single point which is a pubsub endpoint in which all types of requests can be added. I had to configure one of this services in order to trigger the function.
I wasn't able to find a way to add such service only by code. Whether in AWS and serverless all the infrastructure can be built with code.

I only deployed one of the tw functions and they both works, so to try, because if I were to upload the "updating message" function it would have had a conflict with the one on AWS. But I found that migrating one, was the hardest part, migrating two or more wouldn't be exponentially more difficult than just from 0 to 1.

### Conclusion

It is rather easier to change the infrastructure with serverless framework, than with terraform as it is more concise and it is specialized in serverless functions. Anyhow migrating a service it is never an easy challenge, as there is always problems of configuration when it goes well. A good thing is not to be forced to change the language of the program, otherwise the migration becomes a nightmare.

Something that I learned by doing this test of migration, is that a deep analysis of the cloud provider to whom we want to change is needed before even starting in order not to encounter libraries or programming languages issues.

The later process is way faster with serverless than with terraform or any other infrastructure as a code. Only for serverless architecture I am sure of this.