import os, json
import mxdevtool as mx
import numpy as np
import mxdevtool.termstructures as ts
from mxdevtool.xenarix.pathcalc import *

XENFILE_EXT = 'xen'
HASHCODES_KEY = 'hashcodes'


# arguments parse from arg name
def get_arg_fromValue(name, arg_v, mrk_d, models_calcs):
    arg = None

    if 'Curve' == name[-len('Curve'):]:
        curve_d = mrk_d.get_yield_curve(arg_v)
        curveType = curve_d[mx.CLASS_TYPE_NAME]
        if curveType == ts.FlatForward.__name__:
            arg = ts.FlatForward.fromDict(curve_d, mrk_d)
        elif curveType == ts.ZeroYieldCurve.__name__:
            arg = ts.ZeroYieldCurve.fromDict(curve_d, mrk_d)
        elif curveType == ts.BootstapSwapCurveCCP.__name__:
            arg = ts.BootstapSwapCurveCCP.fromDict(curve_d, mrk_d)
        elif curveType == ts.ZeroSpreadedCurve.__name__:
            arg = ts.ZeroSpreadedCurve.fromDict(curve_d, mrk_d)
        else:
            raise Exception('unknown curveType - {0}'.format(name))
    elif 'volTs' == name or 'VolTs' == name[-len('VolTs'):]:
        volTs_d = mrk_d.get_volTs(arg_v)
        volType = volTs_d[mx.CLASS_TYPE_NAME]
        if volType == ts.BlackConstantVol.__name__:
            arg = ts.BlackConstantVol.fromDict(volTs_d, mrk_d)
        else:
            raise Exception('unknown volType - {0}'.format(name))
    elif 'Para' == name[-len('Para'):]:
        arg = DeterministicParameter.fromDict(arg_v)
    elif 'Date' == name[-len('Date'):]:
        arg = mx.Date(arg_v)
    elif 'compounding' == name or 'Compounding' == name[-len('Compounding'):]:
        arg = mx.compoundingParse(arg_v)
    elif 'calendar' == name or 'Calendar' == name[-len('Calendar'):]:
        arg = mx.calendarParse(arg_v)
    elif 'dayCounter' == name or 'DayCounter' == name[-len('DayCounter'):]:
        arg = mx.dayCounterParse(arg_v)
    elif 'businessDayConvention' == name or 'BusinessDayConvention' == name[-len('BusinessDayConvention'):]:
        arg = mx.businessDayConventionParse(arg_v)
    elif 'interpolationType' == name or 'InterpolationType' == name[-len('InterpolationType'):]:
        arg = mx.interpolator1DParse(arg_v)
    elif 'extrapolationType' == name or 'ExtrapolationType' == name[-len('ExtrapolationType'):]:
        arg = mx.extrapolator1DParse(arg_v)
    elif 'Tenor' == name[-len('Tenor'):]:
        arg = mx.Period(arg_v)
    elif name in ['ir_pc', 'pc', 'pc1', 'pc2'] and isinstance(arg_v, str)  :
        arg = models_calcs[arg_v]
    elif name == 'pc_list':
        arg = [models_calcs[pc] for pc in arg_v]
    else:
        arg = arg_v

    if arg is None:
        raise Exception('unsupported argument name : {0}'.format(arg_v))
    
    return arg


def get_args_fromDict(d, mrk_d, models_calcs, arg_names):
    args = []
    for name in arg_names:
        arg_v = d[name]
        # curve
        args.append(get_arg_fromValue(name, d[name], mrk_d, models_calcs))

    return args


# model parse
def parseClassFromDict(d, models_calcs, mrk_d=mx.MarketData()):
    if not isinstance(d, dict):
        raise Exception('dictionary type is required')
    
    classTypeName = d[mx.CLASS_TYPE_NAME]

    try:
        class_instance = globals()[classTypeName]
        init = getattr(class_instance, "__init__", None)
        args = get_args_fromDict(d, mrk_d, models_calcs, inspect.getargspec(init).args[1:])
        return class_instance(*args)
    except:
        raise Exception('unknown classTypeName - {0}'.format(classTypeName))


