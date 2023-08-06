

class ResourceCurve:
    obj_list = []

    def __init__(self, params):
        self.curv_id = int(params.get('curv_id')) if params.get('curv_id') else None
        self.curv_name = params.get('curv_id').strip() if params.get('curv_id') else None
        self.default_flag = params.get('default_flag') if params.get('default_flag') else None
        self.pct_usage_0 = float(params.get('pct_usage_0')) if params.get('pct_usage_0') else None
        self.pct_usage_1 = float(params.get('pct_usage_1')) if params.get('pct_usage_1') else None
        self.pct_usage_2 = float(params.get('pct_usage_2')) if params.get('pct_usage_2') else None
        self.pct_usage_3 = float(params.get('pct_usage_3')) if params.get('pct_usage_3') else None
        self.pct_usage_4 = float(params.get('pct_usage_4')) if params.get('pct_usage_4') else None
        self.pct_usage_5 = float(params.get('pct_usage_5')) if params.get('pct_usage_5') else None
        self.pct_usage_6 = float(params.get('pct_usage_6')) if params.get('pct_usage_6') else None
        self.pct_usage_7 = float(params.get('pct_usage_7')) if params.get('pct_usage_7') else None
        self.pct_usage_8 = float(params.get('pct_usage_8')) if params.get('pct_usage_8') else None
        self.pct_usage_9 = float(params.get('pct_usage_9')) if params.get('pct_usage_9') else None
        self.pct_usage_10 = float(params.get('pct_usage_10')) if params.get('pct_usage_10') else None
        self.pct_usage_11 = float(params.get('pct_usage_11')) if params.get('pct_usage_11') else None
        self.pct_usage_12 = float(params.get('pct_usage_12')) if params.get('pct_usage_12') else None
        self.pct_usage_13 = float(params.get('pct_usage_13')) if params.get('pct_usage_13') else None
        self.pct_usage_14 = float(params.get('pct_usage_14')) if params.get('pct_usage_14') else None
        self.pct_usage_15 = float(params.get('pct_usage_15')) if params.get('pct_usage_15') else None
        self.pct_usage_16 = float(params.get('pct_usage_16')) if params.get('pct_usage_16') else None
        self.pct_usage_17 = float(params.get('pct_usage_17')) if params.get('pct_usage_17') else None
        self.pct_usage_18 = float(params.get('pct_usage_18')) if params.get('pct_usage_18') else None
        self.pct_usage_19 = float(params.get('pct_usage_19')) if params.get('pct_usage_19') else None
        self.pct_usage_20 = float(params.get('pct_usage_20')) if params.get('pct_usage_20') else None

        ResourceCurve.obj_list.append(self)

    @classmethod
    def find_by_id(cls, id):
        obj = list(filter(lambda x: x.curv_id == id, cls.obj_list))[0]
        return obj

    def __repr__(self):
        return self.curv_name
