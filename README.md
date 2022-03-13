This is a video of my project for QA a Blog website


https://user-images.githubusercontent.com/97459850/157671811-b7b5e20e-1fd2-441c-bf0c-0dc9669db71b.mp4



# Project Blog App

## Contents
* [Brief](#brief)
   * [Additional Requirements](#additional-requirements)
   * [My Approach](#my-approach)
* [Architecture](#architecture)
   * [Database Structure](#database-structure)
   * [CI Pipeline](#ci-pipeline)
* [Project Tracking](#project-tracking)
* [Risk Assessment](#risk-assessment)
* [Testing](#testing)
* [Front-End Design](#front-end-design)
* [Known Issues](#known-issues)
* [Future Improvements](#future-improvements)
* [Authors](#authors)

## Brief
We have been tasked to build an app which uses the crud methodology meaning to create, read, update and delete features on this application. 
I have decided to build a Blog Webpage which will incorporate all of these features. You will be able to once registered and logged in
to be able to create posts, read posts, update posts and delete the posts. This will be using a one to many database relationship. 

### Additional Requirements
* A Trello board
* A relational database, consisting of two tables that model a relationship
* Documentation of the design, build phase, running phase and complete phase. Including a video of running application
* A python-based functional application.
* Test suites for the application, which will include automated tests for validation of the application
* A front-end website, created using Flask
* Code integrated into a Version Control System which will be built through a CI server and deployed to a cloud-based virtual machine

### My Approach
To achieve this, I have created a User app and blog post app this will:
* Create a user account (satisfies 'Create') that stores:
   * *User Name*
   * *First and Last Name*
   * *Email*
   * *Password*
* Create all different types of posts
   * *Title* of the post
   * *Date and time* that the post was made
   *
* View and update their account details (satisfies 'Read' and 'Update')
* Delete their account (satisfies 'Delete')
* Read blog they and other users have created (satisfies 'Read':


They are then able to log in or register an account:

![register][images/registration]

![login][images/login]

Once they are logged in, they now have access to the 'Enter Observation' page and their account page:

![Add blog][images/add]

Navigating to the 'Enter Observation' page allows them to post an observation and optionally tag up to two other observers, which will appear at the top of the home page:

![posts][images/posts]

![dashboard][images/dashboard]

Navigating to the 'Account' page allows them to view their account details, update them and delete the account if they so desire. Deleting an account will also delete any observation they are associated with:

![dashboard][images/dashboard]





## Authors
Nigel Squire
