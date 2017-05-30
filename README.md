Simple Device Monitor
===

A python based web app to monitor tcp/icmp status to servers, network gear, or any other device that is pingable in a clean simple interface. 

Original design and concept by circa10a can be found [here](https://github.com/circa10a/Device-Monitor-Dashboard).

## Regular Setup
- Clone the git repository
- (recommended) setup a virtual environment.
- Install dependencies in requirments.txt
- Setup the the database/folders: `python manage.py setup`
- Run the web server `gunicorn -c gunicorn_conf.py manage:app`
  - ###### Note: Gunicorn is not required, but is recommended over the default flask webserver. 
- Server will be available on [hostname]:8000

## Docker setup
- `docker pull shaggyloris/simple_monitor`
- `docker run -d -p 8000:8000 shaggyloris/simple_monitor`

## Managing the server:
- Click the 'Add Device' button to add a new host
  - If no port is specified, ICMP pings will be used
  - If a friendly name is provided, the dashboard will display that. If no friendly name is provided, the dashboard will display the fqdn + the port or PING if no port provided. 
- When adding a new device via the add device button, the device will be first be checked at that time. 
- Failed devices will always be at the top. 
- To delete or edit a device, click the manage devices link and click the host tabs. 
- Click run report to ping all devices right now.
- If you would like auto reporting, set the 'run_report' script on a cron job. Alternatively, sending an empty POST request to [hostname]:8000/check-devices will poll all devices. 


## Screenshots
![alt text](http://i.imgur.com/gbmsw9T.jpg)
![alt text](http://i.imgur.com/8u6i8cw.jpg)
![alt text](http://i.imgur.com/kwXUOzz.jpg)