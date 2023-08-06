
class SchedOption:
    obj_list = []

    def __init__(self, params):

        self.schedoptions_id = params.get('schedoptions_id').strip() if params.get('schedoptions_id') else None
        self.proj_id = params.get('proj_id').strip() if params.get('proj_id') else None
        self.sched_outer_depend_type = params.get('sched_outer_depend_type').strip() if params.get('sched_outer_depend_type') else None
        self.sched_open_critical_flag = params.get('sched_open_critical_flag').strip() if params.get('sched_open_critical_flag') else None
        self.sched_lag_early_start_flag = params.get('sched_lag_early_start_flag').strip() if params.get('sched_lag_early_start_flag') else None
        self.sched_retained_logic = params.get('sched_retained_logic').strip() if params.get('sched_retained_logic') else None
        self.sched_setplantoforecast = params.get('sched_setplantoforecast').strip() if params.get('sched_setplantoforecast') else None
        self.sched_float_type = params.get('sched_float_type').strip() if params.get('sched_float_type') else None
        self.sched_calendar_on_relationship_lag = params.get('sched_calendar_on_relationship_lag').strip() if params.get('sched_calendar_on_relationship_lag') else None
        self.sched_use_expect_end_flag = params.get('sched_use_expect_end_flag').strip() if params.get('sched_use_expect_end_flag') else None
        self.sched_progress_override = params.get('sched_progress_override').strip() if params.get('sched_progress_override') else None
        self.level_float_thrs_cnt = params.get('level_float_thrs_cnt').strip() if params.get('level_float_thrs_cnt') else None
        self.level_outer_assign_flag = params.get('level_outer_assign_flag').strip() if params.get('level_outer_assign_flag') else None
        self.level_outer_assign_priority = params.get('level_outer_assign_priority').strip() if params.get('level_outer_assign_priority') else None
        self.level_over_alloc_pct = params.get('level_over_alloc_pct').strip() if params.get('level_over_alloc_pct') else None
        self.level_within_float_flag = params.get('level_within_float_flag').strip() if params.get('level_within_float_flag') else None
        self.level_keep_sched_date_flag = params.get('level_keep_sched_date_flag').strip() if params.get('level_keep_sched_date_flag') else None
        self.level_all_rsrc_flag = params.get('level_all_rsrc_flag').strip() if params.get('level_all_rsrc_flag') else None
        self.sched_use_project_end_date_for_float = params.get('sched_use_project_end_date_for_float').strip() if params.get('sched_use_project_end_date_for_float') else None
        self.enable_multiple_longest_path_calc = params.get('enable_multiple_longest_path_calc').strip() if params.get('enable_multiple_longest_path_calc') else None
        self.limit_multiple_longest_path_calc = params.get('limit_multiple_longest_path_calc').strip() if params.get('limit_multiple_longest_path_calc') else None
        self.max_multiple_longest_path = params.get('max_multiple_longest_path').strip() if params.get('max_multiple_longest_path') else None
        self.use_total_float_multiple_longest_paths = params.get('use_total_float_multiple_longest_paths').strip() if params.get('use_total_float_multiple_longest_paths') else None
        self.key_activity_for_multiple_longest_paths = params.get('use_total_float_multiple_longest_paths').strip() if params.get('use_total_float_multiple_longest_paths') else None
        self.LevelPriorityList = params.get('LevelPriorityList').strip() if params.get('LevelPriorityList') else None
        SchedOption.obj_list.append(self)

    def get_id(self):
        return self.schedoptions_id

    def __repr__(self):
        return self.proj_id