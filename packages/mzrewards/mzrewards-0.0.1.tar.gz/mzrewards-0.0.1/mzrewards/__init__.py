import os
import sys
import json
from algosdk.future import transaction
from algosdk import account
from algosdk.v2client import *
from pyteal import *
import base64
import json
import secrets
import hashlib


def network_client():
    try:
        algod_address = 'https://testnet-algorand.api.purestake.io/ps2/'
        algod_token = 'VzZDSA0GmX3p9YpIbryAe8Wtif6VWNUp4CQaV6NG'
        headers = {
        "X-API-Key": algod_token,
        }
        algod_client = algod.AlgodClient(algod_token, algod_address, headers)
        return algod_client
    except Exception as e:
        raise Exception(e)

def Create_ASA_TXN(algod_client,private_key,total,assetname,unitname,decimals):
    try:
        # algod_client = network_client()
        # private_key = parser.get('ALGOD_test_params', 'private_key')
        address = account.address_from_private_key(private_key)
        params = algod_client.suggested_params()
        gh, first_valid_round, last_valid_round = params.gh, params.first, params.last
        fee = 1000
        sp = transaction.SuggestedParams(fee, first_valid_round,last_valid_round,gh)
        # get last block info
        block_info = algod_client.block_info(sp.first)
        # print("Block", sp.first, "info:", json.dumps(block_info, indent=2), "\n")
        assetid = block_info["block"]["tc"]+1
        #metadata = bytes("fACPO4nRgO55j1ndAK3W6Sgc4APkcyFa", "ascii") # should be a 32-byte hash
    
        txn,err = transaction.AssetConfigTxn(address, sp, total=total, manager=address,
                    reserve=address, freeze=address, clawback=address,
                    unit_name=unitname, asset_name=assetname,decimals=decimals,
                    default_frozen=False),None
        signed = txn.sign(private_key)
        txid = algod_client.send_transaction(signed)
        return txid, err, assetid
    except Exception as e:
        txid, err = e, e
        assetid = None
        return txid, err, assetid

def Clawback_ASA_TXN(algod_client,claw_addr_pkey,target_address,receiver_address,amount,assetid):
    try:
        # algod_client = network_client()
        clawback_address = account.address_from_private_key(claw_addr_pkey)
        params = algod_client.suggested_params()
        gh, first_valid_round, last_valid_round = params.gh, params.first, params.last
        fee = 1000
        sp = transaction.SuggestedParams(fee, first_valid_round,last_valid_round,gh)
        txn, err = transaction.AssetTransferTxn(clawback_address, sp,
                receiver_address, amount, assetid, revocation_target=target_address), None
        signed = txn.sign(claw_addr_pkey)
        txid = algod_client.send_transaction(signed)
        return txid, err
    except Exception as e:
        txid, err = e, e
        return txid, err

def Destroy_ASA_TXN(algod_client, private_key, assetid):
    try:
        # algod_client = network_client()
        creator_address = account.address_from_private_key(private_key)
        params = algod_client.suggested_params()
        gh, first_valid_round, last_valid_round = params.gh, params.first, params.last
        fee = 1000
        sp = transaction.SuggestedParams(fee, first_valid_round,last_valid_round,gh)
        txn, err = transaction.AssetConfigTxn(creator_address, sp, index=assetid, strict_empty_address_check=False), None
        signed = txn.sign(private_key)
        txid = algod_client.send_transaction(signed)
        return txid, err
    except Exception as e:
        txid, err = e, e
        return txid, err

def Freeze_ASA_TXN(algod_client,frze_addr_pkey,target_address,assetid,freeze_state):
    try:
        # algod_client = network_client()
        freeze_address = account.address_from_private_key(frze_addr_pkey)
        params = algod_client.suggested_params()
        gh, first_valid_round, last_valid_round = params.gh, params.first, params.last
        fee = 1000
        sp = transaction.SuggestedParams(fee, first_valid_round,last_valid_round,gh)
        txn = transaction.AssetFreezeTxn(freeze_address, sp, index=assetid, target=target_address,
                        new_freeze_state=freeze_state)
        err = None
        signed = txn.sign(frze_addr_pkey)
        txid = algod_client.send_transaction(signed)
        return txid, err
    except Exception as e :
        txid, err = e, e
        return txid, err

