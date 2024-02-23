from voice_input import *
from vision_rec import *
from auto_click import *
from text_proc import *

def main():
    
    icon_click(process_icon_detection(extract_info(process_audio_to_text())))
    
    

if __name__ == "__main__":
    main()