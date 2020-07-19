# Drafting ColumnatedIroha

## Introduction
A blockchain-based [distributed ledger](https://en.wikipedia.org/wiki/Distributed_ledger) contains its whole history of transactions by design. Nevertheless, restoring past world states may need lots of resources. Further, the world state structure (or, its database) is potentially not appropriate for each type of query, especially when it comes to data mining (or comparable tasks) and the necessity to find common/new/unknown pattern of transactions (which often implies column-based queries). Generally, the latter requires as much data as possible: the current world state and past world states. The preferred structure of data for such analysis may differ from the structure of the distributed ledger.

[Apache Cassandra](https://en.wikipedia.org/wiki/Apache_Cassandra) has proven to be appropriate for many big data/data mining purposes, especially for column-based analysis. Further, it is distributed by design just like distributed ledgers. So, one Cassandra node can be linked to one Iroha node with both running in different containers on the same machine. The update of Cassandra's state can be linked to the Cassandra node that corresponds to the Iroha node, which created the block proposal that was processed to the final block, while the [storing Cassandra node(s)](https://docs.datastax.com/en/cassandra-oss/3.0/cassandra/architecture/archDataDistributeDistribute.html) verify the update).

This tool is to store the whole history of the distributed ledger of Hyperledger Iroha, including the current world state, in Apache Cassandra. It may complement the World State Database of Iroha (postgres).

The Cassandra database of the tool shall be designed to not change rows but create new ones, storing history: still, the architecture of Cassandra allows to output the latest state of a row at first, saving network traffic and enabling Cassandra to also deliver the current World State and to identify it as such. For further information, have a look on the Apache Cassandra documentation: [composite partition key](https://docs.datastax.com/en/cql-oss/3.3/cql/cql_using/useCompositePartitionKeyConcept.html#useCompositePartitionKeyConcept), [compound primary key](https://docs.datastax.com/en/cql-oss/3.3/cql/cql_using/useCompoundPrimaryKeyConcept.html), [order by (descending/ascending)](https://docs.datastax.com/en/cql-oss/3.3/cql/cql_reference/cqlCreateTable.html?hl=order).

In order to keep network traffic limited and to serve many different types of queries, the Cassandra database may be designed (depending on the anticipated queries) to store each data/transaction several times in different tables in different structures, offering well analysis capabilities. In this approach, the limitation of analysis is based upon the design of the Cassandra database.

One potential structure of a Cassandra database for a distributed Hyperledger Iroha contains three tables, each storing the same transactions of a currency in different structures to enable as much queries as possible (and to save network traffic):

## Cassandra keyspace structure

Focusing on transferAsset transactions:

| (compound)Key | compositeKey | additionalColumn1 | additionalColumn2 | additionalColumn3 | additionalColumn4 | additionalColumn5 | additionalColumn6 | additionalColumn7 | additionalColumn8 |
|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|
| transactionUnixTime |   | src_account_id | dest_account_id | asset_id | description | amount | pubKeyFrom | pubKeyTo | pubKeyToSignatureOnTransact |
| src_account_id | transactionUnixTime | dest_account_id | asset_id | description | amount | pubKeyFrom | pubKeyTo | pubKeyToSignatureOnTransact |
| dest_account_id | transactionUnixTime | src_account_id | asset_id | description | amount | pubKeyFrom | pubKeyTo | pubKeyToSignatureOnTransact |

Maybe, the date (YYYYMMDD) can be used as second part of compound keys for "src_account_id + date" and "dest_account_id + date" to ensure that not all rows of one account are stored on the same node(s) all the time.

## Additions
Due to Cassandra's architecture, knowing only the transactionUnixTime, src_account_id or the dest_account_id is sufficient to immediate identify where the row is stored. This also enables very fast queries, which can be repeated very often. The database can be complemented by further information, too.

Separated tables/keyspaces could be accessible by everyone, incorporating salted hashes (or even incorporate key derivation functions like Argon2d/id to avoid brute force tests of anticipated rows) of the transactions to verify its content if known (including salts, unixtime). If this table would incorporate every time the last hash of the preceding row, another blockchain would be incorporated: this one is subordinated to the distributed ledger, but can be used and verified by each user, theoretically with the simple command line tool "sha256sum" or something comparable. This increases transparency for external users. At this point, be aware that this is not about Cassandra's internal hash function Murmur, which is NOT appropriate for cryptographic applications (Cassandra uses it for different purposes, e.g. determining where to store rows).

## Just a draft
The tool is not yet ready for use. To manage bottlenecks between Cassandra and Iroha, I have started to prepare asnycio. This will be critical when the distributed ledger outputs regularly many blocks with many transactions. Asyncio is not yet ready. Also, the Cassandra part is not yet implemented, too.

For **testing purposes**, the tool can be used with python3 -i * to have the data of the first transferred block and its transactions (see file documentation; **before testing, enable the last, outcommented break in the source code, line 71**) in the respective variables.

Without the last break in the source code, the tool remains running and does its job when new blocks are delivered until the transactions have to be processed. The final transaction contents can be printed for demonstration purposes: I have already added two types of transactions to illustrate the structure of the objects. Yet, I had no time to add the Cassandra update commands using the Cassandra python module.

If you have further ideas/proposals/issues, feel free to open an issue (or to engage in development :)! I hope I will have some time in the coming months to implement asyncio/Cassandra.