class Rsg(mx.core_Rsg):
    def __init__(self, sampleNum, dimension=365, seed=0, skip=0, isMomentMatching=False, randomType='pseudo', subType='mersennetwister', randomTransformType='boxmullernormal'):
        self._randomType = randomType
        self._subType = subType
        self._randomTransformType = randomTransformType

        mx.core_Rsg.__init__(self, sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)

    @staticmethod
    def fromDict(d, mrk_d=mx.MarketData()):
        mx.check_fromDict(d, mx.CLASS_TYPE_NAME, Rsg.__name__)

        sampleNum = d['sampleNum']
        dimension = d['dimension']
        seed = d['seed']
        skip = d['skip']
        isMomentMatching = d['isMomentMatching']
        randomType = d['randomType']
        subType = d['subType']
        randomTransformType = d['randomTransformType']

        return Rsg(sampleNum, dimension, seed, skip, isMomentMatching, randomType, subType, randomTransformType)

    def toDict(self):
        res = dict()

        res[mx.CLASS_TYPE_NAME] = self.__class__.__name__

        res['sampleNum'] = self.sampleNum
        res['dimension'] = self.dimension
        res['seed'] = self.seed
        res['skip'] = self.skip
        res['isMomentMatching'] = self.isMomentMatching
        res['randomType'] = self.randomType
        res['subType'] = self.subType
        res['randomTransformType'] = self.randomTransformType

        return res

    randomType = property(lambda self: self._randomType,None,None)
    subType = property(lambda self: self._subType,None,None)
    randomTransformType = property(lambda self: self._randomTransformType,None,None)


class ScenarioJsonBuilder:
    def __init__(self, json_dict):
        self.__dict__ = json_dict

    def _timegrid(self, tg_d, mrk_d):
        timegrid = None
        classTypeName = tg_d[mx.CLASS_TYPE_NAME]

        if classTypeName == mx.TimeGrid.__name__:
            timegrid = mx.TimeGrid.fromDict(tg_d)
        elif classTypeName == mx.TimeEqualGrid.__name__.lower():
            timegrid = mx.TimeEqualGrid.fromDict(tg_d)
        elif classTypeName == mx.TimeArrayGrid.__name__.lower():
            timegrid = mx.TimeArrayGrid.fromDict(tg_d)
        else:
            raise Exception('unknown timegrid type - {0}'.format(classTypeName))

        return timegrid

    def build_scenario_inputs(self, mrk_d):

        if mrk_d is None:
            mrk_d = mx.MarketData()

        # models
        models_calcs = dict()

        models = []
        for m in self.models:
            model = parseClassFromDict(m, models_calcs, mrk_d)
            models_calcs[model.name] = model
            models.append(model)
        
        calcs = []
        for c in self.calcs:
            calc = parseClassFromDict(c, models_calcs, mrk_d)
            models_calcs[calc.name] = calc
            calcs.append(calc)
        
        corr = mx.Matrix(self.corr)

        timegrid = self._timegrid(self.timegrid, mrk_d)
        rsg = Rsg.fromDict(self.rsg, mrk_d)

        return models, calcs, corr, timegrid, rsg, self.filename, self.isMomentMatching


# class Scenario(mx.core_ScenarioGenerator2):
class Scenario:
    def __init__(self, models, calcs, corr, timegrid, rsg, filename, isMomentMatching = False):
        _corr = mx.Matrix(corr)

        # _dimension = (len(timegrid) - 1) * len(models)
        # _rsg = Rsg(rsg.sampleNum, _dimension, rsg.seed, rsg.skip, rsg.isMomentMatching, rsg.randomType, rsg.subType, rsg.randomTransformType)

        self.models = models
        self.calcs = calcs
        self.corr = _corr
        self.timegrid = timegrid
        self.rsg = rsg
        self.filename = filename
        self.isMomentMatching = isMomentMatching

    @staticmethod
    def fromDict(d, mrk_d=None):
        if not isinstance(d, dict):
            raise Exception('dictionary type is required')

        sjb = ScenarioJsonBuilder(d)

        if mrk_d == None:
            mrk_d = mx.MarketData()
        args = sjb.build_scenario_inputs(mrk_d)
        return Scenario(*args)

    def toDict(self):
        res = dict()
        
        res['models'] = [ m.toDict() for m in self.models]
        res['calcs'] = [ c.toDict() for c in self.calcs]
        res['corr'] = self.corr.toList()
        res['timegrid'] = self.timegrid.toDict()
        res['rsg'] = self.rsg.toDict()
        res['filename'] = self.filename
        res['isMomentMatching'] = self.isMomentMatching

        return res

    def hashCode(self, encoding='utf-8'):
        from hashlib import sha256
        json_str = json.dumps(self.toDict())

        return sha256(json_str.encode(encoding)).hexdigest()
    
    def generate(self):
        _dimension = (len(self.timegrid) - 1) * len(self.models)
        _rsg = Rsg(self.rsg.sampleNum, _dimension, self.rsg.seed, self.rsg.skip, self.rsg.isMomentMatching, 
                   self.rsg.randomType, self.rsg.subType, self.rsg.randomTransformType)

        scen = mx.core_ScenarioGenerator2(self.models, self.calcs, self.corr, self.timegrid, 
                        _rsg, self.filename, self.isMomentMatching)

        scen.generate()

    