def Optin_ASA_TXN(algod_client,private_key,assetid):
    try:
        # algod_client = network_client()
        address = account.address_from_private_key(private_key)
        params = algod_client.suggested_params()
        gh, first_valid_round, last_valid_round = params.gh, params.first, params.last
        fee = 1000
        sp = transaction.SuggestedParams(fee, first_valid_round,last_valid_round,gh)
        receiver_address = address
        amount = 0
        txn = transaction.AssetTransferTxn(address, sp,
                receiver_address, amount, assetid)
        err = None
        signed = txn.sign(private_key)
        txid = algod_client.send_transaction(signed)
        return txid, err
    except Exception as e:
        txid, err = e, e
        return txid, err

def Send_ASA_TXN(algod_client,sender_private_key,receiver_address,amount, assetid):
    try:
        # algod_client = network_client()
        sender_address = account.address_from_private_key(sender_private_key)
        params = algod_client.suggested_params()
        gh, first_valid_round, last_valid_round = params.gh, params.first, params.last
        fee = 1000
        sp = transaction.SuggestedParams(fee, first_valid_round,last_valid_round,gh)
        txn = transaction.AssetTransferTxn(sender_address, sp,
                receiver_address, amount, assetid)
        err = None
        signed = txn.sign(sender_private_key)
        txid = algod_client.send_transaction(signed)
        return txid, err
    except Exception as e:
        txn, err = e, e
        return txn, err

def Update_ASA_TXN(algod_client,mngr_addr_pkey,assetid, **kwargs):
    try:
        # algod_client = network_client()
        manager_address = account.address_from_private_key(mngr_addr_pkey)
        params = algod_client.suggested_params()
        gh, first_valid_round, last_valid_round = params.gh, params.first, params.last
        fee = 1000
        sp = transaction.SuggestedParams(fee, first_valid_round,last_valid_round,gh)
        new_manager = kwargs.get('manager',None)
        new_reserve = kwargs.get('reserve',None)
        new_freeze = kwargs.get('freeze',None)
        new_clawback = kwargs.get('clawback',None)
        txn,err = transaction.AssetConfigTxn(manager_address, sp, manager=new_manager, reserve=new_reserve,
            freeze=new_freeze, clawback=new_clawback, index=assetid,strict_empty_address_check=False), None
        signed = txn.sign(mngr_addr_pkey)
        txid = algod_client.send_transaction(signed)
        return txid, err
    except Exception as e:
        txid, err = e, e
        return txid, err

def txnaction(algod_client, private_key):
    try:
        addr = account.address_from_private_key(private_key)
        params = algod_client.suggested_params()
        gh, first_valid_round, last_valid_round = params.gh, params.first, params.last
        fee = 1000
        secret = base64.b64encode(os.urandom(32)).decode('ascii')
        lease = base64.b64decode(secret)
        sp = transaction.SuggestedParams(fee, first_valid_round,last_valid_round,gh)
        txn = transaction.Transaction(addr,sp,None,lease,"pay",None)
        return txn
    except Exception as e:
        raise Exception(e)

def sl_argsdeploy(algod_client,private_key,byte_string,values):
    try:
        base64_bytes = byte_string.encode("ascii") 
        string_bytes = base64.b64decode(base64_bytes)
        txn = txnaction(algod_client,private_key)
        lsig = transaction.LogicSig(string_bytes,args=values)
        lsig.sign(private_key)
        lstx = transaction.LogicSigTransaction(txn, lsig)
        txid = algod_client.send_transaction(lstx)
        print("Transaction ID: " + txid)
        return txid
    except Exception as e:
        raise Exception(e)

def sample():
    print("hello world")