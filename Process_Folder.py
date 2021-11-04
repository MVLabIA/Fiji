#@ File    (label = "Input directory", style = "directory") srcFile
#@ File    (label = "Output directory", style = "directory") dstFile
#@ String  (label = "File extension", value=".tif") ext
##@ String  (label = "File name contains", value = "") containString
#@ boolean (label = "Keep directory structure when saving", value = true) keepDirectories

# See also Process_Folder.ijm for a version of this code
# in the ImageJ 1.x macro language.
dyes = ['Syt9', 'DAPI', 'DiO', 'Syt59', 'Syt9', 'TRDHP']


import os

from ij import IJ, ImagePlus
#import trainableSegmentation

def run():
  dyes = ['Syt9', 'DAPI', 'DiO', 'Syt59', 'Syt9', 'TRDHP']
  srcDir = srcFile.getAbsolutePath()
  dstDir = dstFile.getAbsolutePath()
  for root, directories, filenames in os.walk(srcDir):
    filenames.sort();
    for containString in dyes:
      for filename in filenames:
        # Check for file extension
        if not filename.endswith(ext):
          continue
        # Check for file name pattern
        if containString not in filename:
          continue
        if "processed" in filename:
          continue
        print(directories)
        process(srcDir, dstDir, root, filename, keepDirectories)
 
def process(srcDir, dstDir, currentDir, fileName, keepDirectories):
  newdstDir = currentDir.replace(srcDir,"")
  if not os.path.exists(dstDir+newdstDir):
	os.makedirs(dstDir+newdstDir)
  print "Processing:"
   
  # Opening the image
  print "Open image file", fileName
  #imp = IJ.openImage(os.path.join(currentDir, fileName))
   
  # Put your processing commands here!
  IJ.open(os.path.join(currentDir, fileName))
  IJ.run("8-bit")
  IJ.run("Smooth", "stacks")
  #IJ.run("Auto Threshold", "method=Intermodes white")
  IJ.run("Set Measurements...", "area mean min centroid shape redirect=None decimal=3")
  IJ.run("Analyze Particles...", "size=1-Infinity display clear")
  IJ.saveAs("jpeg", dstDir+newdstDir + "/" + "Processed-" + fileName)
  IJ.saveAs("Results", dstDir+newdstDir + "/" + "Results-" + fileName + ".csv")
  IJ.run("Close")
  IJ.run("Close")
  '''
  # Saving the image
  saveDir = currentDir.replace(srcDir, dstDir) if keepDirectories else dstDir
  if not os.path.exists(saveDir):
    os.makedirs(saveDir)
  print "Saving to", saveDir
  IJ.saveAs(imp, "Tiff", os.path.join(saveDir, fileName));
  imp.close()
  '''
 
run()