class ScenarioResults(mx.core_ScenarioResult):
    def __init__(self, filename):
        mx.core_ScenarioResult.__init__(self, filename)
        self.shape = (self.simulNum, self.assetNum, self.timegridNum) 

    def toNumpyArr(self):
        npz = np.load(self.filename)
        arr = npz['data']
        arr.reshape(self.shape)

        return arr

    def __getitem__(self, scenCount):
        return self._multiPath(scenCount)

    def tPosSlice(self, t_pos, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPos(t_pos)
        else:
            return self._multiPathTPos(scenCount, t_pos)

    def timeSlice(self, time, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateTime(time)
        else:
            return self._multiPathTPosInterpolateTime(scenCount, time)

    def dateSlice(self, date, scenCount=None):
        if scenCount is None:
            return self._multiPathAllTPosInterpolateDate(date)
        else:
            return self._multiPathTPosInterpolateDate(scenCount, date)


# history, connect to db, upload, download
# db, file or etc...
class XenarixManager:
    def load(self, name, key, refDate):
        pass

    def save(self, name, scen):
        pass

    def get_list(self, filter=None):
        pass


class XenarixFileManager(XenarixManager):
    def __init__(self, config):
        self.config = config
        self.location = config['location']

        if not os.path.exists(self.location):
            raise Exception('directory does not exist - {0}'.format(self.location) )

    def _build_dict(self, scen):
        scen_d = scen.toDict()
        hashcodes_d = dict()
        
        hashcodes_d['base'] = scen.hashCode()

        scen_d[HASHCODES_KEY] = hashcodes_d

        return scen_d

    def save(self, name, scen):
        json_str = None
        path = os.path.join(self.location, name + '.' + XENFILE_EXT)
        f = open(path, "w")
        
        if isinstance(scen, Scenario):
            d = dict()
            d['scen0'] = self._build_dict(scen)
            json_str = json.dumps(d)
        elif isinstance(scen, list):
            if len(scen) == 0:
                raise Exception('empty list')

            d = dict()
            k = 0
            for s in scen:
                if not isinstance(s, Scenario):
                    raise Exception('scenario type is required')
                else:
                    scen_name = 'scen{0}'.format(k)
                    d[scen_name] = self._build_dict(s)
                k += 1
            json_str = json.dumps(d)
        elif isinstance(scen, dict):
            if len(scen) == 0:
                raise Exception('empty dict')

            if len(scen) == 1:
                self.save(name, scen[0])
                return

            d = dict()
            for k, s in scen.items():
                if not isinstance(s, Scenario):
                    raise Exception('scenario type is required')
                else:
                    d[k] = self._build_dict(s)
            json_str = json.dumps(d)
        else:
            f.close()
            raise Exception('scenario type is required')
        
        if json_str is None:
            f.close()
            raise Exception('nothing to write')
        
        f.write(json_str)
        f.close()

    def load(self, name):
        path = os.path.join(self.location, name + '.' + XENFILE_EXT)
        f = open(path, "r")
        json_str = f.read()
        scen_d = json.loads(json_str)

        res = dict()
        
        for k, v in scen_d.items():
            sb = ScenarioJsonBuilder(v)
            inputs = sb.build_scenario_inputs(mrk_d=None)
            res[k] = Scenario(*inputs)

        return res

    def scenList(self):
        included_extensions = [ XENFILE_EXT ]
        file_names = [os.path.splitext(fn)[0] for fn in os.listdir(self.location)
            if any(fn.endswith(ext) for ext in included_extensions)]
        
        return file_names


def generate1d(model, calcs, timegrid, rsg, filename, isMomentMatching = False):
    _calcs = calcs

    if calcs is None:
        _calcs = []

    corr = mx.IdentityMatrix(1)

    scen = Scenario([model], _calcs, corr, timegrid, rsg, filename, isMomentMatching)
    scen.generate()

    return ScenarioResults(filename)


def generate(models, calcs, corr, timegrid, rsg, filename, isMomentMatching = False):
    if calcs is None:
        calcs = []

    scen = Scenario(models, calcs, corr, timegrid, rsg, filename, isMomentMatching)
    scen.generate()

    return ScenarioResults(filename)

