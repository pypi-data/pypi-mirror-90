from typing import NoReturn
import math
import numpy
import matplotlib.pyplot as plt

from cryspy.B_parent_classes.cl_1_item import ItemN
from cryspy.B_parent_classes.cl_2_loop import LoopN


class DiffrnRefln(ItemN):
    """
    The flip ratios measured in the single diffraction experiment.

    Data items in the DIFFRN_REFLN category record details about
    the intensities measured in the diffraction experiment.

    The DIFFRN_REFLN data items refer to individual intensity
    measurements and must be included in looped lists.

    Attributes:
        - 

    """
    ATTR_MANDATORY_NAMES = ("index_h", "index_k", "index_l")
    ATTR_MANDATORY_TYPES = (int, int, int)
    ATTR_MANDATORY_CIF = ("index_h", "index_k", "index_l")

    ATTR_OPTIONAL_NAMES = ("fr", "fr_sigma", "fr_calc", "intensity_up_calc",
                           "intensity_down_calc")
    ATTR_OPTIONAL_TYPES = (float, float, float, float, float)
    ATTR_OPTIONAL_CIF = ("fr", "fr_sigma", "fr_calc" , "intensity_up_calc",
                         "intensity_down_calc")

    ATTR_NAMES = ATTR_MANDATORY_NAMES + ATTR_OPTIONAL_NAMES
    ATTR_TYPES = ATTR_MANDATORY_TYPES + ATTR_OPTIONAL_TYPES
    ATTR_CIF = ATTR_MANDATORY_CIF + ATTR_OPTIONAL_CIF

    ATTR_INT_NAMES = ()
    ATTR_INT_PROTECTED_NAMES = ()

    # parameters considered are refined parameters
    ATTR_REF = ()
    ATTR_SIGMA = tuple([f"{_h:}_sigma" for _h in ATTR_REF])
    ATTR_CONSTR_FLAG = tuple([f"{_h:}_constraint" for _h in ATTR_REF])
    ATTR_REF_FLAG = tuple([f"{_h:}_refinement" for _h in ATTR_REF])

    # formats if cif format
    D_FORMATS = {"fr_calc": "{:.5f}", "intensity_up_calc": "{:.2f}",
                 "intensity_down_calc": "{:.2f}"}

    # constraints on the parameters
    D_CONSTRAINTS = {}

    # default values for the parameters
    D_DEFAULT = {}
    for key in ATTR_SIGMA:
        D_DEFAULT[key] = 0.
    for key in (ATTR_CONSTR_FLAG + ATTR_REF_FLAG):
        D_DEFAULT[key] = False

    PREFIX = "diffrn_refln"

    def __init__(self, **kwargs) -> NoReturn:
        super(DiffrnRefln, self).__init__()

        # defined for any integer and float parameters
        D_MIN = {"fr": 0., "fr_sigma": 0., "fr_calc": 0.,
                 "intensity_up_calc": 0., "intensity_down_calc": 0.}

        # defined for ani integer and float parameters
        D_MAX = {}

        self.__dict__["D_MIN"] = D_MIN
        self.__dict__["D_MAX"] = D_MAX
        for key, attr in self.D_DEFAULT.items():
            setattr(self, key, attr)
        for key, attr in kwargs.items():
            setattr(self, key, attr)


