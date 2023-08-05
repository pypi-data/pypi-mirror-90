# AUTOGENERATED! DO NOT EDIT! File to edit: Helpers.ipynb (unless otherwise specified).

__all__ = ['Helpers', 'notify', 'keys', 'scanDb', 'toDf', 'fromSeries', 'fromDf', 'fromDict', 'toListDict', 'toSeries',
           'setNoUpdate', 'setUpdate']

# Cell
from nicHelper.wrappers import add_method, add_class_method, add_static_method
from nicHelper.dictUtil import stripDict
from linesdk.linesdk import Line
from typing import List
import pandas as pd
import os, logging



# Cell
class Helpers:
  pass

# Cell
@add_static_method(Helpers)
def notify(message):
  line = Line(os.environ.get('LINEKEY'))
  r = line.sendNotify(message)
  if r.status_code != 200:
    print(r.json())
    return False
  return True

# Cell
@add_class_method(Helpers)
def keys(cls):
  keys = list(vars(cls)['_attributes'].keys())
  return keys

# Cell
@add_class_method(Helpers)
def scanDb(cls, limit=100):
  return list(cls.scan(limit=limit))

# Cell
@add_class_method(Helpers)
def toDf(cls, products:List[Helpers])->pd.DataFrame:
  df = pd.DataFrame()
  for product in products:
    productSeries = product.toSeries()
    productSeries = productSeries.rename(product.cprcode)
    df = df.append(productSeries)
  return df

# Cell
@add_class_method(Helpers)
def fromSeries(cls, data:pd.Series)->Helpers:
  return cls.fromDict(data.to_dict())


# Cell
@add_class_method(Helpers)
def fromDf(cls, data:pd.DataFrame)->List[Helpers]:
  return data.apply(lambda x: cls.fromSeries(x), axis=1).to_list()


# Cell
@add_class_method(Helpers)
def fromDict(cls, dictInput):
  logging.debug(dictInput)
  dictInput = stripDict(dictInput)
  #### extract the keys
  filteredInput = {k:v for k,v in dictInput.items() if k in cls.keys()}
  #### save whole object to dictInput
  filteredInput['data'] = dictInput
  logging.debug(filteredInput)
  return cls(**filteredInput)

# Cell
@add_class_method(Helpers)
def toListDict(cls, items:List[Helpers]):
  return [item.data for item in items]

# Cell
@add_method(Helpers)
def toSeries(self):
  return pd.Series(self.data)

# Cell
@add_method(Helpers)
def setNoUpdate(self, batch = None):
  self.needsUpdate = self.FALSE
  if batch:
    return batch.save(self)
  else:
    return self.save()

@add_method(Helpers)
def setUpdate(self, batch=None):
  self.needsUpdate = self.TRUE
  if batch:
    return batch.save(self)
  else:
    return self.save()