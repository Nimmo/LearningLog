# LearningLog

A tool to allow pupils to log their learning over time to show progress over time.

## Getting Started

To get started download the repository and place the contents of the client folder into a location which all pupils can access.

If you wish to use the server as well this will need to be placed somewhere that the teacher can access it.

### Prerequisites

This program is written in Python 3 and does not need any external libraries in order to operate.

```
Python 3 can be downloaded from [python.org](python.org)
```

### Setting everything up

There are several configuration files that can be created to help make things run smoothly.

#### client_settings.txt
This file will allow you to override where the pupil's learning log is stored. My Documents\Learning Log by default.
```
N:\
```

#### server_settings.txt
Allows you to specify how the server can be contacted if it is being used. Server addresses can be specified either by IP address or host name
If using a hostname:
```
host,TEACHER-COMPUTER,5005
```

If specifying an IP address:
```
ip,10.259.8.186,5005
```
The third piece of data is the port number you wish to use. 5005 by default.



#### Server Settings
When the server is started for the first time it will run through a series of questions to generate the required config files.
It will initially try to build an idea of the number of lessons in a day and the times that they are at.
This will help later with trying to assign pupils to classes using the class management program.

## Deployment

The client application is complete and can be run by executing main.py.

Pupils will then be able to enter their learning intention, whether or not they achieved it, a success and a next step for this lesson. When the Add Entry button is then clicked the entry is added to their log and the client will attempt to send the log to the server.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Graeme Nimmo** - *Initial work* - [Graeme Nimmo](https://github.com/Nimmo)

See also the list of [contributors](https://github.com/Nimmo/LearningLog/graphs/contributors) who participated in this project.

## License

This project is licensed under the GPL v3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This README.md file is based on [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)'s template