class DiffrnReflnL(LoopN):
    """
    Flip ratios measured in the single diffraction experiment.

    """
    ITEM_CLASS = DiffrnRefln
    ATTR_INDEX = None
    def __init__(self, loop_name = None) -> NoReturn:
        super(DiffrnReflnL, self).__init__()
        self.__dict__["items"] = []
        self.__dict__["loop_name"] = loop_name

    def report(self):
        return self.report_agreement_factor_exp() + "\n" + self.report_chi_sq_exp()

    def report_agreement_factor_exp(self):
        """
        Make a report about experimental agreement factor in string format.
        """

        l_chi_sq_exp, l_ag_f_exp = [], []
        l_diff = []
        n_3s, n_2s, n_1s, n_0s = 0, 0, 0, 0
        l_hkl = [(int(_1), int(_2), int(_3)) for _1, _2, _3 in
                 zip(self.index_h, self.index_k, self.index_l)]
        for _hkl, _fr_1, _fr_sigma_1 in zip(l_hkl, self.fr, self.fr_sigma):
            _diff = abs(_fr_1-1.)/float(_fr_sigma_1)
            if _diff >= 3.:
                n_3s += 1
            elif _diff >= 2.:
                n_2s += 1
            elif _diff >= 1.:
                n_1s += 1
            else:
                n_0s += 1
            if _fr_1 <= 1.:
                l_diff.append(1./_fr_1-1.)
            else:
                l_diff.append(_fr_1-1.)

            _mhkl = (-1 * _hkl[0], -1 * _hkl[1], -1 * _hkl[2])
            if _mhkl in l_hkl:
                ind_mhkl = l_hkl.index(_mhkl)
                _fr_2, _fr_sigma_2 = self.fr[ind_mhkl], self.fr_sigma[ind_mhkl]
                _fr_sigma = 1. / (_fr_sigma_1 ** (-2) + _fr_sigma_2 ** (-2)) ** 0.5
                _fr_average = (_fr_1 * _fr_sigma_1 ** (-2) + _fr_2 * _fr_sigma_2 ** (-2)) * _fr_sigma ** 2
                delta_fr = abs(_fr_1 - _fr_average)
                chi_sq_exp = (delta_fr / _fr_sigma_1) ** 2
                l_chi_sq_exp.append(chi_sq_exp)
                if math.isclose(_fr_1-1., 0):
                    ag_f_exp = abs((_fr_1 - _fr_average) / (_fr_1 - 1.+_fr_sigma_1))
                else:
                    ag_f_exp = abs((_fr_1 - _fr_average) / (_fr_1 - 1.))
                l_ag_f_exp.append(ag_f_exp)
                # print("hkl: {:4} {:4} {:4}".format(_hkl[0], _hkl[1], _hkl[2]))
                # print("chi_sq_exp: {:.3f} ".format(chi_sq_exp))
                # print("ag_f_exp: {:.3f} ".format(ag_f_exp))
        ls_out = ["# Experimental agreement factor\n"]
        n = n_0s + n_1s + n_2s + n_3s
        ls_out.append(f"\n| Number of measured reflections:| {n:4}|")
        ls_out.append(f"  |    range of h is |{min([_[0] for _ in l_hkl]):3},{max([_[0] for _ in l_hkl]):3} |")
        ls_out.append(f"  |             k is |{min([_[1] for _ in l_hkl]):3},{max([_[1] for _ in l_hkl]):3} |")
        ls_out.append(f"  |             l is |{min([_[2] for _ in l_hkl]):3},{max([_[2] for _ in l_hkl]):3} |")
        ls_out.append(f" |max(FR_exp - 1) is |{max(l_diff):5.3f} |")
        ls_out.append("\n N+1 > abs(FR_exp - 1)/FR_sigma > N: ")
        ls_out.append(f" |abs(FR_exp - 1)/FR_sigma < 1: |{n_0s:4}| {100*float(n_0s)/float(n):5.1f}% | ")
        ls_out.append(f" |                    N = 1: |{n_1s:4}| {100*float(n_1s)/float(n):5.1f}%  |")
        ls_out.append(f" |                    N = 2: |{n_2s:4}| {100 * float(n_2s) / float(n):5.1f}% |")
        ls_out.append(f" |abs(FR_exp - 1)/FR_sigma > 3: |{n_3s:4}| {100 * float(n_3s) / float(n):5.1f}% |")

        n_friedel = len(l_chi_sq_exp)
        ls_out.append(f"\n|Total number of Friedel reflections is |{n_friedel:}.|")
        if n_friedel != 0:
            ls_out.append(f"|  (abs(FR_exp-FR_av.)/FR_sigma)^2  is| {sum(l_chi_sq_exp) / n_friedel:.2f}|")
            ls_out.append(f"|   abs(FR_exp-FR_av.)/abs(FR_exp-1) per reflection is |{(100*sum(l_ag_f_exp)/n_friedel):.2f}% |")

        return "\n".join(ls_out)

    def calc_chi_sq_points(self) -> (float, int):
        """Calculate chi_sq and points if fr, fr_sigma, fr_calc are given."""
        l_fr, l_fr_sigma, l_fr_calc = self.fr, self.fr_sigma, self.fr_calc
        if (l_fr is None) & (l_fr_sigma is None) & (l_fr_calc is None):
            return (None, None)

        l_chi_sq = [(abs(float(fr-fr_calc)/float(fr_sigma))**2)
                    for fr, fr_sigma, fr_calc
                    in zip(l_fr, l_fr_sigma, l_fr_calc)]
        return sum(l_chi_sq), len(l_chi_sq)

    def report_chi_sq_exp(self, cell=None) -> str:
        """
        Make a report about experimental chi_sq in string format.

        cell is unit cell object.
        """
        ls_out = []
        l_hkl = [(_1, _2, _3) for _1, _2, _3 in zip(self.index_h, self.index_k, self.index_l)]
        l_fr, l_fr_sigma, l_fr_calc = self.fr, self.fr_sigma, self.fr_calc
        if (l_fr is None) & (l_fr_sigma is None) & (l_fr_calc is None):
            return "\n".join(ls_out)
        n = len(l_fr)
        n_1s, n_2s, n_3s = 0, 0, 0
        l_chi_sq, l_worsest, l_af_f, l_af_r = [], [], [], []
        for _hkl, _fr, _fr_sigma, _fr_calc in zip(l_hkl, l_fr, l_fr_sigma, l_fr_calc):
            _diff = abs(float(_fr-_fr_calc)/float(_fr_sigma))
            l_chi_sq.append(_diff**2)
            l_af_f.append(abs(float(_fr - _fr_calc) / float(_fr)))
            if _fr != 1.:
                l_af_r.append(abs(float(_fr-_fr_calc)/float(_fr-1)))
            if _diff <= 1.:
                n_1s +=1
            elif _diff <= 2.:
                n_2s += 1
            elif _diff <= 3.:
                n_3s += 1
            else:
                l_worsest.append((_hkl, _fr, _fr_sigma, _fr_calc, _diff))
        ls_out.append("# Chi_sq experimental")
        ls_out.append(f"Total number of reflections is {n:}")
        ls_out.append(f"|  (abs(FR_exp-FR_mod)/FR_sigma)^2 per reflection is |{sum(l_chi_sq)/float(n):.2f}|")
        ls_out.append(f"|   abs(FR_exp-FR_mod)/FR_exp      per reflection is |{100*sum(l_af_f) / float(n):.2f}%|")
        ls_out.append(f"|   abs(FR_exp-FR_mod)/abs(FR_exp-1)    per reflection is |{100*sum(l_af_r) / float(n):.2f}%|")
        ls_out.append("           (reflections with FR_exp = 1 are excluded)")
        n_worsest = len(l_worsest)
        ls_out.append("\n## Reflections in range  ")
        ls_out.append(" (N-1)*FR_sigma < abs(FR_exp - FR_mod) < N*FR_sigma: ")
        ls_out.append(f"|      N = 1:| {n_1s:}/{n:} ={100*float(n_1s)/float(n):5.1f}% ({2*34.1:4.1f}%, three sigma rule) |")
        ls_out.append(f"|      N = 2:| {n_2s:}/{n:} ={100 * float(n_2s) / float(n):5.1f}% ({2*(13.6):4.1f}%, three sigma rule)|")
        ls_out.append(f"|      N = 3:| {n_3s:}/{n:} ={100 * float(n_3s) / float(n):5.1f}% ({2*(2.1):4.1f}%, three sigma rule)|")
        ls_out.append(f"|      N > 3:| {n_worsest:}/{n:} ={100 * float(n_worsest) / float(n):5.1f}% ({2*(0.1):4.1f}%, three sigma rule)|")
        l_worsest.sort(key=lambda x: x[4], reverse=True)
        if len(l_worsest) > 1:
            if n_worsest > 10: n_worsest = 10
            ls_out.append("\n## The ten worsest reflections:")
            ls_out.append("|  h | k | l  |     FR |FR_sigma | FR_calc | diff|")
            for (_hkl, _fr, _fr_sigma, _fr_calc, _diff) in l_worsest[:n_worsest]:
                ls_out.append(f"|{_hkl[0]:3}|{_hkl[1]:3}|{_hkl[2]:3}|{_fr:9.5f}|{_fr_sigma:9.5f}|{_fr_calc:9.5f}|{_diff:6.1f}|")
        if cell is not None:
            np_h = numpy.array(self.index_h, dtype=int)
            np_k = numpy.array(self.index_k, dtype=int)
            np_l = numpy.array(self.index_l, dtype=int)
            np_sthovl = cell.calc_sthovl(index_h=np_h, index_k=np_k,
                                         index_l=np_l)
            np_fr, np_fr_sigma = numpy.array(l_fr, dtype=float), numpy.array(l_fr_sigma, dtype=float) 
            np_fr_calc = numpy.array(l_fr_calc, dtype=float)
            np_diff = numpy.abs((np_fr-np_fr_calc)/np_fr_sigma)
            n_bins = 10
            np_val, np_sthovl_bins = numpy.histogram(np_sthovl, bins=n_bins)
            ls_out.append("\n## Distribution of reflection in sin(theta)/lambda range")
            ls_out.append("|sthovl_1 |sthovl_2 | (Exp-Mod)/Sigma |n_points|")
            for _1, _2, _3 in zip(np_sthovl_bins[:-1], np_sthovl_bins[1:], np_val):
                np_flag = numpy.logical_and(np_sthovl >= _1, np_sthovl < _2) 
                res = np_diff[np_flag]
                if res.size == 0:
                    ls_out.append(f"|{_1:8.3f} |{_2:8.3f}|       None    |      0|")
                else:
                    ls_out.append(f"|{_1:8.3f} |{_2:8.3f}|    {np_diff[np_flag].mean():7.3f} |{_3:10}|")
            numpy.histogram(np_sthovl, bins=n_bins)
        return "\n".join(ls_out)

    def plots(self):
        return [self.plot_fr_vs_fr_calc()]
    
    def plot_fr_vs_fr_calc(self):
        """Plot experimental fr vs. fr_calc
        """
        if not(self.is_attribute("fr") & self.is_attribute("fr_sigma") &
               self.is_attribute("fr_calc")):
            return 

        fig, ax = plt.subplots()
        ax.set_title("Flip Ratio")
        np_fr_1 = numpy.array(self.fr, dtype=float)-numpy.array(self.fr_sigma, dtype=float)
        np_fr_2 = numpy.array(self.fr, dtype=float)+numpy.array(self.fr_sigma, dtype=float)
        fr_min = min([min(np_fr_1), min(self.fr_calc)])
        fr_max = max([max(np_fr_2), max(self.fr_calc)])
        ax.plot([fr_min, fr_max], [fr_min, fr_max], "k:")
        ax.errorbar(self.fr_calc, self.fr, yerr=self.fr_sigma, fmt="ko",
                    alpha=0.2)
        ax.set_xlabel("Flip ratio (model)")
        ax.set_ylabel('Flip ratio (experiment)')
        ax.set_aspect(1)
        fig.tight_layout()
        return (fig, ax)
        
# s_cont = """
#   loop_
#   _diffrn_refln_index_h
#   _diffrn_refln_index_k
#   _diffrn_refln_index_l
#   _diffrn_refln_fr
#   _diffrn_refln_fr_sigma
#       0    0    8   0.64545   0.01329 
#       2    0    6   1.75682   0.0454
# """

# obj = DiffrnReflnL.from_cif(s_cont)
# print(obj, end="\n\n")
# print(obj.report_agreement_factor_exp(), end="\n\n")
# print(obj.numpy_fr_sigma, end="\n\n")
