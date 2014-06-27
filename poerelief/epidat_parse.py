# encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#from lxml import etree
#from io import StringIO, BytesIO
from loc import loc
from types import *
#import xmltodict
import untangle
import datetime
# Temporär JS code der abfragt  returns one json array  refreshes every so often‘’ or so

#Frage an Thomas - Warum <p> tags in xml?? vorgesehen in epidat?

#from lxml import objectify

# Fixed baseurl for SI epidat records
baseurl = "http://steinheim-institut.de/cgi-bin/epidat?id="
# The seperator
s = "-"
# specifies the format
format = "teip5"
# afaik records always start at 1
id = 1
# Fixed location for testing
#loc = "aha"


class Record(object):
  def __init__(self):
    self.id = 0
    self.loc = ""
    self.url = ""
    #self.expr = ""
    self.licence = ""
    self.title = ""
    self.urld = ""
    self.date = ""
    self.insc = ""
    self.material = ""
    self.condition = ""
    self.decoration = ""
    self.geoname = ""
    self.geotype = ""
    self.geocountry = ""
    self.georegion = ""
    self.geocoord = ""
    self.images = []
    self.idd = ""
    self.sex = ""
    self.pname = ""
    self.deathdate = ""
    self.edition = ""
    self.verso = ""
    self.recto = ""
    self.translation = ""
    self.linecomm = []
    self.endcomm = ""
    self.proso = ""
    self.bibliography = ""

