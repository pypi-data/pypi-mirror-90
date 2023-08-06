import time
import sys
import os

import pkg_resources

import logging
import logging.handlers

from functools import lru_cache

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from collections import OrderedDict

from prettytable import PrettyTable
# import pprint

import requests
from requests.auth import HTTPDigestAuth


import json

DYNDCF_API_URL = 'https://192.168.2.1/rws/publicApi/v1/dcf'

UNIT_STR = ["V", "C", "Pa", "kPa", "%", "l/h", "bar", "Hz",
    "s", "ms", "min", "kW", "kWh", "J", "kJ", "",
    "m/s", "'", "h", "MWh", "MJ", "GJ", "W", "MW",
    "kJ/h", "MJ/h", "GJ/h", "ml", "l", "m3", "ml/h", "m3/h",
    "Wh", "?", "K", "", "lx", "t/min", "kvar", "kvarh",
    "mbar", "msg/m", "m", "kJ/kg", "g/kg", "ppm", "A", "kVA",
    "kVAh", "ohm"]


# import http.client as http_client
# http_client.HTTPConnection.debuglevel = 1


class MyLogger(object):
    def __init__(self, title="DynDCF"):
        self._title=title

    def create(self):
        return logging.getLogger(self._title)

    def tcp(self, level=logging.DEBUG, host='localhost'):
        logger=self.create()
        logger.setLevel(level)
        handler = logging.handlers.SocketHandler(host, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(handler)
        return logger

    def null(self):
        logger=self.create()
        logger.setLevel(logging.ERROR)
        handler=logging.NullHandler()
        logger.addHandler(handler)
        return logger


class DynDCFItemLabel(object):
    def __init__(self, item, label=None, low=None, normal=None, high=None):
        self._item=item
        self._label=label
        self._low=low
        self._normal=normal
        self._high=high

    @property
    def item(self):
        return self._item

    @property
    def key(self):
        return self.item.key

    @property
    def logger(self):
        return self.item.logger

    def signalChange(self):
        self.item.signalConfigTrigger()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if self._label != value:
            self._label=value
            self.signalChange()

    @property
    def low(self):
        return self._low

    @low.setter
    def low(self, value):
        if self._low != value:
            self._low=value
            self.signalChange()

    @property
    def normal(self):
        return self._normal

    @normal.setter
    def normal(self, value):
        if self._normal != value:
            self._normal=value
            self.signalChange()

    @property
    def high(self):
        return self._high

    @high.setter
    def high(self, value):
        if self._high != value:
            self._high=value
            self.signalChange()

    def match(self, key):
        if key is None:
            return False

        try:
            key=str(key).lower()
            if self.label and key in self.label.lower():
                return True
            # if self.low  and key in self.low:
                # return True
            # if self.normal and key in self.normal:
                # return True
            # if self.high and key in self.high:
                # return True
        except:
            pass

        return False

    def setLabel(self, label, low, normal, high):
        self.label=label
        self.low=low
        self.normal=normal
        self.high=high


class DynDCFItem(object):

    UNIT_DIGITAL = 15

    def __init__(self, parent, key, deltaTrigger, timeTrigger=60, inhibitTime=15, unit=None, refresh=None, decimals=1, tag=None, alias=None):
        # assert issubclass(parent.__class__, DynDCFItems)
        self._parent=parent
        self._key=key
        self._value=None
        self._lastValue=None
        self._unit=unit
        self._flags=None
        self._decimals=decimals
        self._tag=tag
        self._alias=alias
        self._stamp=0
        self._inhibitTime=inhibitTime
        self._timeoutInhibit=0
        self._trigger=False
        self._deltaTrigger=self.setDeltaTrigger(deltaTrigger)
        self._timeTrigger=self.setTimeTrigger(timeTrigger)
        self._timeoutRefresh=0
        self._onRefresh=refresh
        self._labels=DynDCFItemLabel(self)

    @property
    def logger(self):
        return self._parent.logger

    @property
    def parent(self):
        return self._parent

    @property
    def key(self):
        return self._key

    @property
    def tag(self):
        return self._tag

    @property
    def decimals(self):
        return self._decimals

    @decimals.setter
    def decimals(self, value):
        value=int(value)
        if self._decimals != value:
            self._decimals=value
            self.signalConfigTrigger()

    @tag.setter
    def tag(self, value):
        if self._tag != value:
            self._tag=value
            self.signalConfigTrigger()

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value):
        if self._alias != value:
            self._alias=value
            self.signalConfigTrigger()

    @property
    def labels(self):
        return self._labels

    def match(self, key):
        if key is None:
            return False

        try:
            key=str(key)
            if key in self.key:
                return True

        except:
            pass

        if self.labels.match(key):
            return True

        return False

    def onInit(self):
        pass

    def setInhibitTime(self, delay):
        self._inhibitTime=max(5, int(delay))

    def setInhibitNormal(self):
        self.setInhibitTime(15)

    desetInhibitTurbo(self):
        self.setInhibitTime(0)

    def registerRefresh(self, f):
        self._onRefresh=f

    def signalUpdated(self):
        self.stamp()
        self.manager()

    def setTimeTrigger(self, delay):
        if delay is None:
            self._timeTrigger=None
        else:
            self._timeTrigger=max(5, int(delay))
            if self._inhibitTime>self._timeTrigger:
                self._inhibitTime=self._timeTrigger
            self.trigger()

    def setDeltaTrigger(self, delta):
        if delta is None:
            self._deltaTrigger=None
        else:
            self._deltaTrigger=float(delta)
            self.trigger()

    def trigger(self):
        if not self._trigger and self._value is not None:
            self._trigger=True
            self.parent.signalTrigger(self)
            self._timeoutInhibit=time.time()+self._inhibitTime
            if self._onRefresh:
                try:
                    self._onRefresh(self)
                except:
                    pass

    def resetTrigger(self):
        self._trigger=False
        if self._value:
            self._lastValue=self._value

    def manager(self):
        if not self._trigger:
            t=time.time()
            if t>=self._timeoutInhibit:
                if self._deltaTrigger is not None:
                    try:
                        if self._value is not None:
                            if self._lastValue is None:
                                self.trigger()
                            elif abs(self._value-self._lastValue)>=self._deltaTrigger:
                                self.trigger()
                    except:
                        pass
                if self._timeTrigger and t>=self._timeoutRefresh:
                    self.trigger()
                    self._timeoutRefresh=time.time()+self._timeTrigger

    def signalConfigTrigger(self):
        self.parent.signalConfigTrigger(self)

    def stamp(self):
        self._stamp=time.time()

    def validateValue(self, value):
        try:
            if isinstance(value, bool):
                self.unit=self.UNIT_DIGITAL
                value=float(value)
            else:
                value=float(value)
                if self._unit==self.UNIT_DIGITAL:
                    if value:
                        value=1.0
            return value
        except:
            pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        value=self.validateValue(value)
        if value is not None:
            self.signalUpdated()
            if self._value!=value:
                self._value=value

    def on(self):
        self.value=1
        self.unit=self.UNIT_DIGITAL

    def off(self):
        self.value=0
        self.unit=self.UNIT_DIGITAL

    def toggle(self):
        if self.value:
            self.off()
        else:
            self.on()

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        if isinstance(unit, str):
            unit=self.getUnitFromStr(unit)
        if unit is not None:
            self.signalUpdated()
            if self._unit!=unit:
                self._unit=unit

    def unitstr(self):
        try:
            return UNIT_STR[self.unit]
        except:
            return ''

    @lru_cache()
    def getUnitFromStr(self, unit):
        try:
            unit=unit.lower()
            for n in range(len(UNIT_STR)):
                if unit==UNIT_STR[n].lower():
                    return n
        except:
            pass
        try:
            return UNIT_STR[int(unit)]
        except:
            pass

    def valuestr(self):
        if self.value is not None:
            unit=self.unit
            if unit in [self.UNIT_DIGITAL, 0xFF]:
                if self.value:
                    return 'ON'
                return 'OFF'
            return '%.01f%s' % (self.value, self.unitstr())
        return 'None'

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, flags):
        if flags is not None:
            self.signalUpdated()
            if self._flags!=flags:
                self._flags=flags

    def age(self):
        return time.time()-self._stamp

    def checkAge(self, maxAge):
        if self.age()<maxAge:
            return True
        return False

    def isAlive(self, maxAge=180):
        return self.checkAge(maxAge)

    def updateValue(self, value, unit, flags):
        self.value=value
        self.unit=unit
        self.flags=flags

    def syncConfig(self):
        self.logger.debug('Synchronizing config for item %s' % self.key)
        config={'tag': self.tag, 'alias': self.alias, 'dec': self.decimals}
        if self._labels:
            config['lblm']=self.labels.label
            config['lowm']=self.labels.low
            config['normalm']=self.labels.normal
            config['highm']=self.labels.high

        if config:
            r=self.doPUT('labels/%s' % self.key, data=json.dumps(config))
            if r:
                return True

        self.logger.error('Config sync for item %s' % self.key)
        return False

    def doGET(self, service, params=None, data=None):
        return self.parent.doGET(service, params, data)

    def doPUT(self, service, params=None, data=None):
        return self.parent.doPUT(service, params, data)

    def setLabel(self, label, low, normal, high):
        self.labels.setLabel(label, low, normal, high)

    def __repr__(self):
        return '<%s(%s, value=%s, age=%ds, trigger=%d)>' % (self.__class__.__name__,
            self.key,
            self.valuestr(), self.age(), self._trigger)


