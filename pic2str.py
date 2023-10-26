# -*- coding: utf-8 -*-
# code from https://clay-atlas.com\blog/2019/11/13/python-chinese-tutorial-packages-pyinstaller-image-exe/

import base64


def pic2str(functionName, file):
    pic = open(file, 'rb')
    content = '{} = {}\n'.format(functionName, base64.b64encode(pic.read()))
    pic.close()

    with open('copic.py', 'a') as f:
        f.write(content)
        #f.write('\n')


if __name__ == '__main__':
    '''
    pic2str('img_button_cancel_off', r".\assets\frame_check\button_cancel_off.png")
    pic2str('img_button_edit_off', r".\assets\frame_process\button_edit_off.png")
    pic2str('img_button_edit_on', r".\assets\frame_process\button_edit_on.png")
    pic2str('img_button_edit_out', r".\assets\frame_process\button_edit_out.png")
    pic2str('img_button_eject_off', r".\assets\frame_process\button_eject_off.png")
    pic2str('img_button_eject_on', r".\assets\frame_process\button_eject_on.png")
    pic2str('img_button_export_off', r".\assets\frame_result_chart\image_leave_off.png")
    pic2str('img_button_folder_off', r".\assets\frame_result_chart\image_folder_off.png")
    pic2str('img_button_folder_on', r".\assets\frame_result_list\image_folder_on.png")
    pic2str('img_button_home_off', r".\assets\frame_process\button_home_off.png")
    pic2str('img_button_home_on', r".\assets\frame_process\button_home_on.png")
    pic2str('img_button_insert_off', r".\assets\frame_process\button_insert_off.png")
    pic2str('img_button_insert_on', r".\assets\frame_process\button_insert_on.png")

    pic2str('img_button_log_off', r".\assets\frame_result_chart\image_log_off.png")
    pic2str('img_button_log_on', r".\assets\frame_result_log\image_log_on.png")
    pic2str('img_button_login_off', r".\assets\frame_login\button_1.png")
    pic2str('img_button_login_on', r".\assets\frame_login\button_1_click.png")
    pic2str('img_button_logout', r".\assets\frame_setting\image_logout.png")
    pic2str('img_button_logout_on', r".\assets\frame_logout\button_logout_on.png")
    pic2str('img_button_next_on', r".\assets\frame_result_list\image_next_on.png")
    pic2str('img_button_ok_on', r".\assets\frame_error\button_ok_on.png")
    pic2str('img_button_play_off', r".\assets\frame_process\button_play_off.png")
    pic2str('img_button_play_on', r".\assets\frame_process\button_play_on.png")
    pic2str('img_button_play_out', r".\assets\frame_process\button_play_out.png")
    pic2str('img_button_previous_on', r".\assets\frame_result_list\image_previous_on.png")
    pic2str('img_button_process_off', r".\assets\frame_process\button_process_off.png")
    pic2str('img_button_process_on', r".\assets\frame_process\button_process_on.png")
    pic2str('img_button_result_off', r".\assets\frame_process\button_result_off.png")
    pic2str('img_button_result_on', r".\assets\frame_process\button_result_on.png")
    pic2str('img_button_return_on', r".\assets\frame_result_list\image_return_on.png")
    pic2str('img_button_setting_off', r".\assets\frame_result_chart\image_setting_off.png")
    pic2str('img_button_setting_on', r".\assets\frame_setting\image_setting_on.png")
    pic2str('img_button_stop_off', r".\assets\frame_process\button_stop_off.png")
    pic2str('img_button_stop_on', r".\assets\frame_process\button_stop_on.png")
    pic2str('img_button_stop_out', r".\assets\frame_process\button_stop_out.png")
    pic2str('img_button_stopcheck_on', r".\assets\frame_check\button_stop_on.png")

    pic2str('img_button_opt_high_off', r".\assets\frame_process\btn_opt_high_off.png")
    pic2str('img_button_opt_high_on', r".\assets\frame_process\btn_opt_high_on.png")
    pic2str('img_button_opt_low_off', r".\assets\frame_process\btn_opt_low_off.png")
    pic2str('img_button_opt_low_on', r".\assets\frame_process\btn_opt_low_on.png")
    pic2str('img_button_opt_medium_off', r".\assets\frame_process\btn_opt_medium_off.png")
    pic2str('img_button_opt_medium_on', r".\assets\frame_process\btn_opt_medium_on.png")
    pic2str('img_button_opt_none_off', r".\assets\frame_process\btn_opt_none_off.png")
    pic2str('img_button_opt_none_on', r".\assets\frame_process\btn_opt_none_on.png")
    pic2str('img_button_opt_normal_off', r".\assets\frame_process\btn_opt_normal_off.png")
    pic2str('img_button_opt_normal_on', r".\assets\frame_process\btn_opt_normal_on.png")
    pic2str('img_button_opt_short_off', r".\assets\frame_process\btn_opt_short_off.png")
    pic2str('img_button_opt_short_on', r".\assets\frame_process\btn_opt_short_on.png")
    pic2str('img_button_opt_yes_off', r".\assets\frame_process\btn_opt_yes_off.png")
    pic2str('img_button_opt_yes_on', r".\assets\frame_process\btn_opt_yes_on.png")

    pic2str('img_empty_button', r".\assets\frame_result_list\image_empty_button.png")
    pic2str('img_entry_bg', r".\assets\frame_login\entry_1.png")
    pic2str('img_logo', r".\assets\frame_login\image_1.png")

    pic2str('img_state_aborted', r".\assets\frame_process\state_aborted.png")
    pic2str('img_state_completed', r".\assets\frame_process\state_completed.png")
    pic2str('img_state_not_started', r".\assets\frame_process\state_not_started.png")
    '''
    #pic2str('img_button_delete_on', r".\assets\button_delete_on.png")
    #pic2str('img_co_logo', r".\assets\co_logo.png")
    #pic2str('image_reset_off', r".\assets\image_reset_off.png")
    #pic2str('image_reset_on', r".\assets\image_reset_on.png")
    #pic2str('image_test_off', r".\assets\image_test_off.png")
    #pic2str('image_test_on', r".\assets\image_test_on.png")
    #pic2str('image_time_off', r".\assets\image_time_off.png")
    #pic2str('image_time_on', r".\assets\image_time_on.png")
    #pic2str('image_user_off', r".\assets\image_user_off.png")
    #pic2str('image_user_on', r".\assets\image_user_on.png")
    #pic2str('button_home_result', r".\assets\button_home_result.png")
    #pic2str('button_home_test', r".\assets\button_home_test.png")
    pic2str('button_setting_edit', r".\assets\button_setting_edit.png")
    pic2str('button_setting_password', r".\assets\button_setting_password.png")
    pic2str('button_setting_test', r".\assets\button_setting_test.png")
    pic2str('button_setting_time', r".\assets\button_setting_time.png")



