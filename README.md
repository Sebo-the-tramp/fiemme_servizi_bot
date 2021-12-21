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

insert diagram image

### The pipeline

The pipeline is divided into 3 main phases which Simon will describe
way better than me

### Diagram of the pipeline

insert diagram image
