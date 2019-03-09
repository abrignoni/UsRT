import xml.etree.ElementTree as ET
import glob, os, sqlite3, os, sys, re, json

class parsefile(object):

    def __init__(self, filename, db):
        self.filename = filename
        self.db = db

    def parse_usagestats_file(self):
        if 'version' in self.filename:
            return None
        else:
            try:
                if 'daily' in self.filename:
                    sourced = 'daily'
                elif 'weekly' in self.filename:
                    sourced = 'weekly'
                elif 'monthly' in self.filename:
                    sourced = 'monthly'
                elif 'yearly' in self.filename:
                    sourced = 'yearly'
                file_name_int = int(self.filename.split("\\")[-1])
                tree = ET.parse(self.filename)
                root = tree.getroot()
                for elem in root:
                    usagetype = elem.tag
                    if usagetype == 'packages':
                        for subelem in elem:
                            fullatti_str = json.dumps(subelem.attrib)
                            time1 = int(subelem.attrib['lastTimeActive'])
                            if time1 < 0:
                                finalt = abs(time1)
                            else:
                                finalt = file_name_int + time1
                                pkg = (subelem.attrib['package'])
                                tac = (subelem.attrib['timeActive'])
                            datainsert = (usagetype, finalt, tac, pkg, '' , '' , sourced, fullatti_str,)
                            self.db.cursor().execute('INSERT INTO data (usage_type, lastime, timeactive, package, types, classs, source, fullatt)  VALUES(?,?,?,?,?,?,?,?)', datainsert)
                            self.db.commit()
                    elif usagetype == 'configurations':
                        for subelem in elem:
                            fullatti_str = json.dumps(subelem.attrib)
                            time1 = int(subelem.attrib['lastTimeActive'])
                            if time1 < 0:
                                finalt = abs(time1)
                            else:
                                finalt = file_name_int + time1
                            tac = (subelem.attrib['timeActive'])
                            datainsert = (usagetype, finalt, tac, '' , '' , '' , sourced, fullatti_str,)
                            self.db.cursor().execute('INSERT INTO data (usage_type, lastime, timeactive, package, types, classs, source, fullatt)  VALUES(?,?,?,?,?,?,?,?)', datainsert)
                            self.db.commit()
                    elif usagetype == 'event-log':
                        for subelem in elem:
                            time1 = int(subelem.attrib['time'])
                            if time1 < 0:
                                finalt = abs(time1)
                            else:
                                finalt = file_name_int + time1
                            pkg = (subelem.attrib['package'])
                            tipes = (subelem.attrib['type'])
                            fullatti_str = json.dumps(subelem.attrib)
                            if 'class' in subelem.attrib:
                                classy = subelem.attrib['class']
                                datainsert = (usagetype, finalt, '' , pkg , tipes , classy , sourced, fullatti_str,)
                                self.db.cursor().execute('INSERT INTO data (usage_type, lastime, timeactive, package, types, classs, source, fullatt)  VALUES(?,?,?,?,?,?,?,?)', datainsert)
                                self.db.commit()
                            else:
                                datainsert = (usagetype, finalt, '' , pkg , tipes , '' , sourced, fullatti_str,)
                                self.db.cursor().execute('INSERT INTO data (usage_type, lastime, timeactive, package, types, classs, source, fullatt)  VALUES(?,?,?,?,?,?,?,?)', datainsert)
                                self.db.commit()

            except: pass
