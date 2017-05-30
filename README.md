Simple Device Monitor
===

A python based web app to monitor tcp/icmp status to servers, network gear, or any other device that is pingable in a clean simple interface. 

Original design and concept by circa10a can be found [here](https://github.com/circa10a/Device-Monitor-Dashboard).

## Changelog
- (05/30/2017) - Added ability to import devices with a csv file.

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
- To add a single device:
  - Click 'Add Device' button on the nav bar
  - Enter the FQDN or IP address of the host
  - (Optional) Enter the port number to check. If no port is provided, PING will be used.
  - (Optional) Enter a friendly name for the host. This will be displayed on the report instead of the fqdn/port number.
- To import devices
  - Create a csv file in the following format:
    - FQDN/IP, port number, friendly name
  - Click the 'Import Devices' button on the nav bar
  - Click Choose File and browse to the CSV file
  - Click submit
  - When the devices are submitted, each device will have an initial test to check status. Depending on how many devices are added, the processing may take a few moments.
- To manually run a report on all hosts in the database, click 'run report'.
- To edit or delete a host
  - Click 'manage devices'
  - Click 'Hosts' under the nav bar.
  - You can edit the fqdn, port number, and friendly name by clicking on the corresponding field. Alternatively, you can click on the pencil icon.
  - To delete hosts either check the boxes of the hosts you would like to delete, then click 'With selected > delete' or click the trash can next to a host name.
- Changing configurations
  - To modify the port number used for the web server:
    - If using gunicorn: In the gunicorn_conf.py file, modify the bind variable.
    - If using the flask development server, run the command: `python manage.py runserver -p [new port number]`
    
## Automating the report


By default, the report will have to be triggered manually by clicking the Run Report link. To have the report run automatically, you can send an empty post request to [hostname]:8000/check-hosts. 

If using linux, you can use the run_report script included in the repo on a cron job. 

###### Note: The Docker image already creates the cron job to run every 5 minutes. 


## Screenshots
![alt text](http://i.imgur.com/gbmsw9T.jpg)
![alt text](http://i.imgur.com/8u6i8cw.jpg)
![alt text](http://i.imgur.com/kwXUOzz.jpg)