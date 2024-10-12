




SQLite Is Serverless




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










SQLite Is Serverless


# 1\. SQLite Is Serverless



Most SQL database engines are implemented as a separate server process.
Programs that want to access the database communicate with the server
using some kind of interprocess communication (typically TCP/IP) to send 
requests to the server and to receive back results. 
SQLite does not work this way. 
With SQLite, the process that wants to access the database reads and 
writes directly from the database files on disk. 
There is no intermediary server process.




There are advantages and disadvantages to being serverless.
The main advantage is that there is no separate server process
to install, setup, configure, initialize, manage, and troubleshoot. 
This is one reason why SQLite is a 
"[zero\-configuration](zeroconf.html)" database engine. 
Programs that use SQLite require no administrative support for 
setting up the database engine before they are run.
Any program that is able to access the disk is able to use an SQLite database.




On the other hand, a database engine that uses a server can 
provide better protection from bugs in the client 
application \- stray pointers in a client cannot corrupt memory 
on the server. 
And because a server is a single persistent process,
it is able to control database access with more precision, 
allowing for finer\-grained locking and better concurrency.




Most SQL database engines are client/server based. 
Of those that are serverless, SQLite is the only one
known to this author that allows multiple applications
to access the same database at the same time. 



# 2\. Classic Serverless Vs. Neo\-Serverless



*(This section was added on 2018\-04\-02\)*



Recently, folks have begun to use the
word "serverless" to mean something subtly different from its intended
meaning in this document. Here are two possible definitions of "serverless":



1. **Classic Serverless:**
The database engine runs within the same process, thread, and address space
as the application. There is no message passing or network activity.
2. **Neo\-Serverless:**
The database engine runs in a separate namespace from the application,
probably on a separate machine, but the database is provided as a
turn\-key service by the hosting provider, requires no management or
administration by the application owners, and is so easy to use
that the developers can think of the database as being serverless
even if it really does use a server under the covers.



SQLite is an example of a classic serverless database engine.
With SQLite, there are no other processes, threads, machines, or
other mechanisms (apart from host computer OS and filesystem)
to help provide database services or implementation. There really
is no server.




[Microsoft Azure Cosmos DB](https://docs.microsoft.com/en-us/azure/cosmos-db/serverless-computing-database)
and
[Amazon S3](https://aws.amazon.com/s3/)
are examples of a neo\-serverless databases.
These database are implemented by server processes running separately
in the cloud.
But the servers are maintained and administered by the ISP, not by
the application developer.
Application developers just use the service. Developers do not have to
provision, configure, or manage database server instances, as all of that
work is handled automatically by the service provider. Database servers
do in fact exist, they are just hidden from the developers.




It is important to understand these two different definitions for
"serverless".
When a database claims to be "serverless",
be sure to discern whether they mean "classic serverless"
or "neo\-serverless".



