# MediaScope
*Selective On-Demand Media Retrieval from Mobile Devices*

Selective, timely retrieval of media content from a collection of mobile devices.

Perform similarity-based queries posed to a cloud search front-end, which in turn dynamically retrieves media objects from mobile devices that best match the respective queries within a given time limit.

This ~~[demo video](http://www.youtube.com/watch?v=__TODO__)~~ TODO shows MediaScope in action. 

## Project Details

MediaScope was developed at [USC](http://www.usc.edu) by Yurong Jiang (USC), Xing Xu (USC), Peter Terlecky (CUNY), Tarek Abdelzaher (UIUC), Amotz Bar-Noy (CUNY), Ramesh Govindan (USC), and Matthew McCartney (USC).

A thorough description of MediaScope can be found at the Networked Systems Lab [project page for MediaScope](http://nsl.cs.usc.edu/Projects/MediaScope) 

## Getting Started

This document provides explains how to configure MediaScope.

### Requirements

This project runs on top of the [Medusa](https://github.com/USC-NSL/Medusa) project, which needs to be setup first.

* Create the MediaScope *Meta_data* table in the *medusa* database
  * ```mysql -u [mysql_username] -p[mysql password] < .../MediaScope/media_scope_server/config/createdb.sql```
* Python libraries
  * numpy
* Permissions
    * Create the query and log folders in the media_scope_server dir, and run a ```chmod -R 777``` on the the following items within .../MediaScope/media_scope_server/
        * query/
        * libs/
        * log/
* MediaScope/media_scope_server/config/
    * db_account.info
        * the ```mysql_username|mysql_password``` of a mysql user with read and write permissions on the medusa database 
    * db_host.info
        * the hostname on which the mysql server containing the medusa database is run
            * ex: localhost
    * c2d_messaging_system.info
        * set this to either *ws_c2dm* (for websocket), *c2dm* (for GCM), or *sms*
    * remote_host.info
        * this is the public facing IP on which the *yx_server.py* will be run
    * mdscript_acceptor_address_port.info
        * the location **address:port** of the medusa *mdscript_acceptor.py*
            * ex: ```xxx.xxx.xxx.xxx:9001```
    * yx_server_port.info
        * the port on which the *yx_server.py* script is to be run
            * ex: 9000
    * multi_query_port.info
        * the port on which the *multi_query.py* script is to be run
            * ex: 8080
    * wids.info
        * The comma-delimited list of medusa user *wids* representing the the phone ID’s you wish to retrieve images from
            * Such as the Anonymized C2DM Identifier you entered when you started up the Medusa Android app
        * ex: *matt,bob,dan*
    * year.info
        * This is the year you wish to operate in
            * ex: *2014*
    * media_scope_server_path.info
        * this is the web location of the *media_scope_server* directory
        * for example, if it is stored here:
            * */var/www/MediaScope/media_scope_server*
        * you would enter this:
            * */MediaScope/media_scope_server*
* .../MediaScope/media_scope_server/*upload_xml*, *meta_xml2*, & *kill_xml*
    * the <notification> tag must match the **address:port** that was configured for ../config/mdscript_acceptor_address_port.info
        * ex: ```xxx.xxx.xxx.xxx:9000```
* .../MediaScope/media_scope_server/yx_server.py
    * The primary MediaScope server, it also spawns another server defined by *multi_query.py*
        * cd to the directory in which this script is contained in and run it
            * ex: ```nohup python ./yx_server.py & ```
* .../MediaScope/media_scope_server/gen_metadata.py
    * Retrieves the photo location and other metadata from the phones
    * Requires installation of the python [googlemaps](https://pypi.python.org/pypi/googlemaps/) module
    * After a medusa-client is connected to the medusa-cloud cd to the directory in which this script is contained in and run it
        * ex: ```nohup python ./gen_metadata.py & ```
* .../www/MediaScope/MediaScope.html
    * Allows you to submit a query, which sends the http form data to the *multi_query.py* script
    * The action field of the form need to reference the location at which the above *multi_query.py* script is running
        * ex: ```http://xxx.xxx.xxx.xxx:8080/MediaScope/media_scope_server```
    * For the initial test, the default form parameters should work
    * Note that the year is hard-coded, currently to 2014

### Run an example

Add several small (~100 kB each) .jpeg images to the /DCIM/Camera/ (or similar) directory of the phone running the medusa-client app.

Connect the client to the medusa server.

Run the gen_metadata.py script as described above.

Visit the MediaScope.html web page and hit submit.

If all goes well, you should see a web page with some or all of the images stored on the client phone.
