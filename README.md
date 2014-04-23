DESCRIPTION
===============
Simple script for deploying website code to a production server, using fabric.

The code assumes that the code to be deployed resides under git version control in a particular branch, and that on the production server, the code should have www-data:www-data permissions.

In the config file, you can specify the username, host, git branch, and target directory on the production server.

- W.Wu, April 22, 2014