class DynDCFDigitalItem(DynDCFItem):
    def __init__(self, parent, key, timeTrigger=60, inhibitTime=15, refresh=None):
        super(DynDCFDigitalItem, self).__init__(parent, key, 0.5, timeTrigger, inhibitTime, unit=15, decimals=0, refresh=refresh)

    def setLabel(self, label, low, high):
        super(DynDCFDigitalItem, self).setLabel(label, low, None, high)


class DynDCFAnalogItem(DynDCFItem):
    pass


class DynDCFItems(object):
    def __init__(self, parent, inputs=True):
        assert isinstance(parent, DynDCF)
        self._parent=parent
        self._input=inputs
        self._items=[]
        self._itemsByKey={}
        self._triggers={}
        self._currentItem=0
        self._timeoutTrigger=0
        self._configTriggers=OrderedDict()
        self._timeoutConfigTrigger=0

    @property
    def parent(self):
        return self._parent

    @property
    def logger(self):
        return self._parent.logger

    def get(self, key):
        try:
            return self._itemsByKey[key]
        except:
            pass
        try:
            return self._items[int(key)]
        except:
            pass

    def add(self, item):
        assert isinstance(item, DynDCFItem)
        if not self.get(item.key):
            self._items.append(item)
            self._itemsByKey[item.key]=item
            self.logger.debug('adding item %s' % (item.key))
            self.onAdd(item)
            return item

    def onAdd(self, item):
        pass

    def signalTrigger(self, item):
        self._triggers[item.key]=item
        self.logger.info('triggering item %s' % item.key)

    def resetTrigger(self, item):
        try:
            self.logger.debug('reseting trigger for item %s' % item.key)
            item.resetTrigger()
            del self._triggers[item.key]
        except:
            pass

    def signalConfigTrigger(self, item):
        if item and not self._configTriggers.get(item.key, None):
            self.logger.debug('Queuing item %s for config sync...' % item.key)
            self._configTriggers[item.key]=item

    def popNextConfigTrigger(self):
        try:
            key=list(self._configTriggers.keys())[0]
            if key:
                item=self._configTriggers[key]
                del self._configTriggers[key]
                return item
        except:
            pass

    def all(self):
        return list(self._items)

    def count(self):
        return len(self._items)

    def __len__(self):
        return self.count()

    def __iter__(self):
        return iter(self.all())

    def __getitem__(self, key):
        return self.get(key)

    def sync(self, items):
        pass

    def manager(self):
        if self._items:
            try:
                n=32
                while n>0:
                    self._items[self._currentItem].manager()
                    self._currentItem+=1
                    n-=1
            except:
                self._currentItem=0

        if self._triggers and time.time()>=self._timeoutTrigger:
            try:
                # important to create a separate list
                # TODO: max
                maxcount=32
                self._timeoutTrigger=time.time()+1.0
                if not self.sync(list(self._triggers.values())[0:maxcount]):
                    self._timeoutTrigger=time.time()+5.0
            except:
                self.logger.exception('trigger()')
                self._timeoutTrigger=time.time()+15.0

        if time.time()>self._timeoutConfigTrigger:
            item=self.popNextConfigTrigger()
            if item:
                self._timeoutConfigTrigger=time.time()+2.0
                if not item.syncConfig():
                    # retrigger config update
                    self.signalConfigTrigger(item)

    def __repr__(self):
        return '<%s(%d items, %d triggers)>' % (self.__class__.__name__, self.count(), len(self._triggers))

    def digital(self, key, timeTrigger=60, inhibitTime=15, refresh=None):
        item=self.get(key)
        if not item:
            item=DynDCFDigitalItem(self, key, timeTrigger, inhibitTime, refresh=refresh)
            self.add(item)
        return item

    def analog(self, key, deltaTrigger=None, timeTrigger=60, inhibitTime=15, refresh=None):
        item=self.get(key)
        if not item:
            item=DynDCFAnalogItem(self, key, deltaTrigger, timeTrigger, inhibitTime, refresh=None)
            self.add(item)
        return item

    def doGET(self, service, params=None, data=None):
        return self.parent.doGET(service, params, data)

    def doPUT(self, service, params=None, data=None):
        return self.parent.doPUT(service, params, data)

    def table(self, key=None):
        self.manager()
        if self._items:
            empty=True
            t=PrettyTable()
            t.field_names = ['#', 'key', 'value', 'unit', 'tags', 'age', 'trigger', 'label']
            t.align['#']='l'
            t.align['key']='l'
            t.align['value']='r'
            t.align['unit']='l'
            t.align['flags']='l'
            t.align['age']='l'
            t.align['trigger']='l'
            t.align['label']='l'

            now=time.time()

            n=0
            for item in self.all():
                if key and not item.match(key):
                    pass
                else:
                    age='%.01fs' % item.age()
                    trigger=''
                    if item._trigger:
                        trigger='YES'
                    elif time.time()<item._timeoutInhibit:
                        trigger='X'
                    else:
                        trigger=''
                        if item._timeoutRefresh:
                            trigger+='%ds' % (item._timeoutRefresh-now)
                    label=''
                    if item.labels.label:
                        label=item.labels.label
                    t.add_row([n, item.key, item.valuestr(), item.unit, item.flags, age, trigger, label])
                    empty=False
                n+=1

            if not empty:
                print(t)


