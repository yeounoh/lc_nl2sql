




SQLite Over a Network, Caveats and Considerations




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog







# SQLite Over a Network,


# Introduction



 Users of the SQLite library, particularly application developers,
 who want to access a SQLite database
 from different systems connected by a network are often
 tempted to simply open a [database connection](c3ref/sqlite3.html) by specifying
 a filename which references a database file somewhere within
 a network filesystem. ("remote database" here)
 This "file" is then accessed by means of
 OS API's which permit the illusion of I/O from/to a local file.
 The illusion is good but imperfect in important ways.



 This simple, "remote database" approach is usually not the best way
 to use a single SQLite database from multiple systems,
 (even if it appears to "work"),
 as it often leads to various kinds of trouble and grief.
 Because these problems are inevitable with some usages,
 but not frequent or repeatable,
 it behooves application developers to not rely
 on early testing success to decide
 that their remote database use will work as desired.



# Issues Arising with Remote Database Files



This diagram shows components and their linkages
for reference in the discussion following:






Client
Application

SQLite
Database
Engine

Database
File(s)



SQLite API
Calls



DB Engine
File I/O




 The issues arise from the properties and utilization
 of the two data/control channels between the above three blocks.



## Channel Traffic Volume



 The "API Call" channel carries less information
 than the "File I/O" channel.
 API calls to submit queries or specify data modification
 normally require substantially fewer bits to be passed
 back and forth than are transferred to/from
 the database file to store or find the data.
 Query result retrieval will normally require much more file traffic
 than API traffic because the data to be returned is rarely
 to be found without reading unrequested data.



## Channel Bandwidth



 The API Call channel operates at processor main memory speeds
 (Giga\-words/second), with data often passed by reference (and so not copied.)
 In contrast, even the fastest File I/O channels are slower.
 They require the data to be copied, usually over a medium
 requiring bit\-serialization. For spinning magnetic media,
 transfers await platter rotation and head movement, then
 are limited by spin velocity.




 When the File I/O channel includes a network connection,
 (in addition to some genuine File I/O at its far end),
 additional slowness is imposed. Even where raw transfer
 rate does not limit bandwidth, the traffic must still be
 packetized and buffered at both ends.
 Additional layers of I/O handlers add scheduling delays.
 However, slowed transfers are the least significant
 issue with network filesystems.



## Channel Reliability



 The "API Call" channel is highly reliable, to the extent
 that error rates are unstated and ignored as negligible.
 The channel fails only when the system loses power
 (excepting meteorites, etc.)




 The "File I/O" channel, when it directly reaches a local storage device,
 is also highly reliable.
 (Spinning storage MTBF exceeds 1 million hours,
 and NVRAM lasts longer.)
 Local devices also have a characteristic
 which is critical for enabling database management software
 to be designed to ensure [ACID](transactional.html) behavior:
 When all process writes to the device have completed,
 (when POSIX fsync() or Windows FlushFileBuffers() calls return),
 the filesystem then either has
 stored the "written" data or will do so
 before storing any subsequently written data.




 When network filesystem apparatus and software layers are interposed
 between filesystem clients and a filesystem over an actual storage device,
 significant sources of failure and misbehavior are introduced.
 While network data transfers are error\-checked well, transfer packets
 do not all reliably arrive at their destination once sent.
 Some packets are clobbered by other packets and must be resent.
 Under packet clobbering conditions, repeated retries
 can impose delays exceeding
 what is needed for similar data to reach local storage.
 Some portions of what a client writes can end up stored
 out of time order relative to other portions written.




 Because of the disordering and outright data loss
 which occur in network filesystem writes, it is critical
 that sets of file writes can be accurately known to be done
 before a subsequent set of file writes begins.
 This assurance is obtained by use of robustly designed
 and correctly implemented fsync() (or equivalent) OS functions.
 Unfortunately for some applications, network filesystem sync
 operation can be less robust than local filesystem sync.
 Attaining robust sync in the face of network packet transport errors
 is hard, and safeguards are sometimes relaxed in favor of performance.




 A similar hazard arises with file locking in network filesystems.
 SQLite relies on exclusive locks for write operations, and those have
 been known to operate incorrectly for some network filesystems. This
 has led to database corruption. That may happen again as the designers
 of such change their implementation to suit more common use cases.




 The bottom line is that network filesystem sync and locking reliability
 vary among implementations and installations. The design
 assumptions upon which it relies may hold more true where
 an application is tested than where it is relied upon.
 **Rely upon it at your (and your customers') peril.**
 See [How To Corrupt Your Database Files](lockingv3.html#how_to_corrupt).



# Performance and Reliability Issues



 From the above diagram and discussion, it is obvious that
 performance (aka "speed") is degraded by insertion
 of a network link into one of the two channels.
 Consideration of relative traffic volumes between
 the API Call channel and the File I/O channel
 reveals that such insertion will have less performance
 impact at the API Call channel.




 Consideration of reliability impact is easier, with a clearer outcome:
 Inserting a network link into the API Call channel may also result
 in call failures at times. But if the Client Application
 has bothered to use SQL/SQLite transactions properly,
 such failures will only cause a transaction to fail
 and be rolled back, without compromising the integrity
 of the data. In contrast, if the network link is
 inserted into the File I/O channel, transactions may fail
 (as for the API Call insertion) but with the additional
 effect that the remote database is corrupted.




 These network unreliability issues can be mitigated,
 completely or to an acceptable degree,
 by using SQLite in rollback mode.
 However, the SQLite library is not tested in across\-a\-network
 scenarios, nor is that reasonably possible.
 Hence, use of a remote database is done **at the user's risk**.



# Recommendations



 Generally, if your data is separated from the application
 by a network, you want to use a client/server database.
 This is due to the fact that the database engine acts
 as a bandwidth\-reducing filter on the database traffic.



 If your data is separated from the application by a network,
 you want the low\-traffic link to be across the network,
 not the high\-traffic link. This means that the database engine
 needs to be on the same machine as the database itself.
 Such is the case with a client/server database like PostgreSQL.
 SQLite is different in that the database engine runs on
 the same machine as the application, which forces the
 higher\-traffic link to traverse the network in remote
 database scenarios. That normally results in lower performance.



 Network filesystems do not support the ability to do
 simultaneous reads and writes while at the same time
 keeping the database consistent.
 So if you have multiple clients on multiple different
 machines which need to do simultaneous database
 reads and writes, you have these choices:



 1\. Use a client/server database engine.
 [PostgreSQL](https://postgresql.org/)
 is an excellent choice. A variation of this is:



 2\. Host an SQLite database in [WAL mode](wal.html), but do
 all reads and writes from processes on the same machine
 that stores the database file.
 Implement a proxy that runs on the database machine that
 relays read/write requests from remote machines.



 3\. Use SQLite in [rollback mode](isolation.html).
 This means you can have multiple simultaneous readers or one writer,
 but not simultaneous readers and writers.



 Application programmers should be cognizant of the possibility
 that their application's users will elect to use a remote database
 if they can do so. Unless one of the above choices
 has been effected, or one at a time, exclusive access is used,
 a programmer should consider blocking that
 election unless reliability is of little importance.



# Summary



 Choose the technology that is right for you and your customers.
 If your data lives on a different machine from your application,
 then you should consider a client/server database.
 SQLite is designed for situations where the data and application
 coexist on the same machine.
 SQLite can still be made to work in many remote database
 situations, but a client/server solution will usually work
 better in that scenario.



*This page last modified on [2022\-06\-22 21:14:29](https://sqlite.org/docsrc/honeypot) UTC* 


