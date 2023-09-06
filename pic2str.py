# -*- coding: utf-8 -*-
# code from https://clay-atlas.com\blog/2019/11/13/python-chinese-tutorial-packages-pyinstaller-image-exe/

import base64


def pic2str(file, functionName):
    pic = open(file, 'rb')
    content = '{} = {}\n'.format(functionName, base64.b64encode(pic.read()))
    pic.close()

    with open('copic.py', 'a') as f:
        f.write(content)
        #f.write('\n')


if __name__ == '__main__':
    pic2str(r".\assets\frame_check\button_cancel_off.png", 'img_button_cancel_off')
    pic2str(r".\assets\frame_check\button_stop_on.png", 'img_button_stopcheck_on')

    pic2str(r".\assets\frame_error\button_ok_on.png", 'img_button_ok_on')

    pic2str(r".\assets\frame_login\button_1.png", 'img_button_login_off')
    pic2str(r".\assets\frame_login\button_1_click.png", 'img_button_login_on')
    pic2str(r".\assets\frame_login\entry_1.png", 'img_entry_bg')
    pic2str(r".\assets\frame_login\image_1.png", 'img_logo')

    pic2str(r".\assets\frame_logout\button_logout_on.png", 'img_button_logout_on')

    pic2str(r".\assets\frame_result_chart\image_folder_off.png", 'img_button_folder_off')
    pic2str(r".\assets\frame_result_chart\image_home_off.png", 'img_button_home_off')
    pic2str(r".\assets\frame_result_chart\image_leave_off.png", 'img_button_export_off')
    pic2str(r".\assets\frame_result_chart\image_log_off.png", 'img_button_log_off')
    pic2str(r".\assets\frame_result_chart\image_setting_off.png", 'img_button_setting_off')

    pic2str(r".\assets\frame_result_list\image_folder_on.png", 'img_button_folder_on')
    pic2str(r".\assets\frame_result_list\image_next_on.png", 'img_button_next_on')
    pic2str(r".\assets\frame_result_list\image_previous_on.png", 'img_button_previous_on')
    pic2str(r".\assets\frame_result_list\image_return_on.png", 'img_button_return_on')
    pic2str(r".\assets\frame_result_list\image_empty_button.png", 'img_empty_button')

    pic2str(r".\assets\frame_result_log\image_log_on.png", 'img_button_log_on')

    pic2str(r".\assets\frame_setting\image_logout.png", 'img_button_logout')
    pic2str(r".\assets\frame_setting\image_result_off.png", 'img_button_result_off')
    pic2str(r".\assets\frame_setting\image_setting_on.png", 'img_button_setting_on')

    pic2str(r".\assets\frame_home\image_1.png", 'img_button_home_on')

    pic2str(r".\assets\frame_process\btn_opt_high_off.png", 'img_button_opt_high_off')
    pic2str(r".\assets\frame_process\btn_opt_high_on.png", 'img_button_opt_high_on')
    pic2str(r".\assets\frame_process\btn_opt_low_off.png", 'img_button_opt_low_off')
    pic2str(r".\assets\frame_process\btn_opt_low_on.png", 'img_button_opt_low_on')
    pic2str(r".\assets\frame_process\btn_opt_medium_off.png", 'img_button_opt_medium_off')
    pic2str(r".\assets\frame_process\btn_opt_medium_on.png", 'img_button_opt_medium_on')
    pic2str(r".\assets\frame_process\btn_opt_none_off.png", 'img_button_opt_none_off')
    pic2str(r".\assets\frame_process\btn_opt_none_on.png", 'img_button_opt_none_on')
    pic2str(r".\assets\frame_process\btn_opt_normal_off.png", 'img_button_opt_normal_off')
    pic2str(r".\assets\frame_process\btn_opt_normal_on.png", 'img_button_opt_normal_on')
    pic2str(r".\assets\frame_process\btn_opt_short_off.png", 'img_button_opt_short_off')
    pic2str(r".\assets\frame_process\btn_opt_short_on.png", 'img_button_opt_short_on')
    pic2str(r".\assets\frame_process\btn_opt_yes_off.png", 'img_button_opt_yes_off')
    pic2str(r".\assets\frame_process\btn_opt_yes_on.png", 'img_button_opt_yes_on')

    pic2str(r".\assets\frame_process\button_edit_off.png", 'img_button_edit_off')
    pic2str(r".\assets\frame_process\button_edit_on.png", 'img_button_edit_on')
    pic2str(r".\assets\frame_process\button_edit_out.png", 'img_button_edit_out')

    pic2str(r".\assets\frame_process\button_eject_off.png", 'img_button_eject_off')
    pic2str(r".\assets\frame_process\button_eject_on.png", 'img_button_eject_on')
    pic2str(r".\assets\frame_process\button_home_off.png", 'img_button_home_off')
    pic2str(r".\assets\frame_process\button_home_on.png", 'img_button_home_on')
    pic2str(r".\assets\frame_process\button_insert_off.png", 'img_button_insert_off')
    pic2str(r".\assets\frame_process\button_insert_on.png", 'img_button_insert_on')
    pic2str(r".\assets\frame_process\button_play_off.png", 'img_button_play_off')
    pic2str(r".\assets\frame_process\button_play_on.png", 'img_button_play_on')
    pic2str(r".\assets\frame_process\button_play_out.png", 'img_button_play_out')
    pic2str(r".\assets\frame_process\button_process_off.png", 'img_button_process_off')
    pic2str(r".\assets\frame_process\button_process_on.png", 'img_button_process_on')
    pic2str(r".\assets\frame_process\button_result_off.png", 'img_button_result_off')
    pic2str(r".\assets\frame_process\button_result_on.png", 'img_button_result_on')
    pic2str(r".\assets\frame_process\button_stop_off.png", 'img_button_stop_off')
    pic2str(r".\assets\frame_process\button_stop_on.png", 'img_button_stop_on')
    pic2str(r".\assets\frame_process\button_stop_out.png", 'img_button_stop_out')
    pic2str(r".\assets\frame_process\state_aborted.png", 'img_state_aborted')
    pic2str(r".\assets\frame_process\state_completed.png", 'img_state_completed')
    pic2str(r".\assets\frame_process\state_not_started.png", 'img_state_not_started')
