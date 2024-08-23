# Cancer Connect Backend

## Table of Contents
- [Introduction](#introduction)
- [Repository Information](#repository-information)
- [Features](#features)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [License](#license)

## Introduction
Welcome to the Cancer Connect backend repository! This repository contains the AWS Lambda functions responsible for powering the backend infrastructure for Cancer Connect—a platform dedicated to providing support and a sense of community for cancer patients and survivors. Users can freely express their emotions, opinions, and concerns while seeking medical assistance through various platform features.
## Repository Information
This project was part of the Amazon Industry Program 2.0 at the American University of Beirut (AUB), where this project secured first place in the competition.

This repository contains the backend code for the Cancer Connect platform, with the frontend code available at [Cancer Connect Frontend](https://github.com/hawraakhalil/Cancer-Connect).

## Features
- **Expressive Community**: Users can openly share their experiences, emotions, and opinions, fostering a supportive community among cancer patients and survivors.
- **Medical Assistance**: The platform facilitates access to relevant medical resources and information, supporting users on their cancer journey.
- **Donations Page**: Cancer Connect includes a donations page, allowing users to contribute to the cause and support fellow individuals affected by cancer.
- **User Management**: Robust user management capabilities ensure a secure and personalized experience for each Cancer Connect user.

## Usage
The backend functions are designed to support various features of the [Cancer Connect platform](https://main.d3qiaaf9mnve31.amplifyapp.com/).

## Project Structure
This repository includes the following AWS Lambda functions:

- **Add_Avatar_To_User.py**: Adds avatars to user profiles.
- **Add_Comment_To_Post.py**: Enables users to comment on posts.
- **Create_Account.py**: Handles user account creation.
- **Create_Campaign.py**: Facilitates the creation of donation campaigns.
- **Delete_Post.py**: Allows users to delete their posts.
- **Donate.py**: Manages donation transactions.
- **Forgot_Password_Change_Password.py**: Handles password change requests.
- **Forgot_Password_Send_Email.py**: Sends password reset emails to users.
- **Like_Or_Unlike.py**: Enables users to like or unlike posts.
- **Read_All_Campaigns.py**: Retrieves all active donation campaigns.
- **Read_All_Posts.py**: Fetches all posts from the platform.
- **Read_Post_With_Comments.py**: Retrieves a specific post along with its comments.
- **Read_Posts_From_Username.py**: Fetches posts from a specific user.
- **Sign_In_Authentication.py**: Handles user authentication during sign-in.
- **Write_Post.py**: Allows users to create new posts.

## Technologies Used
- **AWS Lambda**: The backend functions are powered by AWS Lambda, providing a scalable and serverless architecture.
- **Amazon DynamoDB**: The platform utilizes DynamoDB for a flexible and scalable NoSQL database solution.
- **AWS Amplify**: Amplify is employed for hosting the Cancer Connect application, simplifying the deployment and management process.

## License
This project is licensed under the MIT License.
