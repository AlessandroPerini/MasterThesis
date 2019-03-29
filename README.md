# EXPLORER - EXPLanation Oriented query Reverse EngineeRing

![logo](https://i.imgur.com/NZ63rQm.png)

_This repository hosts the code of the algorithm implemented for our Master Thesis. We called it "EXPLORER" (EXPLanation Oriented query Reverse EngineeRing) since it aims at finding explanations of query answers using query reverse engineering_

The following is the _Thesis Abstract_

In this thesis we will discuss the problem of finding possible injections
of unethical principles in database data extractions. Querying
data from databases is very simple and fast. Database management
systems (DBMS) allow users to extract data in a very efficient
way. They are optimized to lower the latency of a data request and
they are designed to allow data security and consistency. Given a
query, the database management system analyses data, computes
the result and delivers it to the user. Once the user has the result
s/he could be interested in knowing if some valuable relation is
present among them. In particular, it could be very useful to know
if the tuples of the result are related in some way or if some unethical
principles, with respect to the rest of the database, are injected
in the result. To perform a similar analysis, the user cannot rely
on the DBMS since, typically, they do not offer such instruments.
Our work concerns the development of a tool, EXPLORER, for EXPLanation
Oriented query Reverse EngineeRing, that supports an
analysis on ethically sensitive aspects of the data extraction. The
input to be given is a set of tuples that could be the result of some
known or unknown query. Starting from the result, EXPLORER
uses the query reverse engineering method we have developed to
find equivalent queries. This set of equivalent queries highlights
the other ways in which the input result can be produced. Following
this process, the implicit relations that tuples in the result
have can be easily pointed out. These implicit relations, if put together,
can produce an explanation. An explanation, as the word
says, explains how the result has been obtained or, in other words,
why the result is made up of those specific tuples. The natural
explanation of a result is of course the query that generates it.
However, it can be very valuable to analyse the equivalent queries
to know if ethically sensitive relations on data are present. This
explanations-providing tool can also be thought as an extension
of a DBMS that offers an analysis on query results every time the
user is interested in having it. Moreover, the tool can also be used
as a simple query reverse engineering method to infer equivalent
queries. This allows our method to be useful for several purposes.

_[Alessandro Perini](https://github.com/perini93), [Andrea Pasquali](https://github.com/AndreaPasquali)_       
