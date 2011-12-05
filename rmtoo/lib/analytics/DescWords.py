#
# -*- coding: utf-8 -*-
#
'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  The Description is the critical part of the requirement. This
  module checks for some good and bad words and tries a heuristic to
  get an idea about bad requirement descriptions.
   
 (c) 2010-2011 by flonatel GmhH & Co. KG

 For licensing details see COPYING
'''

import re

from rmtoo.lib.LaTeXMarkup import LaTeXMarkup
from rmtoo.lib.analytics.Result import Result

class DescWords:

    # This is the assessment of each word (better regular expression).
    # If the regular expression matches, the value is added.
    # If the resulting number is lower than a given limit, an error is
    # assumed. 
    # The numbers are provided on a level between [-100, 100] where
    # -100 is a very very bad word and 100 is a very very good.
    # Do not add the single word 'not': only do this in pairs,
    # e.g. 'must not'.
    words_en_GB = [
        [ re.compile("\. "), -15, "Additional fullstop (not only at the end of the desctiption)"],
        [ re.compile(" about "), -15, "Usage of the word 'about'"],
        [ re.compile(" and "), -10, "Usage of the word 'and'"],
        [ re.compile(" approximately "), -100, "Usage of the word 'approximately'"],
        [ re.compile(" etc\.? "), -40, "Usage of the word 'etc'"],
        [ re.compile(" e\.g\. "), -40, "Usage of the word 'e.g.'"],
        [ re.compile(" has to "), 20, "Usage of the word 'has to'"],
        [ re.compile(" have to "), 20, "Usage of the word 'have to'"],
        [ re.compile(" i\.e\. "), -40, "Usage of the word 'i.e.'"],
        [ re.compile(" many "), -20, "Usage of the word 'many'"],
        [ re.compile(" may "), 10, "Usage of the word 'may'"],
        [ re.compile(" maybe "), -50, "Usage of the word 'maybe'"],
        [ re.compile(" might "), 10, "Usage of the word 'might'"],
        [ re.compile(" must "), 25, "Usage of the word 'must'"],
        [ re.compile(" or "), -15, "Usage of the word 'or'"],
        [ re.compile(" perhaps "), -100, "Usage of the word 'perhaps'"],
        [ re.compile(" should "), 15, "Usage of the word 'should'"],
        [ re.compile(" shall "), 15, "Usage of the word 'shall'"],
        [ re.compile(" some "), -25, "Usage of the word 'some'"],
        [ re.compile(" vaguely "), -25, "Usage of the word 'vaguely'"],
    ]

    words_de_DE = [
        [ re.compile("\. "), -15, "Additional fullstop (not only at the end of the desctiption)"],
        [ re.compile(" ca\. "), -75, "Usage of the word 'ca.'"],
        [ re.compile(" möglicherweise "), -100, "Usage of the word 'möglicherweise'"],
        [ re.compile(" muss "), 25, "Usage of the word 'muss'"],
        [ re.compile(" oder "), -15, "Usage of the word 'oder'"],
        [ re.compile(" und "), -10, "Usage of the word 'und'"],
        [ re.compile(" usw."), -40, "Usage of the word 'usw'"],
        [ re.compile(" vielleicht "), -25, "Usage of the word 'vielleicht'"],
        [ re.compile(" z\.B\. "), -40, "Usage of the word 'z.B.'"],
    ]

    words = { "en_GB": words_en_GB,
              "de_DE": words_de_DE, }

    def __init__(self, config):
        '''Sets up the DescWord object for use.'''
        self.lwords = DescWords.get_lang(config)

    @staticmethod
    def get_lang(config):
        def_lang = config.get_value_default(
                'requirements.input.default_language', 'en_GB')

        if def_lang in DescWords.words:
            return DescWords.words[def_lang]
        else:
            return None
        return DescWords.words["en_GB"]

    @staticmethod
    def analyse(lname, lwords, text):
        # print("ANALYSE: [%s]" % text)
        # Must be at least some positive things to get this
        # positive. (An empty description is a bad one.)
        level = -10
        log = []
        for wre, wlvl, wdsc in lwords:
            plain_txt = LaTeXMarkup.replace_txt(text).strip()
            fal = len(wre.findall(plain_txt))
            if fal > 0:
                level += fal * wlvl
                log.append("%+4d:%d*%d: %s" % (fal * wlvl, fal, wlvl, wdsc))
                # Note the result of this test in the requirement itself.
        return Result('DescWords', lname, level, log)

    def check_requirement(self, lname, req):
        '''Checks all the requirements.
           If the result is positive, it is good.'''
        #print("DescWords called")
        result = DescWords.analyse(lname,
                 self.lwords, req.get_value("Description").get_content())
        return result.get_value() >= 0, result
