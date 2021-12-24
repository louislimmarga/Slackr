import os, shutil

def clearPictures():
    folder = './pictures'
    for the_file in os.listdir(folder):
        if the_file == "firstAvatar.jpg":
            continue
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def clear():
    if os.path.exists('usersData.p'):
        os.remove('./usersData.p')
    if os.path.exists('channelsData.p'):
        os.remove('./channelsData.p')
    if os.path.exists('resetCodes.p'):
        os.remove('./resetCodes.p') 
    if os.path.exists('channelsMessages.p'):
        os.remove('./channelsMessages.p')
    if os.path.exists('unusedMessageID.p'):
        os.remove('./unusedMessageID.p')
    if os.path.exists('channelsTimer.p'):
        os.remove('./channelsTimer.p')
    if os.path.exists('usersImageNames.p'):
        os.remove('./usersImageNames.p')
