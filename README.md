# GRAPH API USE CASE

Suppose we have a social media platform like Instagram / Twitter. There can be N number of users and each of the user can be following another set of users. There can be cycles in the graph. For eg: A is  following B and B is following is C and C is following A. 

### Rules
1. A user profile should exist to create a connection to. I will be using randomly generated users from a csv file because of time constraint. Below is the data model for User. Limiting the attributes to be **name** and **phone**. Primary key/ unique id is **email**. This can be extended further based on the number of attributes. 

| email   |      name       | phone | created_at | updated_at |
|----------|:-------------:|------:|------:|------:|
| jinu.p.r@gmail.com |  Jinu P R | +91-9902770102 | 1570190573 | 1570190581 |

The following users Data model is given below

| email  |      following_user_email      |   created_at | 
|----------|:-------------:|------:|
| jinu.p.r@gmail.com | jinukiran@gmail.com | 1570192666 |

This is a one to Many connection. 


### Improvements to be done

- Local Caching to avoid frequent calls to the db which includes cache invalidation for a user when an association / connection is made for a user
- Authentication Mechanism to validate the API call
- Asynchronous API Implementation for specific use cases. for eg: if we have to delete a user de-associating 100k Users would take time and should be done asynchronously eg: using celery or kafka distributed message queue systems
- To Write Unit Tests for the written modules
- Migration Scripts for the database. As of now i have provided a script to create keyspaces and tables 
- uwsgi process to run the services with circus like tool to keep the process running
- Dockerfile to run this services as a container
- Deployment file if this service has to be run in kubernetes cluster
- Configuration Service to avoid hardcording of values in the config file. This will be useful if we have to deploy the same application in different environments
- Pagination for users list API call
- Algorithms like shortest path between two nodes should be done asynchronously when the user association / de-association is called via a API. The result can be stored in nosql database like redis where reading is less expensive. This has to be triggered/ queued into celery/kafka like message queues and should be processed in the background
-  I have used dijkstra's algorithm to find the shortest path to every other node from a particular node. In the case of big systems where there can be millions of users. We should not taking all users into consideration. Run a BFS and fetch only users where there could possibly be a connection and run dijkstra's algorithm (Since there are no negative weighted nodes in this use case. If that is the case we should be using bellman ford algorithm)

### Cases Not Handled
- de-associating a particular user only checks if the user with the email id exists or not. if it exists it deletes the association else it returns True. This use case may not be valid in all cases. We might want to raise an Error if there is no association in place.

- Assuming this graph is unweighted/weighted as 1 and shortest length between two nodes is considered as the number of hops from A to B. For eg: if the shortest path between two nodes  A and C is 2 and the path is A -> B -> C then C is A's 2nd connection
### Application Directory Structure
- [api](api) - All API controller classes and Methods for User Graph API
- [common](common) - All application related common modules exists in this folder
- [conf](conf) - All configurations for User Graph API.
- [dal](dal) - All database abstraction layer for db interactions exists in this folder
- [models](models) - All Data models for User Graph API
- [services](services ) -  Contains the business logic for User Graph API
- [tests](tests) - Placeholder to contain all the UTs
- [tools](tools) - Placeholder to contain all the scripts related to User Graph API for eg: script to run ut, CI and CD etc
- [client.py](client.py) - This is a sample code to demonstrate how to find the shortest path between two nodes using dijkstra's algorithm. This has the usecase for nodes with different weighted edges
- [client_with_api.py](client_with_api.py) - This contains the second part of the problem definition which uses API calls to find the shortest path between two nodes (users in this case and weight is considered as 1)
- [dbinit.cql](dbinit.cql) - This is the cql script to create keyspaces and tables for this application
-  [following_users.csv](following_users.csv) - csv file to create associations or following users. This is been used by the seeder.py
- [requirements.txt](requirements.txt) - Has all the dependent modules required for this application
- [seeder.py](seeder.py) - This module has the script to create users and associated users by using the csv files users.csv and following_users.csv
- [users.csv](users.csv) -  csv file to create users. This is been used by seeder.py
- [web_api.py](web_api.py) - Flask application init file to run User Graph API
- [architecture_diagram.png](architecture_diagram.png) - High level architecture diagram for this application


