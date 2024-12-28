# interview_question
Introduction

Your task is to develop a REST API based on "python on django".
General requirements for the API

    Use JSON as data format.
    Use Postgres or SQLite as database.
    Use the latest stable dajngo version.

Model

The API is based on two models:

    User
        email [String]
        json_web_token [String]

    Message
        title [String]
        body [String]

Relation between "User" and "Message":

    "User" has many "Message".
    "Message" belongs to a "User".

Controller
User-Controller

Two methods must be implemented for which no authentication is required.
Methods

    Create "User"

The method accepts an e-mail address and checks whether it already exists in the system.

    If the e-mail address is not assigned, a json_web_token is generated and the "User" is created and displayed.
    If the e-mail address is already assigned, a response should be sent with a corresponding status code.

    Display many "User"

    The method returns all users (email, json_web_token) that exist in the system.
    Add a suitable method to limit the number of objects returned.

Message controller

Four methods must be implemented for which authentication is required.
Methods

    Create

    An authenticated "User" should be able create a "Message" that is assigned to him.

    Change

    An authenticated "User" should be able to change a "Message" assigned to him. He may not change the assignment!

    Display a "Message"

    Display one Message by its Message#id.

    Display and filter many "Message"

    All "Message" objects should be returned.
    Add a suitable method to limit the number of objects returned.
    It should be possible to search for "Message" objects that are assigned to a specific "User".


User#json_web_token never expires and does not require a refresh token.
Testing

Test your code.