class DynDCFInputs(DynDCFItems):
    """Client->DYN (=upload or WRITE or PUSH)"""

    def sync(self, items):
        values=[]
        for item in items:
            self.resetTrigger(item)
            if item.isAlive(180):
                data={'key': item.key}
                if item.value is not None:
                    data['value']=item.value
                if item.unit is not None:
                    data['unit']=item.unit
                if item.flags is not None:
                    data['flags']=item.flags
                values.append(data)
            else:
                self.logger.error('ignoring upload of dead item %s' % item.key)

        if values:
            r=self.doPUT('states', data=json.dumps(values))
            if r:
                return True

    def din(self, key, timeTrigger=60, inhibitTime=15, refresh=None):
        return self.digital(key, timeTrigger, inhibitTime, refresh=None)

    def ain(self, key, timeTrigger=60, inhibitTime=15, refresh=None):
        return self.analog(key, deltaTrigger=None, timeTrigger=timeTrigger, inhibitTime=inhibitTime, refresh=refresh)

    def __repr__(self):
        return '<%s(%d inputs, %d triggers)>' % (self.__class__.__name__, self.count(), len(self._triggers))


class DynDCFOutputs(DynDCFItems):
    """DYN->Client (=download or READ or PULL)"""

    def sync(self, items):
        result=True

        keys=[]
        for item in items:
            keys.append(item.key)
            self.resetTrigger(item)

        data={'keys': ','.join(keys), 'select': 'state'}

        # TODO: retirer params
        # r=self.doGET('states', data=json.dumps(data))
        r=self.doGET('states', params=data)
        if r:
            for state in r:
                try:
                    item=self.get(state['key'])
                    if 'error' in state:
                        msg=state['error']
                        if 'key' in state:
                            msg += '/%s' % state['key']
                        self.logger.error(msg)
                        result=False
                    else:
                        item=self.get(state['key'])
                        if item:
                            item.unit=state['unitCode']
                            item.value=state['value']
                            item.flags=state['flags']
                except:
                    result=False
                    self.logger.exception('sync()')
        return result

    def dout(self, key, timeTrigger=60, inhibitTime=15, refresh=None):
        return self.digital(key, timeTrigger, inhibitTime, refresh=refresh)

    def aout(self, key, deltaTrigger=None, timeTrigger=60, inhibitTime=15, refresh=None):
        return self.analog(key, deltaTrigger, timeTrigger, inhibitTime, refresh=refresh)

    def __repr__(self):
        return '<%s(%d outputs, %d triggers)>' % (self.__class__.__name__, self.count(), len(self._triggers))


