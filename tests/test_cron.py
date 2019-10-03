import pytest
import datetime

import cronwhen.cron


base_point = datetime.datetime(2019,10,3,12,49) #Thursday

def check_cron_expression(expr,results):
    d = base_point
    ce = cronwhen.cron.CronExpression(expr)
    for r in results:
        d = ce.getNextOccurence(d)
        Y,M,D,h,m = r
        if d.year != Y or d.month != M or d.day != D or d.hour != h or d.minute != m:
            df = '%a %d %b(%m) %Y, at %H:%M:%S'
            pytest.fail("Expression %s: expected = %s | computed = %s" %
                (expr, datetime.datetime(Y,M,D,h,m).strftime(df), d.strftime(df)))


def test_cron_any():
    t = ('* * * * *',        ((2019,10, 3,12,50),(2019,10, 3,12,51),(2019,10, 3,12,52)))
    check_cron_expression(*t)

def test_cron_string_days():
    tests = [
        ('1 2 * * SUN',     ((2019,10, 6, 2, 1),(2019,10,13, 2, 1))),
        ('1 2 * * MON',     ((2019,10, 7, 2, 1),(2019,10,14, 2, 1))),
        ('1 2 * * TUE',     ((2019,10, 8, 2, 1),(2019,10,15, 2, 1))),
        ('1 2 * * WED',     ((2019,10, 9, 2, 1),(2019,10,16, 2, 1))),
        ('1 2 * * THU',     ((2019,10,10, 2, 1),(2019,10,17, 2, 1))),
        ('1 2 * * FRI',     ((2019,10, 4, 2, 1),(2019,10,11, 2, 1))),
        ('1 2 * * SAT',     ((2019,10, 5, 2, 1),(2019,10,12, 2, 1))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_string_months():
    tests = [
        ('1 2 3 JAN *',     ((2020, 1, 3, 2, 1),(2021, 1, 3, 2, 1))),
        ('1 2 3 FEB *',     ((2020, 2, 3, 2, 1),(2021, 2, 3, 2, 1))),
        ('1 2 3 MAR *',     ((2020, 3, 3, 2, 1),(2021, 3, 3, 2, 1))),
        ('1 2 3 APR *',     ((2020, 4, 3, 2, 1),(2021, 4, 3, 2, 1))),
        ('1 2 3 MAY *',     ((2020, 5, 3, 2, 1),(2021, 5, 3, 2, 1))),
        ('1 2 3 JUN *',     ((2020, 6, 3, 2, 1),(2021, 6, 3, 2, 1))),
        ('1 2 3 JUL *',     ((2020, 7, 3, 2, 1),(2021, 7, 3, 2, 1))),
        ('1 2 3 AUG *',     ((2020, 8, 3, 2, 1),(2021, 8, 3, 2, 1))),
        ('1 2 3 SEP *',     ((2020, 9, 3, 2, 1),(2021, 9, 3, 2, 1))),
        ('1 2 3 OCT *',     ((2020,10, 3, 2, 1),(2021,10, 3, 2, 1))),
        ('1 2 3 NOV *',     ((2019,11, 3, 2, 1),(2020,11, 3, 2, 1))),
        ('1 2 3 DEC *',     ((2019,12, 3, 2, 1),(2020,12, 3, 2, 1))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_simple_field():
    # Single field, either requiring an increment of the field above or not
    tests = [
        ('59 * * * *',       ((2019,10, 3,12,59),(2019,10, 3,13,59),(2019,10, 3,14,59))),
        ('35 * * * *',       ((2019,10, 3,13,35),(2019,10, 3,14,35),(2019,10, 3,15,35))),
        ('* 19 * * *',       ((2019,10, 3,19, 0),(2019,10, 3,19, 1),(2019,10, 3,19, 2))),
        ('* 0 * * *',        ((2019,10, 4, 0, 0),(2019,10, 4, 0, 1),(2019,10, 4, 0, 2))),
        ('* * 5 * *',        ((2019,10, 5, 0, 0),(2019,10, 5, 0, 1),(2019,10, 5, 0, 2))),
        ('* * 1 * *',        ((2019,11, 1, 0, 0),(2019,11, 1, 0, 1),(2019,11, 1, 0, 2))),
        ('* * * * 6',        ((2019,10, 5, 0, 0),(2019,10, 5, 0, 1),(2019,10, 5, 0, 2))),
        ('* * * * 1',        ((2019,10, 7, 0, 0),(2019,10, 7, 0, 1),(2019,10, 7, 0, 2))),
        ('* * * 12 *',       ((2019,12, 1, 0, 0),(2019,12, 1, 0, 1),(2019,12, 1, 0, 2))),
        ('* * * 1 *',        ((2020, 1, 1, 0, 0),(2020, 1, 1, 0, 1),(2020, 1, 1, 0, 2))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_day_in_months():
    # Day of month, testing the number of days in each month and leap years
    tests = [
        # Day of month, testing the number of days in each month and leap years
        ('0 0 31 * *',       ((2019,10,31, 0, 0),(2019,12,31, 0, 0),(2020, 1,31, 0, 0),(2020, 3,31, 0, 0))),
        ('0 0 29 * *',       ((2019,10,29, 0, 0),(2019,11,29, 0, 0),(2019,12,29, 0, 0),(2020, 1,29, 0, 0),
                              (2020, 2,29, 0, 0),(2020, 3,29, 0, 0),(2020, 4,29, 0, 0),(2020, 5,29, 0, 0),
                              (2020, 6,29, 0, 0),(2020, 7,29, 0, 0),(2020, 8,29, 0, 0),(2020, 9,29, 0, 0),
                              (2020,10,29, 0, 0),(2020,11,29, 0, 0),(2020,12,29, 0, 0),(2021, 1,29, 0, 0),
                              (2021, 3,29, 0, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)


def test_cron_simple_combination():
    # Field combination, requiring an increment of the first 'any' field
    tests = [
        ('12 2 * * *',       ((2019,10, 4, 2,12),(2019,10, 5, 2,12),(2019,10, 6, 2,12))),
        ('7 5 1 * *',        ((2019,11, 1, 5, 7),(2019,12, 1, 5, 7),(2020, 1, 1, 5, 7))),
        ('7 5 * * 2',        ((2019,10, 8, 5, 7),(2019,10,15, 5, 7),(2019,10,22, 5, 7))),
        ('42 23 25 3 *',     ((2020, 3,25,23,42),(2021, 3,25,23,42),(2022, 3,25,23,42))),
        ('0 0 * 8 5',        ((2020, 8, 7, 0, 0),(2020, 8,14, 0, 0),(2020, 8,21, 0, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_multiplicator_field():
    # Single field, with multiplicator
    tests = [
        ('*/26 * * * *',     ((2019,10, 3,12,52),(2019,10, 3,13,00),(2019,10, 3,13,26))),
        ('* */7 * * *',      ((2019,10, 3,14, 0),(2019,10, 3,14, 1),(2019,10, 3,14, 2))),
        ('3 */7 * * *',      ((2019,10, 3,14, 3),(2019,10, 3,21, 3),(2019,10, 4, 0, 3))),
        ('* * */10 * *',     ((2019,10,11, 0, 0),(2019,10,11, 0, 1),(2019,10,11, 0, 2))),
        ('18 * */10 * *',    ((2019,10,11, 0,18),(2019,10,11, 1,18),(2019,10,11, 2,18))),
        ('* 3 */10 * *',     ((2019,10,11, 3, 0),(2019,10,11, 3, 1),(2019,10,11, 3, 2))),
        ('8 3 */10 * *',     ((2019,10,11, 3, 8),(2019,10,21, 3, 8),(2019,10,31, 3, 8),(2019,11, 1, 3, 8))),
        ('* * * * */3',      ((2019,10, 5, 0, 0),(2019,10, 5, 0, 1),(2019,10, 5, 0, 2))),
        ('19 * * * */1',     ((2019,10, 3,13,19),(2019,10, 3,14,19),(2019,10, 3,15,19))),
        ('59 23 * * */2',    ((2019,10, 3,23,59),(2019,10, 5,23,59),(2019,10, 6,23,59))),
        ('* * * */11 *',     ((2019,12, 1, 0, 0),(2019,12, 1, 0, 1),(2019,12, 1, 0, 2))),
        ('* 13 * */3 *',     ((2019,10, 3,13, 0),(2019,10, 3,13, 1),(2019,10, 3,13, 2))),
        ('12 * 8 */7 *',     ((2020, 1, 8, 0,12),(2020, 1, 8, 1,12),(2020, 1, 8, 2,12))),
        ('30 21 1 */5 *',    ((2019,11, 1,21,30),(2020, 1, 1,21,30),(2020, 6, 1,21,30))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_multiplicator_out_of_range():
    # Out of range multiplicator
    tests = [
        ('*/132 * * * *',    ((2019,10, 3,13, 0),(2019,10, 3,14, 0),(2019,10, 3,15, 0))),
        ('0 */2154 * * *',   ((2019,10, 4, 0, 0),(2019,10, 5, 0, 0),(2019,10, 6, 0, 0))),
        ('0 0 */85 * *',     ((2019,11, 1, 0, 0),(2019,12, 1, 0, 0),(2020, 1, 1, 0, 0))),
        ('0 0 * * */87450',  ((2019,10, 6, 0, 0),(2019,10,13, 0, 0),(2019,10,20, 0, 0))),
        ('0 0 1 */13 *',     ((2020, 1, 1, 0, 0),(2021, 1, 1, 0, 0),(2022, 1, 1, 0, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_multiplicator_combination():
    # Field combination, with multiplicators
    tests = [
        ('*/53 */2 * * *',          ((2019,10, 3,12,53),(2019,10, 3,14,00),(2019,10, 3,14,53))),
        ('*/35 */22 */8 * *',       ((2019,10, 9, 0, 0),(2019,10, 9, 0,35),(2019,10, 9,22, 0),
                                     (2019,10, 9,22,35),(2019,10,17, 0, 0),(2019,10,17, 0,35))),
        ('*/46 */18 * * */5',       ((2019,10, 4, 0, 0),(2019,10, 4, 0,46),(2019,10, 4,18, 0),
                                     (2019,10, 4,18,46),(2019,10, 6, 0, 0),(2019,10, 6, 0,46))),
        ('50 */16 */30 */4 *',      ((2020, 1, 1, 0,50),(2020, 1, 1,16,50),(2020, 1,31, 0,50),
                                     (2020, 1,31,16,50),(2020, 5, 1, 0,50),(2020, 5, 1,16,50),
                                     (2020, 5,31, 0,50),(2020, 5,31,16,50),(2020, 9, 1, 0,50),
                                     (2020, 9, 1,16,50),(2021, 1, 1, 0,50),(2021, 1, 1,16,50))),
    ]
    for t in tests:
        check_cron_expression(*t)


def test_cron_dom_dow():
    # Days in month vs days of week
    tests = [
        # - dom and dow has same first match
        ('0 0 5 * 6',       ((2019,10, 5, 0, 0),(2019,10,12, 0, 0),(2019,10,19, 0, 0),
                             (2019,10,26, 0, 0),(2019,11, 2, 0, 0),(2019,11, 5, 0, 0))),
        ('0 0 */2 * */6',   ((2019,10, 5, 0, 0),(2019,10, 6, 0, 0),(2019,10, 7, 0, 0),
                             (2019,10, 9, 0, 0),(2019,10,11, 0, 0),(2019,10,12, 0, 0))),
        # - dom has a first match before dow
        ('0 0 4 * 0',       ((2019,10, 4, 0, 0),(2019,10, 6, 0, 0),(2019,10,13, 0, 0))),
        # - dow has a first match before dom
        ('0 0 10 * 2',      ((2019,10, 8, 0, 0),(2019,10,10, 0, 0),(2019,10,15, 0, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_range_field():
    # Single field, ranges, with current time either before range, in range, or after range
    tests = [
        ('25-26 * * * *',   ((2019,10, 3,13,25),(2019,10, 3,13,26),(2019,10, 3,14,25))),
        ('48-51 * * * *',   ((2019,10, 3,12,50),(2019,10, 3,12,51),(2019,10, 3,13,48))),
        ('55-58 * * * *',   ((2019,10, 3,12,55),(2019,10, 3,12,56),(2019,10, 3,12,57),
                             (2019,10, 3,12,58),(2019,10, 3,13,55),(2019,10, 3,13,56))),
        ('50 1-3 * * *',    ((2019,10, 4, 1,50),(2019,10, 4, 2,50),(2019,10, 4, 3,50),
                             (2019,10, 5, 1,50),(2019,10, 5, 2,50),(2019,10, 5, 3,50))),
        ('55 3-13 * * *',   ((2019,10, 3,12,55),(2019,10, 3,13,55),(2019,10, 4, 3,55))),
        ('50 15-16 * * *',  ((2019,10, 3,15,50),(2019,10, 3,16,50),(2019,10, 4,15,50))),
        ('12 12 1-2 * *',   ((2019,11, 1,12,12),(2019,11, 2,12,12),(2019,12, 1,12,12))),
        ('50 2 2-4 * *',    ((2019,10, 4, 2,50),(2019,11, 2, 2,50),(2019,11, 3, 2,50),
                             (2019,11, 4, 2,50),(2019,12, 2, 2,50),(2019,12, 3, 2,50))),
        ('0 0 21-22 * *',   ((2019,10,21, 0, 0),(2019,10,22, 0, 0),(2019,11,21, 0, 0))),
        ('12 12 * * 0-1',   ((2019,10, 6,12,12),(2019,10, 7,12,12),(2019,10,13,12,12))),
        ('50 22 * * 1-5',   ((2019,10, 3,22,50),(2019,10, 4,22,50),(2019,10, 7,22,50))),
        ('0 0 * * 5-6',     ((2019,10, 4, 0, 0),(2019,10, 5, 0, 0),(2019,10,11, 0, 0))),
        ('12 12 12 3-4 *',  ((2020, 3,12,12,12),(2020, 4,12,12,12),(2021, 3,12,12,12))),
        ('50 22 31 6-10 *', ((2019,10,31,22,50),(2020, 7,31,22,50),(2020, 8,31,22,50))),
        ('0 0 1 11-12 *',   ((2019,11, 1, 0, 0),(2019,12, 1, 0, 0),(2020,11, 1, 0, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_range_start_equal_end():
    # Ranges with same start and end
    tests = [
        ('59-59 * * * *',   ((2019,10, 3,12,59),(2019,10, 3,13,59),(2019,10, 3,14,59))),
        ('*/31 5-5 * * *',  ((2019,10, 4, 5, 0),(2019,10, 4, 5,31),(2019,10, 5, 5, 0))),
        ('36 21 30-30 * *', ((2019,10,30,21,36),(2019,11,30,21,36),(2019,12,30,21,36),
                             (2020, 1,30,21,36),(2020, 3,30,21,36),(2020, 4,30,21,36))),
        ('1 2 * * 0-0',     ((2019,10, 6, 2, 1),(2019,10,13, 2, 1),(2019,10,20, 2, 1))),
        ('0 23 1 12-12 *',  ((2019,12, 1,23, 0),(2020,12, 1,23, 0),(2021,12, 1,23, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_range_combination():
    # Field combination, with ranges
    tests = [
        ('1-2 3-4 5-6 7-8 *',   ((2020, 7, 5, 3, 1),(2020, 7, 5, 3, 2),(2020, 7, 5, 4, 1),
                                 (2020, 7, 5, 4, 2),(2020, 7, 6, 3, 1),(2020, 7, 6, 3, 2),
                                 (2020, 7, 6, 4, 1),(2020, 7, 6, 4, 2),(2020, 8, 5, 3, 1),
                                 (2020, 8, 5, 3, 2),(2020, 8, 5, 4, 1),(2020, 8, 5, 4, 2),
                                 (2020, 8, 6, 3, 1),(2020, 8, 6, 3, 2),(2020, 8, 6, 4, 1),
                                 (2020, 8, 6, 4, 2),(2021, 7, 5, 3, 1))),
        ('0 10-11 * 11-11 2-3', ((2019,11, 5,10, 0),(2019,11, 5,11, 0),(2019,11, 6,10, 0),
                                 (2019,11, 6,11, 0),(2019,11,12,10, 0),(2019,11,12,11, 0),
                                 (2019,11,13,10, 0),(2019,11,13,11, 0),(2019,11,19,10, 0),
                                 (2019,11,19,11, 0),(2019,11,20,10, 0),(2019,11,20,11, 0),
                                 (2019,11,26,10, 0),(2019,11,26,11, 0),(2019,11,27,10, 0),
                                 (2019,11,27,11, 0),(2020,11, 3,10, 0),(2020,11, 3,11, 0),
                                 (2020,11, 4,10, 0),(2020,11, 4,11, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_range_and_multiplicator():
    # Ranges with multiplicators
    tests = [
        ('2-20/7 * * * *',      ((2019,10, 3,13, 2),(2019,10, 3,13, 9),(2019,10, 3,13,16),(2019,10, 3,14, 2))),
        ('0 1-2/20 * * *',      ((2019,10, 4, 1, 0),(2019,10, 5, 1, 0),(2019,10, 6, 1, 0))),
        ('12 12 25-31/6 * *',   ((2019,10,25,12,12),(2019,10,31,12,12),(2019,11,25,12,12),(2019,12,25,12,12))),
        ('14 14 14 * 0-5/4',    ((2019,10, 3,14,14),(2019,10, 6,14,14),(2019,10,10,14,14),(2019,10,13,14,14))),
        ('14 14 14 1-4/2 *',    ((2020, 1,14,14,14),(2020, 3,14,14,14),(2021, 1,14,14,14),(2021, 3,14,14,14))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_list_field():
    # Single field, lists
    #TODO manage lists in wrong order (simple reordering at read time)
    #TODO manage lists with same element twice (reordering en imposant unicite)
    tests = [
        ('2,3,7 * * * *',       ((2019,10, 3,13, 2),(2019,10, 3,13, 3),(2019,10, 3,13, 7),(2019,10, 3,14, 2))),
        ('3,2,7 * * * *',       ((2019,10, 3,13, 2),(2019,10, 3,13, 3),(2019,10, 3,13, 7),(2019,10, 3,14, 2))),
        ('51 2,11,13 * * *',    ((2019,10, 3,13,51),(2019,10, 4, 2,51),(2019,10, 4,11,51))),
        ('51 2,13,13,11,2 * * *',    ((2019,10, 3,13,51),(2019,10, 4, 2,51),(2019,10, 4,11,51))),
        ('3 3 21,31 * *',       ((2019,10,21, 3, 3),(2019,10,31, 3, 3),(2019,11,21, 3, 3),(2019,12,21, 3, 3))),
        ('3 3 31,21 * *',       ((2019,10,21, 3, 3),(2019,10,31, 3, 3),(2019,11,21, 3, 3),(2019,12,21, 3, 3))),
        ('5 4 * * 0,3',         ((2019,10, 6, 4, 5),(2019,10, 9, 4, 5),(2019,10,13, 4, 5),(2019,10,16, 4, 5))),
        ('5 4 * * 3,0',         ((2019,10, 6, 4, 5),(2019,10, 9, 4, 5),(2019,10,13, 4, 5),(2019,10,16, 4, 5))),
        ('0 10 31 1,2,10 4',   ((2019,10,10,10, 0),(2019,10,17,10, 0),(2019,10,24,10, 0),(2019,10,31,10, 0),
                                 (2020, 1, 2,10, 0),(2020, 1, 9,10, 0),(2020, 1,16,10, 0),(2020, 1,23,10, 0),
                                 (2020, 1,30,10, 0),(2020, 1,31,10, 0),(2020, 2, 6,10, 0),(2020, 2,13,10, 0),
                                 (2020, 2,20,10, 0),(2020, 2,27,10, 0),(2020,10, 1,10, 0))),
        ('0 10 31 10,2,1 4',   ((2019,10,10,10, 0),(2019,10,17,10, 0),(2019,10,24,10, 0),(2019,10,31,10, 0),
                                 (2020, 1, 2,10, 0),(2020, 1, 9,10, 0),(2020, 1,16,10, 0),(2020, 1,23,10, 0),
                                 (2020, 1,30,10, 0),(2020, 1,31,10, 0),(2020, 2, 6,10, 0),(2020, 2,13,10, 0),
                                 (2020, 2,20,10, 0),(2020, 2,27,10, 0),(2020,10, 1,10, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)

def test_cron_list_combination():
    tests = [
        # Field combination, with lists
        ('1,2,3 0 11,12 1 *',   ((2020, 1,11, 0, 1),(2020, 1,11, 0, 2),(2020, 1,11, 0, 3),
                                 (2020, 1,12, 0, 1),(2020, 1,12, 0, 2),(2020, 1,12, 0, 3),
                                 (2021, 1,11, 0, 1),(2021, 1,11, 0, 2),(2021, 1,11, 0, 3))),
        ('0 0 25,26,28 2,3 1,5', ((2020, 2, 3, 0, 0),(2020, 2, 7, 0, 0),(2020, 2,10, 0, 0),
                                  (2020, 2,14, 0, 0),(2020, 2,17, 0, 0),(2020, 2,21, 0, 0),
                                  (2020, 2,24, 0, 0),(2020, 2,25, 0, 0),(2020, 2,26, 0, 0),
                                  (2020, 2,28, 0, 0),(2020, 3, 2, 0, 0),(2020, 3, 6, 0, 0),
                                  (2020, 3, 9, 0, 0),(2020, 3,13, 0, 0),(2020, 3,16, 0, 0),
                                  (2020, 3,20, 0, 0),(2020, 3,23, 0, 0),(2020, 3,25, 0, 0),
                                  (2020, 3,26, 0, 0),(2020, 3,27, 0, 0),(2020, 3,28, 0, 0),
                                  (2020, 3,30, 0, 0),(2021, 2, 1, 0, 0))),
    ]
    for t in tests:
        check_cron_expression(*t)


# Never-matching expressions
def test_cron_never_matching_expressions():
    start = datetime.datetime(2020,2,29,0,0,1)
    ce = cronwhen.cron.CronExpression('0 0 31 2 *')
    assert(ce.getNextOccurence(start) is None)
    ce = cronwhen.cron.CronExpression('0 0 29 2 *')
    expected_occurrence = datetime.datetime(2024,2,29)
    assert(ce.getNextOccurence(start) == expected_occurrence)

#TODO
# Ill-formed expressions
