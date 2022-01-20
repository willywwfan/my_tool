import ffmpeg
import os

if __name__ == '__main__':
    folder_name = input('folder name:')
    file_list = os.listdir(folder_name)
    work_path = os.listdir('./')
    if "output" not in  work_path:os.mkdir("./output/")
    output_path = os.listdir('./output')
    if folder_name not in output_path:os.mkdir("./output/" + folder_name)

    for file in file_list:
        if file.split(".")[-1] not in ["mp4", "avi", "mov", "wmv", "mkv"]:
            break
        input_video = ffmpeg.input( folder_name + "/" + file)
        (
            ffmpeg
            .output(input_video.video, "./output/" + folder_name + "/" + file.split(".")[0]+ "_convert." +file.split(".")[-1], crf = 23, vcodec = 'libx264')
            .overwrite_output()
            .run()
        )