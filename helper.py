def isImage(file):
  length = len(file.rsplit('.'))
  return ('.' in file and file.rsplit('.')[length - 1].lower() in ['png', 'jpg', 'jpeg'])
