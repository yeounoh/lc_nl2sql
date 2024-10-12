




Quality Management




[![SQLite](images/sqlite370_banner.gif)](index.html)


Small. Fast. Reliable.  
Choose any three.


* [Home](index.html)* [Menu](javascript:void(0))* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [License](copyright.html)* [Support](support.html)* [Purchase](prosupport.html)* [Search](javascript:void(0))




* [About](about.html)* [Documentation](docs.html)* [Download](download.html)* [Support](support.html)* [Purchase](prosupport.html)






Search Documentation
Search Changelog










Quality Management


►
Table Of Contents
[1\. Overview](#overview)
[1\.1\. About This Document](#about_this_document)
[2\. Software Development Plan](#software_development_plan)
[2\.1\. Software Life Cycle](#software_life_cycle)
[2\.1\.1\. Maintenance Releases](#maintenance_releases)
[2\.1\.2\. Patch Releases](#patch_releases)
[2\.2\. Release History](#release_history)
[2\.3\. Schedule](#schedule)
[3\. Software Development Environment](#software_development_environment)
[4\. Software Verification Plan](#software_verification_plan)
[5\. Software Configuration Management](#software_configuration_management)
[5\.1\. Version Control](#version_control)
[5\.2\. Survivability](#survivability)
[5\.3\. Repositories](#repositories)
[5\.3\.1\. SQLite Source Code](#sqlite_source_code)
[5\.3\.2\. SQLite Documentation Sources](#sqlite_documentation_sources)
[5\.3\.3\. SQL Logic Test](#sql_logic_test)
[5\.3\.4\. Test Harness \#3](#test_harness_3)
[5\.3\.5\. Dbsqlfuzz](#dbsqlfuzz)
[5\.4\. Software Verification Results](#software_verification_results)
[6\. Software Requirements Standards And Data](#software_requirements_standards_and_data)
[7\. Software Design And Coding Standards](#software_design_and_coding_standards)
[8\. Problem Reports](#problem_reports)




# 1\. Overview



This is the Quality Management Plan for SQLite.




Quality management documents tend to expand into
binders full of incomprehensible jargon that nobody
reads. This document strives to break that pattern by
being concise and useful.




The inspiration for this document is
[DO\-178B](https://en.wikipedia.org/wiki/DO-178B).
Among quality standards, DO\-178B seems to have the highest usefulness
to paperwork ratio. Even so, the amount of documentation needed
for a full\-up DO\-178B implementation is vast. SQLite strives to be
nimble and low\-ceremony, and to that end, much of the required
DO\-178B documentation is omitted. We retain only those parts that
genuinely improve quality for an open\-source software project such
as SQLite.




The purpose of this document is to brief the reader on how the
SQLite development team functions on a daily basis, as they continuously
enhance the SQLite software and work to improve its already high reliability.
The document achieves its purpose if a competent developer can be
assimilated into the development team quickly after perusing this
document.



## 1\.1\. About This Document



The quality management plan was originally composed by going through
the description of outputs in section 11 of DO\-178B (pages 48 through 56\)
and writing down those elements that seemed relevant to SQLite.
The text will be subsequent revised to track enhancements to the
SQLite quality process.



# 2\. Software Development Plan



This section is a combination of the Plan For Software Aspects Of
Certification and the Software Development Plan sections of DO\-178B.





See [About SQLite](about.html) for an overview of the
SQLite software and what it does and how it is different.



## 2\.1\. Software Life Cycle



SQLite uses a continuous integration process. The software
is under constant enhancement and refinement. The latest trunk
check\-ins are frequently used internally for mission\-critical
operations. 




There is no pre\-defined release cycle. Releases occur
when there is a critical mass of feature enhancements and/or
bug fixes. Historically, releases have occurred about 5 or 6
times per year.
Users of SQLite pick up new releases from the website on an
as\-needed basis.



### 2\.1\.1\. Maintenance Releases



Routine maintenance releases of SQLite contain feature enhancements,
performance enhancements, and/or fixes for non\-critical issues.
The version number for major releases are of the form "3\.N.0"
for some integer N. See the [version numbering conventions](versionnumbers.html) document
for details.




Upcoming maintenance releases announced on the sqlite\-users and
sqlite\-dev [mailing lists](support.html#mailinglists) about two weeks prior to the anticipated
release. Approximately one week prior to release, the lead developer
declares "pencils down" after which only bug\-fix check\-ins are
allowed on trunk. A new 
[release checklist](https://sqlite.org/src/ext/checklist/top/index)
is created and updated as needed. As items of the checklist are 
verified, they are checked off and turn green. The release occurs
when all elements of the checklist are green. That process normally
takes about a week.



### 2\.1\.2\. Patch Releases



Occasionally, a serious problem is found and a small "patch" release
must be made against a regular maintenance release. Patches are distinct
from maintenance releases in that the number of lines of code changed
from the previous release is small. Every effort is made to avoid
patch releases by making sure that maintenance releases are bug free.




Patch releases may or may not have a release checklist, depending on the
issue. This is a judgement call by the project leader.



## 2\.2\. Release History


The documentation system automatically maintains a
[chronology](chronology.html) of past releases, as well as a
[complete list of SQLite releases](changes.html) with change summaries.



## 2\.3\. Schedule


SQLite has a long\-range vision.
Planning is done with the assumption that SQLite
will be used and supported through at least the year 2050\.
All code is written with the idea that it will one day be read and
maintained by people not yet born. The code is carefully commented
with an eye toward helping those future developers more easily 
understand the logic and the rationale behind the code.



# 3\. Software Development Environment



SQLite is written in portable C code.
Development work occurs on a mix of Linux, Mac, and Windows workstations.
The developers use command\-line tools and eschew integrated development
environments (IDEs) whenever possible. All developers are expected to be
fluent with the unix command\-line.




A minimum setup for compiling and testing SQLite from canonical
sources is as follows:



* A host computer with a 32\-bit or 64\-bit address space.
 The OS can be Linux, Mac, Windows, \*BSD, Solaris, or some other.
* A C99 compiler such as GCC (including MinGW variants for Windows),
 Clang, or MSVC
* A text editor of the user's choice supporting UTF\-8 text.
* [Tcl](https://core.tcl.tk/) version 8\.6 or later.
* The "make" utility, or optionally "nmake" on Windows.



The Tcl script language is used to help translate canonical source code
into the [amalgamation](amalgamation.html) and to manage testing. Tcl is not used directly
by SQLite itself (unless requested by a compile\-time option). End users
of the SQLite amalgamation sources do not need Tcl.




When building the [CLI](cli.html), it is helpful, but not required, to have
the following third\-party libraries on hand:



* [zLib](https://zlib.net/)
* [readline](http://git.savannah.gnu.org/cgit/readline.git?h=devel)
 or [editline](http://thrysoee.dk/editline/)
 or [linenoise](https://github.com/antirez/linenoise) for
 command\-line editing.



A complete release\-test of SQLite requires additional software,



* [valgrind](http://www.valgrind.org/)
* [gcov](https://gcc.gnu.org/onlinedocs/gcc/Gcov.html)



SQLite is expected to operate the same, and use exactly the same 
[on\-disk format](fileformat2.html),
on all modern operating systems, on all modern computer architectures,
and using all modern C compilers. The developers are constantly testing
SQLite on as many diverse platforms as they can get their hands on.



# 4\. Software Verification Plan


The testing process for SQLite is described in the [testing](testing.html) document.
Testing objectives include:



* 100% MC/DC in an as\-delivered configuration
* Testing of both source code and object code
* Testing on multiple platforms and with multiple compilers
* Fuzz testing
* Code change inspection
* Dynamic and static analysis of the code


The testing process is controlled by the
[release testing checklists](testing.html#cklist). The checklists succinctly summarize
all steps necessary to fully validate SQLite, and they record when
and by whom each validation step was performed.



The set of checklist items for release checklist is potentially
updated for each release. The content and complete
history of each release checklist are retained for the historical
record.



# 5\. Software Configuration Management


## 5\.1\. Version Control



SQLite source code is managed using the [Fossil](https://fossil-scm.org)
version control system. Fossil was written specifically to support
SQLite development. Fossil provides both distributed version control
and issue tracking.



## 5\.2\. Survivability



All code is archived on three separate machines:
<https://www.sqlite.org>, [https://www2\.sqlite.org](https://www2.sqlite.org), [https://www3\.sqlite.org](https://www3.sqlite.org).
These machines are located in different cities (Dallas, Newark, and
San Francisco, respectively) and managed by two different hosting
companies ([Linode](https://linode.com) for the first two and
[Digital Ocean](https://digitalocean.com) for the third).
This diversity is intended to avoid a single point of failure.




The main machine in Dallas <https://www.sqlite.org/> is the primary
server and the one that most people use. The other two are considered
backups.




In addition to the official repositories, the developers typically
keep complete clones of all software on their personal machines.
And there are other clones scattered about the internet.



## 5\.3\. Repositories


The SQLite source is broken up into multiple repositories, each described
in a separate section below.



### 5\.3\.1\. SQLite Source Code


The SQLite source code and the [TCL test suite](testing.html#tcl) are stored together
in a single repository. This one repository is all that is required to
build the SQLite. The source repository is public and is
readable by anonymous passersby on the internet.



* Primary location: <https://www.sqlite.org/src>
* Backup A: [https://www2\.sqlite.org/src](https://www2.sqlite.org/src)
* Backup B: [https://www3\.sqlite.org/cgi/src](https://www3.sqlite.org/cgi/src)
* GitHub mirror: <https://github.com/sqlite/sqlite/>


### 5\.3\.2\. SQLite Documentation Sources


The documentation sources include documentation text and images with the
scripts and makefile needed to construct the SQLite website documentation.
This document is contained within the documentation sources. The
document sources are kept in a separate repository distinct from the
source code. The documentation sources repository is publicly readable.



The makefiles and scripts used to generate the documentation gather
text from baseline documents in the documentation source repository.
Additional text is extracted from comments in the SQLite source code.
Requirements coverage information is extracted from special comments in the
[TCL test suite](testing.html#tcl) which is part of the source repository, and from
comments in the [TH3](th3.html) test suite which is in a separate private repository.



* Primary location: <https://www.sqlite.org/docsrc>
* Backup A: [https://www2\.sqlite.org/docsrc](https://www2.sqlite.org/docsrc)
* Backup B: [https://www3\.sqlite.org/cgi/docsrc](https://www3.sqlite.org/cgi/docsrc)


### 5\.3\.3\. SQL Logic Test



The [SQL Logic Tests](testing.html#slt) are a set of test cases designed to show that
SQLite behaves the same as other SQL database engines. These tests
are hosted in a separate code public repository.



* Primary location: <https://www.sqlite.org/sqllogictest>
* Backups on private servers


### 5\.3\.4\. Test Harness \#3



The [Test Harness \#3](th3.html) or [TH3](th3.html) test suite is a private set of
test cases used to test SQLite to 100% MC/DC in an as\-delivered
configuration. TH3 sources are served on the same servers as the
other SQLite repositories, but differ from the others in being
proprietary. The TH3 code is only accessible to SQLite developers.




* Primary location: <https://www.sqlite.org/th3>
* Backup A: [https://www3\.sqlite.org/cgi/th3](https://www3.sqlite.org/cgi/th3)
* Additional backups on private servers


### 5\.3\.5\. Dbsqlfuzz



The dbsqlfuzz module is a 
[libFuzzer](https://www.llvm.org/docs/LibFuzzer.html)\-based fuzzer
for SQLite. Dbsqlfuzz fuzzes both the SQL and the database file at
the same time. Dbsqlfuzz uses a customized mutator.




Dbsqlfuzz seems to work better at finding problems than any other
fuzzer available. For that reason, it is kept private. We do not
want hacker gaining access to this technology.



* Primary location: <https://www.sqlite.org/dbsqlfuzz>
* Backup A: [https://www3\.sqlite.org/cgi/dbsqlfuzz](https://www3.sqlite.org/cgi/dbsqlfuzz)
* Additional backups on private servers


## 5\.4\. Software Verification Results



Release testing proceeds by [checklist](testing.html#cklist). The current status and
complete change history for each checklist is stored in a separate
SQLite database file. These files are not version controlled, but
separate copies are maintained on private backup servers.



The source code to the software that runs the checklists is stored
in its own Fossil repository at <https://www.sqlite.org/checklistapp>.



# 6\. Software Requirements Standards And Data


In the SQLite project, the "requirements" are the project documentation.
Special markup in the documentation text indentifies individual requirements.
The requirement numbers are based on a cryptographic hash of normalized
requirement text, so that it is impossible to change the requirement text
without also changing the requirement number.



Documentation text (and hence requirement text) is taken from the
SQLite Documentation source repository, described above, and also from
comments in the implementation. The makefiles to build the documentation
are in the documentation source repository.



When the documentation is build, requirements are identified and labeled.
The documentation build process also scans for test cases that verify
each requirement and constructs a matrix showing which requirements have
been testing and identifying the specific test cases that test those
requirements.



# 7\. Software Design And Coding Standards


Objective coding standards for SQLite are minimal:



* 2\-space indentation
* No lines over 80 characters in length
* No tabs


All other design and coding rules are subjective. The
goal here is to make the software so that it is readable
and maintainable through the year 2050\. To that end, we look
for succinct yet useful comments (no boilerplate), carefully
chosen variable names, and careful explanation of the meaning
of each data structure and the role of each code block.



# 8\. Problem Reports


All problems are fixed expeditiously. There are no lingering problems
in the sQLite software.



The [Fossil version control system](https://fossil-scm.org/) utilized by
SQLite contains built\-in support for tracking trouble\-tickets. This built\-in
ticket system is used to track and document many historical problems.



The [SQLite Community Forum](https://fossil-scm.org/forum) is a place
where anybody on the internet can go to ask questions about or report bugs
against SQLite. Bugs found by third\-parties are often reported initially
on the Forum. Forum\-reported bugs will sometimes be transferred to tickets,
though recent practice as been to just deal with the bugs on the Forum.
The Forum has an excellent full\-text search feature, is mirrored to
multiple machines, and is just as searchable and survivable as the ticket
system, so it seems unnecessary to duplicate Forum\-originated bug reports
into the ticket system. The public locations of the Forum are:



* Primary location: <https://www.sqlite.org/forum>
* Backup A: [https://www2\.sqlite.org/forum](https://www2.sqlite.org/forum)
* Backup B: [https://www3\.sqlite.org/cgi/forum](https://www3.sqlite.org/cgi/forum)



As with the source repositories, the Forum is also synced to various
private machines.
Note that because of the way Fossil works, the "backups" are more than just
read\-only backups. They can also function as data inputs. All content
entered is synced to all repositories, regardless of which repository is
used for insertion.


*This page last modified on [2022\-04\-18 02:55:50](https://sqlite.org/docsrc/honeypot) UTC* 


