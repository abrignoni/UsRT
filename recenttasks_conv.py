import xml.etree.ElementTree as ET
import glob, os, sqlite3, os, sys, re, json, shutil

class datatoparse(object):

	def __init__(self, filename, db, current_dir,folder):
		self.filename = filename
		self.db = db
		self.current_dir = current_dir
		self.validfile = True
		self.images_folder = folder


	def parse_recenttask_file(self):
		try:
			directory = self.filename.rsplit("/",1)[0]
			tree = ET.parse(self.filename)
			root = tree.getroot()
		except:
			self.validfile = False

		if self.validfile == True:
			for child in root:
				fullat1 = json.dumps(root.attrib)
				task_id = root.attrib.get('task_id')
				effective_uid = (root.attrib.get('effective_uid'))
				affinity = (root.attrib.get('affinity'))
				real_activity = (root.attrib.get('real_activity'))
				first_active_time = (root.attrib.get('first_active_time'))
				last_active_time = (root.attrib.get('last_active_time'))
				last_time_moved = (root.attrib.get('last_time_moved'))
				calling_package = (root.attrib.get('calling_package'))
				user_id = (root.attrib.get('user_id'))
				fullat2 = json.dumps(child.attrib)
				action = (child.attrib.get('action'))
				component = (child.attrib.get('component'))
				icon_image_path = (root.attrib.get('task_description_icon_filename'))
				snapshot = task_id + '.jpg'

				check1 = directory + '\\snapshots\\' + snapshot
				isit1 = os.path.isfile(check1)
				if isit1:
					shutil.copy(check1,self.images_folder)
					name = check1.rsplit('\\',1)[1]
					snap = f'{self.images_folder}\{name}'

				else:
					snap = 'No Image'

				if icon_image_path != None:
					recent_image = os.path.basename(icon_image_path)
					recimg = directory + '\\recent_images\\'+recent_image
					shutil.copy(recimg,self.images_folder)
					recimg = f'{self.images_folder}\{recent_image}'


				else:
					thumbnail = glob.glob(directory + '\\recent_images\\' + task_id + '*.*')#[0]
					if len(thumbnail) > 0:
						thumbnail = thumbnail[0]
						if os.path.isfile(thumbnail):
							name = thumbnail.rsplit('\\',1)[1]
							recimg = f'{self.images_folder}\{name}'
							shutil.copy(thumbnail,self.images_folder)
					else:
						recimg = 'No Image'

				datainsert = (task_id, effective_uid, affinity, real_activity, first_active_time, last_active_time, last_time_moved, calling_package, user_id, action, component, snap, recimg, fullat1, fullat2)
				self.db.cursor().execute('INSERT INTO data (task_id, effective_uid, affinity, real_activity, first_active_time, last_active_time, last_time_moved, calling_package, user_id, action, component, snap, recimg, fullat1, fullat2)  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', datainsert)
				self.db.commit()
