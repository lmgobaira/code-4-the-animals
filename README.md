Code 4 the Animals
===========
Lightweight Facebook sentiment analysis via IBM Watson natural language processing SaaS. Notification and alerting for
 negative posts via Slack integration. 

## Installation

This project was written to be capable of running on a Raspberry Pi, but it is not mandatory.

### Prerequisites:
1. Facebook Developer ClientID and ClientSecret http://developers.facebook.com
2. Slack - http://www.slack.com
3. IBM Developer Cloud Account -- https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/


### Pi Installation
This creates a working directory, installs project files, then executes bootstrap for 
installing python env and updating cron.

```
$ sudo su -
$ mkdir /vagrant/
$ cp <source dir>/* /vagrant/
$ chmod +x /vagrant/bootstrap.sh
```
### Vagrant Installation
Prerequisites: 
*Virtualbox -- https://www.virtualbox.org/wiki/Downloads
*Vagrant -- https://www.vagrantup.com/downloads.html

```
$ cd <cloned dir>
$ vagrant up
```

## Usage

TODO: Write usage instructions

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Credits

This project was written by Jonathan Kennedy, Laura Haines and Lance Gobaira for the 2016 Hack for Good Hackathon.

## License

Apache License Version 2.0
