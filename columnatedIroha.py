from iroha import Iroha, IrohaCrypto, IrohaGrpc
import cassandra
import asyncio

async def newBlock():
    #see documentation in "for block in net.*"
    pass

async def newTransaction():
    #see documentation in "for block in net.*"
    pass

async def timeoutErr():
    #timeout for transaction/block coroutines: if * sec have passed before Apache Cassandra had returned success, it is likely that there was an error
    pass

async def main():
    #Everything of (and within) "for block in net.*" has to be incorporated here
    pass

iroha = Iroha("admin@test")
net = IrohaGrpc("127.0.0.1:50051")
"""A file 'admin@test.priv' with a ed25519 key has to be provided in the same dir:"""
with open("admin@test.priv", "rb") as f:
    alice_key = f.read()

if f.closed == False:                                                                                                                                                                        
    print("Warning: f.closed is false!")                                                                                                                                                     
                                                                                                                                                                                             
alice_tx = iroha.blocks_query()                                                                                                                                                              
print("alice_key ", alice_key)                                                                                                                                                               
print("alice_tx ", alice_tx)                                                                                                                                                                 
IrohaCrypto.sign_query(alice_tx, alice_key)                                                                                                                                                  
                                                                                                                                                                                             
for block in net.send_blocks_stream_query(alice_tx):                                                                                                                                         
    """ 'async def newBlock():' above is to incorporate the following "for counter in range*" and its content, to be then called async with the following try/except:                        
    try: 
        await asyncio.wait_for(newBlock(), timeout=5.0) 
    except asyncio.TimeoutError:
        await async.timeoutErr()
    """
    for counter in range(0,len(block.block_response.block.block_v1.payload.transactions)):
        """ 'async def newTransaction():' above is to incorporate the following content until the end of "for counter in range*", to be then called async with the following try/except:
        try: 
            await asyncio.wait_for(newTransaction(), timeout=5.0) 
        except asyncio.TimeoutError:
            await async.timeoutErr()
        """
        transaction = block.block_response.block.block_v1.payload.transactions.pop(counter).payload.reduced_payload.commands.pop()
        if transaction.HasField("set_account_detail") == True:
           #CASSANDRA SET ACCOUNT DETAIL TYPE OF TRANSACTION
           print("set_account_detail transaction inside!")
           transaction.set_account_detail.account_id #returns string
           transaction.set_account_detail.key #returns string
           transaction.set_account_detail.value #returns string
        if transaction.HasField("transfer_asset") == True:
           #CASSANDRA TRANSFER ASSET TYPE OF TRANSACTION
           print("transfer_asset transaction inside!")
           transaction.transfer_asset.src_account_id #returns string
           transaction.transfer_asset.dest_account_id #returns string
           transaction.transfer_asset.asset_id #returns string
           transaction.transfer_asset.description #returns string
           transaction.transfer_asset.amount #returns string
        """
        1. One IF for every transaction type of Iroha
        2. Each IF has to pass information to Apache Cassandra, corresponding to the Cassandra database design
        2.1 Some transactions may need several updates of Cassandra for the same information as this DB possibly stores the same information several times in different tables (which are differently designed); this refers to Apache Cassandra architecture and depends on the anticipated queries during the design phase
        3. If Cassandra had not returned success after the timeout, this has to be reported/handled (see timeoutErr above)
        """
    #If the file is tested/demonstrated with "python -i PyIroha.py", uncomment the following break:
    #break #This break starts python's interactive mode after the first processed block, which can then be used/tested. The first transaction will be already transferred to the "transaction" variable.

"""The following is to be uncommented when the above was incorporated into async def main() above (so, when all async*** are ready for testing)
asyncio.run(main())
"""