#This gets a record from supplied id + loc

  def getRecord(self, url):
    self.url = url
    rec = untangle.parse(url)
    return rec

  def pEvalRecord(self, record):
    #availability #licencename #licencelink
    self.licence = [record.TEI.teiHeader.fileDesc.publicationStmt.availability['status'], record.TEI.teiHeader.fileDesc.publicationStmt.availability.licence.ref.cdata, record.TEI.teiHeader.fileDesc.publicationStmt.availability.licence.ref['target']]
    self.title = record.TEI.teiHeader.fileDesc.titleStmt.title.cdata
    self.urld = record.TEI.teiHeader.fileDesc.publicationStmt.idno[1].cdata
    #date
    try:
      record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.history.origin.date
    except IndexError:
      "IndexError was raised for date"
      self.date = None
    else:
      self.date = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.history.origin.date['notBefore']
    #insc
    self.insc = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.objectDesc.supportDesc.support.p.cdata
    #material
    self.material = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.objectDesc.supportDesc.support.p.material.cdata
    #condition
    try:
      record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.objectDesc.supportDesc.condition
    except IndexError:
      print "Index Error was raised for condition"
      self.condition = None
    else:
      if type(record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.objectDesc.supportDesc.condition.p) is ListType:
        self.condition = list(self.condition)
        for p in record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.objectDesc.supportDesc.condition.p:
          self.condition.append(p)
      else:
        self.condition = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.objectDesc.supportDesc.condition.p.cdata
    #Decodescription #Decotype
    try:
      record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.decoDesc.decoNote
    except IndexError:
      print "Index Error was raised for decotype"
      self.decoration = None
    else:
      self.decoration = [record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.decoDesc.decoNote.cdata, record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.physDesc.decoDesc.decoNote['type']]
    #Geoname
    self.geoname = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.history.origin.settlement.geogName.cdata
    self.geotype = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.history.origin.settlement['type']
    #return type, name
    self.geocountry = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.history.origin.country.cdata
    self.georegion = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.history.origin.country.region.cdata
    self.geocoord = record.TEI.teiHeader.fileDesc.sourceDesc.msDesc.history.origin.settlement.geogName.geo.cdata
    # Graphics
    #FIXME[1] ... check with len or so how many ... url with r.TEI.facsimile.graphic[0]['url'] + add recto verso stuff etc
    try:
      record.TEI.facsimile.graphic
    except IndexError:
      print "IndexError was raised for graphic"
      self.images = None
    else:
      self.images = record.TEI.facsimile.graphic[0]
    # add stuff about authors, etc r.TEI.teiHeader.encodingDesc.classDecl.taxonomy.category ff
    self.idd = record.TEI.teiHeader.fileDesc.publicationStmt.idno[0].cdata
    #sex
    try:
      record.TEI.teiHeader.profileDesc.particDesc
    except IndexError:
      print "IndexError was raised for particDesc + person + sex"
      self.sex = None
    else:
      if type(record.TEI.teiHeader.profileDesc.particDesc.listPerson.person) is ListType:
        self.sex = list(self.condition)
        for s in record.TEI.teiHeader.profileDesc.particDesc.listPerson.person:
          self.sex.append(s['sex'])
      else:
        self.sex = record.TEI.teiHeader.profileDesc.particDesc.listPerson.person['sex'] #1 is male
    #person name
    try:
      record.TEI.teiHeader.profileDesc.particDesc
    except IndexError:
      print "Index Error was raised for particDesc + person + name"
      self.pname = None
    else:
      if type(record.TEI.teiHeader.profileDesc.particDesc.listPerson.person) is ListType:
        self.pname = list(self.pname)
        for p in record.TEI.teiHeader.profileDesc.particDesc.listPerson.person:
          self.pname.append(p.persName.cdata)
      else:
        self.pname = record.TEI.teiHeader.profileDesc.particDesc.listPerson.person.persName.cdata #maybe as list with id if more than one??
    #deathdate
    try:
      record.TEI.teiHeader.profileDesc.particDesc.listPerson.person
    except IndexError:
      print "IndexError was raised for deathdate"
    else:
      if type(record.TEI.teiHeader.profileDesc.particDesc.listPerson.person) is ListType:
        self.deathdate = list(self.deathdate)
        for d in record.TEI.teiHeader.profileDesc.particDesc.listPerson.person:
          if d.event['type'] == "dateofdeath":
            self.deathdate.append(d.event['when'])
      else:
        if record.TEI.teiHeader.profileDesc.particDesc.listPerson.person.event['type'] == "dateofdeath":
          self.deathdate = record.TEI.teiHeader.profileDesc.particDesc.listPerson.person.event['when']
    #edition
    self.edition = record.TEI.text.body.div[0].head.cdata
    #verso
    try:
      record.TEI.text.body.div[0].div
    except IndexError:
      print "IndexError was raised for verso"
      self.verso = None
    else:
      self.verso = record.TEI.text.body.div[0].div[0].ab.cdata
    #recto
    try:
      record.TEI.text.body.div[0].div
    except IndexError:
      print "IndexError was raised for recto"
      self.recto = None
    else:
      self.recto = record.TEI.text.body.div[0].div[1].ab.cdata
    #translation
    try:
      record.TEI.text.body.div[1].div
    except IndexError:
      print "IndexError was raised for translation"
      self.translation = None
    else:
      try:
        record.TEI.text.body.div[1].div.ab
      except AttributeError:
        print "IndexError was raised for translation-ab"
        self.translation = record.TEI.text.body.div[1].div
      else:
        self.translation = record.TEI.text.body.div[1].div.ab.cdata
    #linecomm
    try:
      record.TEI.text.body.div[2]
    except IndexError:
      print "Index Error was raised for linecomm"
      self.linecomm = None
    else:
      try:
        record.TEI.text.body.div[2].p
      except IndexError:
        print "IndexError was raised for linecomm p"
        self.linecomm = record.TEI.text.body.div[2]
      else:
        # head bis ende? cdata anhängen? zzt mit <p> als list
        for i in record.TEI.text.body.div[2].p:
          if type(i) != NoneType:
            self.linecomm.append(i.cdata)
          else:
            pass
    #endcomm
    try:
      record.TEI.text.body.div[3]
    except IndexError:
      print "IndexError was raised for endcomm"
      self.endcomm = None
    else:
      #self.endcomm = record.TEI.text.body.div[3].p
      try:
        record.TEI.text.body.div[3].p
      except IndexError:
        print "IndexError was raised for part of endcomm"
        self.endcomm = record.TEI.text.body.div
      else:
        self.endcomm = record.TEI.text.body.div[3].p
    #proso
    try:
      record.TEI.text.body.div[4]
    except IndexError:
      print "IndexError was raised for proso"
      self.proso = None
    else:
      self.proso = record.TEI.text.body.div[4].p
    #bibliography
    try:
      record.TEI.text.body.div[5]
    except IndexError:
      print "IndexError was raised for bibliography"
      self.bibliography = None
    else:
      self.bibliography = record.TEI.text.body.div[5] # if list, for p in l ... cdata
    return 0

# format data as json

  def toJSON(self, record):
    #use lib for that
    ret = "title:" + self.title + "," "urld:" + self.urld +"," + "date:" + self.date + "," + "pname:" + self.pname + "," + "translation:" + self.translation
    return ret