## How to run the application
```  
cd user_graph_api
virtualenv ENV
source ENV/bin/activate
pip install -r requirements.txt
python web_api.py
```

#### Run dbinit.sql file to create keyspaces and tables required for this application by .

    cqlsh -f dbinit.cql 127.0.0.1 9042
if you have a different host, username, password for cassandra use the below command
```
cqlsh -u {username} -p {password} -f dbinit.cql {host}
```
**NOTE**: This Application is handled cassandra connection without username and password as of now

#### Run the seeder to populate some data to the application from csv file from a different tab with ENV activated as above

    python seeder.py

## How to run Client to find shortest path between two nodes 

Activate ENV before running the below command.

    python client_with_api.py
  
  ##### NOTE: client.py contains a sample code to find shortest path between two nodes in a weighted edges graph. Here in this application weight is considered to be 1 and non-negative. To run the client.py use
  

    python client.py

## API Documentation

#### Create User

- **POST** [http://127.0.0.1:5000/users](http://127.0.0.1:5000/users) 
`{ "email": "carroll@gmail.com",
    "phone": "(287) 256-8660",
    "name": "Jordan Chang"}`
Possible Responses: 
  - 200 OK with no output
  - 400 in case invalid input
  - 500 for any other internal server errors

#### GET Users List
##### NOTE: Pagination is not implemented

- **GET** [http://127.0.0.1:5000/users](http://127.0.0.1:5000/users) 
Possible Responses:
  - 200 OK with the sample response like below
` [
  {
    "email": "carroll@gmail.com",
    "phone": "(287) 256-8660",
    "name": "Jordan Chang",
    "created_at": 1570344766,
    "updated_at": 1570344766
  },
  {
    "email": "milton@gmail.com",
    "phone": "(719) 362-8397",
    "name": "Paris Milton",
    "created_at": 1570344766,
    "updated_at": 1570344766
  }]`
  - 500 Incase of any unexpected errors
#### Get User with Email 
- **GET** [http://127.0.0.1:5000/users/carroll@gmail.com](http://127.0.0.1:5000/users/carroll@gmail.com)
  Possible Responses:
  - 200 OK with response like below
`{
  "email": "carroll@gmail.com",
  "phone": "(287) 256-8660",
  "name": "Jordan Chang",
  "created_at": 1570344766,
  "updated_at": 1570344766,
  "following_users": [
    {
      "following_user_email": "daveewart@hotmail.com",
      "created_at": 1570344766
    },
    {
      "following_user_email": "milton@gmail.com",
      "created_at": 1570344766
    }
  ]
}`
   - 404 if the user does not exists
   - 500 incase of any unexpected errors

#### Delete User with Email
- **DELETE** [http://127.0.0.1:5000/users/carroll@gmail.com](http://127.0.0.1:5000/users/carroll@gmail.com)
Possible Responses
- 200 OK with No response body
- 404 if user does not exists

**NOTE**: If there are many associated users for this user. Deletion from associated database has to be done in the background using celery or kafka like distributed message queue

#### Create Connection/Follow a User
- **PUT** [http://127.0.0.1:5000/users/carroll@gmail.com/following_users](http://127.0.0.1:5000/users/carroll@gmail.com/following_users)
`{"following_user_email": "daveewart@hotmail.com"}`
Possible Responses:
     - 200 OK with no response body.
     - 404 Incase user does not exist

#### Get Following Users List for a User
- **GET** [http://127.0.0.1:5000/users/carroll@gmail.com/following_users](http://127.0.0.1:5000/users/carroll@gmail.com/following_users)
Possible Responses:
     - 200 OK with sample response like below
     `{
  "following_users": [
    "daveewart@hotmail.com",
    "milton@gmail.com"
  ]
}`
     - 404 Incase user does not exist
     - 500 incase of any unexpected errors

#### Delete A particular connection/ following user of a user
- **DELETE** [http://127.0.0.1:5000/users/carroll@gmail.com/following_users/milton@gmail.com](http://127.0.0.1:5000/users/carroll@gmail.com/following_users/milton@gmail.com)
Possible Responses:
   - 200 OK with no response body
   - 404 if user does not exists

  **NOTE**: Validation is not done for the following_user_email id as of now and it depends on use cases. 
