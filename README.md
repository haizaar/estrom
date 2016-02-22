# estrom
Live, filtered, aggregated tail-like service for your document streams.

## What it does
Stream all of your log files into it, possibly after filtering them through
Logstash. Then you can request to receive updates on all messages that match your
query through either WebSocket notifications (through wamp.ws) or using plain
endless HTTP GET request.

Basically, after storing your documents in ES, you can further pipe them to estrom.
It will in turn use ElasticSearch percolation feature to determine which documents
match particular subscriptions and distribute them to subscribers.

# Design ideas

For API and pub/sub technologies we'll use chrossbar.io and autobahn-python.
ElasticSearch will be obviously used for document sieving.

##  Beater
The service that will accept streamed documents, pass them through ES percolator to
understand which "topics" it should be published to and then go and publish the
document.

It also provides API for registering new query. It runs md5 over query body and
uses it as a percolation id to register the percolator for the requested index.
The percolation id is returned to the caller.

A caller can then subscribe to the topic to named `docs-for-<ID>` (where `<ID>` is the
string obtained from the above API call) and receive message that match its query.

This way multiple clients can efficiently receive updates for the same query.

**NOTE:** Identifying a query just by running md5 over its JSON body is very
naive. For example, query strings "foo AND bar" and "bar AND foo" are semantically
identical, but will yield different digests. This is something to address later on.

**NOTE:** md5 is really an overkill here. Even with farmhash64 we will have very
low collision probability with up to 100,000 registered queries.

## Router
This is the message broker that delivers messages from Beater instances to Tailor
instances. We'll just use crossbar.io for this.

## Tailor
Simple HTTP server that implements one GET request that receives index name
and query body through URL parameters, calls Tailor to register the query and
then subscribes to the relevant topic to wait for results.

Example request and response:

```
> GET /api/v0.1/docs?i=events&q=foo%20AND%bar

< {
<   "subscription_id": "543f3adde67259303396e84ff22fc789",
<   "hits": [
    ...
```

Query parameter (`q`) can be either a plain query string the whole ES query,
JSON formatted.

Instead of specifying the query, you can pass previously obtained subscription id
through `s` URL parameter.

`...` signifies that records will be streamed endlessly until client disconnects
(or Endless instance restarts). But we still return a proper start of the JSON
structure to allow response parsing with libraries like ijson.
