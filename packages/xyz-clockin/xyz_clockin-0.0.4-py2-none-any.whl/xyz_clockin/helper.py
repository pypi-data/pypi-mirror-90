# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from datetime import timedelta
from xyz_util.dateutils import format_the_date

def range_date(bd, ed, interval=1):
    bd = format_the_date(bd)
    ed = format_the_date(ed)
    d = bd
    while d <= ed:
        yield d
        d += timedelta(days=interval)


def gen_session_days(session):
    rs = []
    for d in range_date(session.begin_time, session.end_time):
        rs.append(dict(date=d.isoformat()[:10], items=[]))
    return rs


def array_merge(a1, a2, field):
    l1 = len(a1)
    l2 = len(a2)
    i1 = 0
    i2 = 0
    ar = []
    # print a2
    while i1 < l1 and i2 < l2:
        if a1[i1][field] == a2[i2][field]:
            ar.append(a2[i2])
            i1 += 1
            i2 += 1
        elif a1[i1][field] < a2[i2][field]:
            ar.append(a1[i1])
            i1 += 1
        else:
            ar.append(a2[i2])
            i2 += 1
    if i1<l1:
        ar += a1[i1:]
    if i2<l2:
        ar += a2[i2:]
    return ar

def append(a1, items):
    ps = a1[-1]['items']
    m={}
    for d in a1:
        for a in d['items']:
            k=(a['model'], a['id'])
            m[k]=a
    for a in items:
        k = (a['model'], a['id'])
        if k in m:
            continue
        ps.append(a)


def gen_session_items(session):
    days = gen_session_days(session)
    rs = array_merge(days, session.items, 'date')
    from xyz_exam.models import Paper
    from django.contrib.contenttypes.models import ContentType
    ct = ContentType.objects.get_for_model(session)
    papers = Paper.objects.filter(owner_type=ct, owner_id=session.id)
    items = [dict(name=p.title, model='exam.paper', id=p.id) for p in papers]
    append(rs, items)
    return rs
