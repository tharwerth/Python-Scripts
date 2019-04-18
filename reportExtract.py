#########################################################################
# This script unzips the zip files for each daily log review. Multiple days can be done at once. 
# Each date will be moved in to its own seperate folder and the top 20 reports will be contained in a subdirectory for each date
# To modiy this for personal use change the filepaths invariable declerations
#########################################################################

#imports
import gzip
import glob
import os.path
import tarfile
import shutil

#variable defenitions
zippath = "%filepath%\\logs\\zipped"
zipdest = "%filepath%\\logs\\toFile"
archive = "%filepath%\\logs\\archive"
extracted = "%filepath%\\logs\\extracted"
rootdir = "%filepath%ocuments\\logs"
datelist = []
archive = []
archive = []

#list stores the names of the top 20 daily reports
top20list = ['%namesofreports%']

#unzip .gz files and store tarballs
print("Unzipping files")
for src_name in glob.glob(os.path.join(zippath, '*.gz')): 
	base = os.path.basename(src_name)
	dest_name = os.path.join(zippath, base[:-3])
	with gzip.open(src_name, 'rb') as infile:
		with open(dest_name + '.tar', 'wb') as outfile:
			for line in infile:
				outfile.write(line)

#extract folders from tarballs   
print("Extracting tarballs")
#check if folder exists, if not create it
if not os.path.isdir(extracted):
	os.makedirs(extracted)         
for src_name in glob.glob(os.path.join(zippath, '*.tar')):
    base = os.path.basename(src_name)
    dest_name = os.path.join(extracted, base)
    tar = tarfile.open(src_name)
    tar.extractall(dest_name)

#copy report files 
print("Copying report files")
#check if folder exists, if not create
if not os.path.isdir(zipdest):
	os.makedirs(zipdest)
for root, dirs, files in os.walk(extracted):
   for file in files:
      path_file = os.path.join(root,file)
      shutil.copy2(path_file,zipdest)
           
#extract the date from filename to create the directories
srcfiles = os.listdir(zippath)
#reverse the filenames, scan for the date, then reverse the scanned string and store in a temp variable, then write to list
for filename in srcfiles:
	filename = ''.join(reversed(filename))
	filename = ''.join(i for i in filename if i.isdigit())
	tempdate = filename[6:14]
	datedir = ''.join(reversed(tempdate))
	if datedir not in datelist:
		datelist.append(datedir)
datedir = str(datedir)

#Create date coded directory for top 20 reports
print("Creating dated folder for reports")
top20 = "top20"
for date in datelist:
	datedir = date
	if os.path.isdir(os.path.join(rootdir,datedir)):
		print("Directrory for " + date + " already exists")
		createtop = os.path.join(rootdir,datedir)
	else:
		os.mkdir(os.path.join(rootdir,datedir))
		print("Creating directory for " + date)
		createtop = os.path.join(rootdir,datedir)
	if os.path.exists(os.path.join(createtop, top20)):
		print("Top 20 directrory for " + date + " already exists")
	else:
		print("Top 20 directory for " + date + " created")
		topdir = os.mkdir(os.path.join(createtop, top20))

#move top20 reports
i = 0
#move the top 20 files by looping through a list
print("Moving top 20 reports")
for root, dirs, files in os.walk(zipdest):
	for file in files: #for every file, check if the filename is in the list, if it is, move it
		filename = file
		if i <= len(files):
			for report in top20list:
				if report in filename:
					for date in datelist:
						if filename[14:22] == date:
							topmove = os.path.join(rootdir,date)
							path = os.path.join(zipdest,filename)
							check = os.path.join(topmove + '/' ,top20)
							topcheck = os.path.join(check, filename)
							#check if the report has been moved, if not, move it
							if os.path.isfile(topcheck):
								print("File already exists")
							else:	
								shutil.move(path, check)
							i += 1
							
x = 0
for root, dirs, files in os.walk(zipdest):
	for file in files: #for every file, check if the filename is in the list, if it is, move it
		filename = file
		if i <= len(files):
			for report in srcfiles:
				if report in filename:
					for date in datelist:
						if filename[14:22] == date:
							path = os.path.join(zipdest,filename)
							check = datedir
							topcheck = os.path.join(check, filename)
							#check if the report has been moved, if not, move it
							if os.path.isfile(topcheck):
								print("File already exists")
							else:	
								shutil.move(path, check)
							x += 1

#Create the dated log review folder
rootdir = "%filepath%\\logs"
#check for all dates in the date list, for every item in the list, create the necessary folders
for date in datelist:
	reviewdir = os.path.join(rootdir,date)
	print(reviewdir)
	if not os.path.isdir(os.path.join(rootdir,date)):
		os.makedirs(os.path.join(rootdir,date))
	for root, dirs, files in os.walk(zipdest):
		for file in files:
			filename = file
			if filename[14:22] == date:
				shutil.copy(zipdest + '/' + filename, reviewdir)
	
print("Cleaning up...")

#remove the temp directories
shutil.rmtree(zipdest)
shutil.rmtree(extracted)
