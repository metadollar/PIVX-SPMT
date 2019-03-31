#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.Qt import QObject
from PyQt5.QtCore import pyqtSignal

from constants import HW_devices
from ledgerClient import LedgerApi

class HWdevice(QObject):
    # signal: sig1 (thread) is done - emitted by signMessageFinish
    sig1done = pyqtSignal(str)
    # signal: sigtx (thread) is done - emitted by signTxFinish
    sigTxdone = pyqtSignal(bytearray, str)
    # signal: sigtx (thread) is done (aborted) - emitted by signTxFinish
    sigTxabort = pyqtSignal()
    # signal: tx_progress percent - emitted by perepare_transfer_tx_bulk
    tx_progress = pyqtSignal(int)
    # signal: sig_progress percent - emitted by signTxSign
    sig_progress = pyqtSignal(int)
    # signal: sig_disconnected -emitted with DisconnectedException
    sig_disconnected = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.status = 0

    def initDevice(self, hw_index):
        print("Not even here?")
        if hw_index >= len(HW_devices):
            raise Exception("Invalid HW index")

        # Select API
        if hw_index == 0:
            self.api = LedgerApi()
        else:
            raise Exception("Invalid index!")
            #self.api = TrezorApi()

        # Init device & connect signals
        print("About to...")
        self.api.initDevice()
        self.sig1done = self.api.sig1done
        self.sigTxdone = self.api.sigTxdone
        self.sigTxabort = self.api.sigTxabort
        self.tx_progress = self.api.tx_progress
        self.sig_progress = self.api.sig_progress
        self.sig_disconnected = self.api.sig_disconnected



    def clearDevice(self, message=''):
        self.status = 0
        self.api.clearDevice(message)



    def getStatus(self):
        return self.api.getStatus()



    def append_inputs_to_TX(self, utxo, bip32_path):
        self.api.append_inputs_to_TX(utxo, bip32_path)



    def prepare_transfer_tx(self, caller, bip32_path,  utxos_to_spend, dest_address, tx_fee, useSwiftX=False):
        self.api.prepare_transfer_tx(caller, bip32_path,  utxos_to_spend, dest_address, tx_fee, useSwiftX)



    def prepare_transfer_tx_bulk(self, caller, rewardsArray, dest_address, tx_fee, useSwiftX=False):
        self.api.prepare_transfer_tx_bulk(caller, rewardsArray, dest_address, tx_fee, useSwiftX)



    def scanForAddress(self, account, spath, isTestnet=False):
        return self.api.scanForAddress(account, spath, isTestnet)



    def scanForBip32(self, account, address, starting_spath=0, spath_count=10, isTestnet=False):
        return self.api.scanForBip32(account, address, starting_spath, spath_count, isTestnet)



    def scanForPubKey(self, account, spath):
        return self.api.scanForPubKey(account, spath)



    def signMess(self, caller, path, message):
        self.api.signMess(caller, path, message)



    def signMessageSign(self, ctrl):
        self.api.signMessageSign(ctrl)



    def signMessageFinish(self):
        self.api.signMessageFinish()



    def signTxSign(self, ctrl):
        self.api.signTxSign(ctrl)



    def signTxFinish(self):
        self.api.signTxFinish()



    def updateSigProgress(self, percent):
        self.api.updateSigProgress(percent)
