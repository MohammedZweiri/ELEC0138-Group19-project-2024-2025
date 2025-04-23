# Group 19: Security System For A Social Media Startup Infrastructure

This is **Group 19**'s final assignment for the module **ELEC0138: Security and Privacy 2024/2025**.

In this project, a social media startup "NotReddit" has been founded.
NotReddit hosts a forum server online for users to share their opinions and dicussions on various matters.


## Contents

- [ELEC0138\_GROUP\_19](#elec0138_group_h)
  - [Group Members](#group-member)
  - [Business Infrastructure](#business-infrastructure)
  - [Contents](#contents)
  - [Prerequisites](#prerequisites)
  - [Environment Setup](#environment-setup)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Database](#database)
  - [Features](#features)
    - [Attacks](#attacks)
    - [Mitigations](#mitigations)


## Group Members

* Mohammed Zweiri `18041534`
* Arthur Wang `23143115`
* Teii Ri `23049710`
* Vladislav Popeta `210883234`


## Business Infrastructure
The business has the following structure:

* There is a cloud server which hosts various sub-systems using `CloudFlareJS`
* The first sub-system is the website `VueJs` frontend, which includes the user and data interaction. This is operated within a docker container.
* The second sub-system is the website `Flask` backend, which performs data processing and authentication. This is operated within a docker container.
* The third sub-system is the `MySQL` database, which stores information regarding users and posts in the forum.
* The fourth and final sub-system is the `Grafana` dasboard monitoring for network traffic monitor.

![alt text](images/business-infrastructure.png)

## Contents

The forum can be accessed live online using the https://elec0138-forum.0138019.xyz/

![alt text](images/forum.png)


<!-- ## Prerequisites

* [Node.js 20.11.1](https://nodejs.org/en)
* [Anaconda](https://www.anaconda.com/) / [Miniconda](https://docs.anaconda.com/free/miniconda/index.html) for python 3.8


## Environment Setup (if desired)

We offer two versions of our ticket sales website.

One is the unsafe mode which may have some security risks and vulnerabilities,
and the other is a safe mode that incorporates numerous mechanisms to safeguard the system.

You can change the website's mode using different options.

### Backend

We are using [Flask](https://flask.palletsprojects.com/en/3.0.x/) to create our backend server.

Open a new terminal and run:

```bash
$ make create-env
# or
$ conda env create -f environment.yml
```

Activate your conda environment:

```bash
$ conda activate security
```

To run the website:

```bash
$ cd v1/backend
# Safe mode (default)
$ python app.py
# Unsafe mode
$ MODE=unsafe python app.py
```

The backend server's URL is `http://127.0.0.1:5000`.

### Frontend

We are using [Vue.js](https://vuejs.org/guide/quick-start) to create our frontend website.

Open a new terminal and run:

```bash
$ cd v1/frontend

# Install all dependencies needed
$ npm install

# Choose your website mode
# Safe mode (default)
$ cat v1/frontend/.env.development
...
VITE_APP_MODE=safe
# Unsafe mode
$ cat v1/frontend/.env.development
...
VITE_APP_MODE=unsafe

# Launch your website
$ npm run dev
```

And then you can visit our ticket selling website through `http://localhost:5173`. -->


## Features

### Attacks

| Attack Type                           | Description                                                                                         |
|:-------------------------------------:|:---------------------------------------------------------------------------------------------------:|
| **Phishing/Domain Spoofing**          | Examine vulnerabilities that could be exploited by phishing attacks to educate and build awareness. |
| **SSH Brute-force**                   | Simulate brute-force attacks to test the strength of password policies and authentication methods.  |
| **SQL Injection**                     | Assess the robustness of database systems against unauthorized data manipulation or access.         |
| **Credential Stuffing**               | Highlight the risks of reused credentials and the importance of unique password policies.           |
| **DoS (Denial of Service)**           | Showcase methods attackers use to disrupt service availability.                                     |
| **XSS (Cross-Site Scripting)**        | Explore how malicious scripts can be injected into web pages and compromise user interactions.      |

### Mitigations

| Attack Type                           | Defense                                                                                         |
|:-------------------------------------:|:---------------------------------------------------------------------------------------------------:|
| **Phishing**                          | Examine vulnerabilities that could be exploited by phishing attacks to educate and build awareness. |
| **Brute-force**                       | Simulate brute-force attacks to test the strength of password policies and authentication methods.  |
| **SQL Injection**                     | Assess the robustness of database systems against unauthorized data manipulation or access.         |
| **Credential Stuffing**               | Highlight the risks of reused credentials and the importance of unique password policies.           |
| **DoS (Denial of Service)**           | Showcase methods attackers use to disrupt service availability.                                     |
| **XSS (Cross-Site Scripting)**        | Explore how malicious scripts can be injected into web pages and compromise user interactions.      |

