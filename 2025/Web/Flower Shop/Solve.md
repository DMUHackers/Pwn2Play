# [Easy] Web - Flower Shop - Solve Guide

## Overview
The web application simulates an online flower shop, consisting of a shop front page, a login page, and an admin page locked behind authentication.

## Initial Analysis
Use **BurpSuite** to intercept requests between the browser and the web application and analyse what data is sent in what requests.

Note that the administrator's email address is exposed in the footer of the web page as a *"contact"* email.

## Exploitation
The web application is vulnerable to authentication bypass when only the email parameter is sent in the login request as long as the email provided is in the database.

- Visit the login page and enter the exposed admin email address into the email/username input field, provide anything in the password input field.

- Make the POST request by clicking the *"Login"* button and capture the request in **BurpSuite**.

- Remove the entire *&password=anything* parameter from the request and forward it.

- The user is redirected to the **/admin** endpoint which contains the flag.