class DynDCF(object):
    def __init__(self, url, user, password, timeout=5.0, logger=None):
        if logger is None:
            logger=MyLogger().tcp()

        self._url=url or DYNDCF_API_URL
        self._user=user
        self._auth=HTTPDigestAuth(user, password.upper())
        self._timeout=int(timeout)

        self._inputs=DynDCFInputs(self)
        self._outputs=DynDCFOutputs(self)

        self._timeoutInhibit=0
        self._logger=logger

    @property
    def inputs(self):
        """return the DynDCF inputs (client->DynDCF values)"""
        return self._inputs

    @property
    def outputs(self):
        """return the DynDCF outputs (DynDCF->client values)"""
        return self._outputs

    def getVersion(self):
        try:
            distribution=pkg_resources.get_distribution('digimat.dyndcf')
            return distribution.parsed_version
        except:
            pass

    @property
    def version(self):
        return self.getVersion()

    @property
    def logger(self):
        return self._logger

    def url(self, service):
        return '%s/%s' % (self._url, service)

    def doGET(self, service, params=None, data=None):
        try:
            url=self.url(service)
            self.logger.debug('GET(%s) config=%s data=%s' % (url, params, data))
            r=requests.get(url, auth=self._auth, verify=False,
                params=params, data=data, timeout=self._timeout)
            if r and r.ok:
                return r.json()
            self.logger.error('doGET(%s/%d)' % (url, r.status_code))
        except:
            self.logger.exception('doGET(%s)' % service)

    def doPUT(self, service, params=None, data=None):
        try:
            url=self.url(service)
            self.logger.debug('PUT(%s) config=%s data=%s' % (url, params, data))
            r=requests.put(url, auth=self._auth, verify=False,
                params=params, data=data, timeout=self._timeout)
            if r and r.ok:
                return True
            self.logger.error('doPUT(%s)' % (url))
        except:
            self.logger.exception('doPUT(%s)' % service)

    def din(self, key, timeTrigger=60, inhibitTime=15, refresh=None):
        """create/retrieve an item providing a digital value from the external client to the DynDCF server"""
        return self.inputs.digital(key, timeTrigger=timeTrigger,
            inhibitTime=inhibitTime, refresh=refresh)

    def ain(self, key, timeTrigger=60, inhibitTime=15, refresh=None):
        """create/retrieve an item providing an analog value from the external client to the DynDCF server"""
        return self.inputs.analog(key, timeTrigger=timeTrigger,
            inhibitTime=inhibitTime, refresh=refresh)

    def dout(self, key, timeTrigger=60, inhibitTime=15, refresh=None):
        """create/retrieve an item providing a digital value from the DynDCF server to the external client"""
        return self.outputs.digital(key, timeTrigger=timeTrigger,
            inhibitTime=inhibitTime, refresh=refresh)

    def aout(self, key, deltaTrigger=None, timeTrigger=60, inhibitTime=15, refresh=None):
        """create/retrieve an item providing an analog value from the DynDCF server to the external client"""
        return self.outputs.analog(key, deltaTrigger=deltaTrigger, timeTrigger=timeTrigger,
            inhibitTime=inhibitTime, refresh=refresh)

    def get(self, key):
        """retrieve an item by it's key"""
        item=self.inputs.get(key)
        if not item:
            item=self.outputs.get(key)
        return item

    def __getitem__(self, key):
        return self.get(key)

    def manager(self):
        if time.time()>=self._timeoutInhibit:
            self._inputs.manager()
            self._outputs.manager()
            self._timeoutInhibit=time.time()+0.2

    def dump(self):
        # TODO:
        pass

    def isInteractiveMode(self):
        try:
            if sys.ps1:
                interpreter = True
        except AttributeError:
            interpreter = False
            if sys.flags.interactive:
                interpreter = True
        try:
            if os.path.basename(sys.argv[0])=='bpython':
                interpreter=True
        except:
            pass

        return interpreter

    def __repr__(self):
        # WARNING: absolutely not Python but so useful ;)
        if self.isInteractiveMode():
            self.manager()
        return '<%s(%d inputs, %d outputs)>' % (self.__class__.__name__,
            self._inputs.count(), self._outputs.count())

    def table(self, key=None):
        self.inputs.table(key)
        self.outputs.table(key)

    def run(self, maxTime=0):
        try:
            self.logger.info('entering run loop (%ds)' % maxTime)
            timeout=time.time()+maxTime
            while maxTime==0 or time.time()<timeout:
                self.manager()
                time.sleep(.2)
        except KeyboardInterrupt:
            pass
        self.logger.info('leaving run loop')


if __name__ == "__main__":
    pass
