# -*- coding: utf-8 -*- 
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from plone.namedfile.field import NamedBlobImage
from plone import namedfile
from Products.CMFPlone.utils import safe_unicode
import base64
from db.connect.browser.views import SqlObj
import datetime
import csv


class PublicizePressure(BrowserView):
    template = ViewPageTemplateFile('template/publicize_pressure.pt')
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return 
        return self.template()

class TestPressure(BrowserView):
    template = ViewPageTemplateFile('template/test_pressure.pt')
    def __call__(self):
        if api.user.is_anonymous():
            self.request.response.redirect('%s/user_login'%api.portal.get().absolute_url())
            return 
        return self.template()


class CalculatePressure(BrowserView):
    template = ViewPageTemplateFile('template/result_pressure.pt')
    def __call__(self):
        request = self.request
        answer1_1 = request.get('answer1_1')
        answer1_2 = request.get('answer1_2')
        answer1_3 = request.get('answer1_3')
        answer1_4 = request.get('answer1_4')
        answer1_5 = request.get('answer1_5')
        answer1_6 = request.get('answer1_6')
        answer2_1 = request.get('answer2_1')
        answer2_2 = request.get('answer2_2')
        answer2_3 = request.get('answer2_3')
        answer2_4 = request.get('answer2_4')
        answer2_5 = request.get('answer2_5')
        answer2_6 = request.get('answer2_6')
        answer2_7 = request.get('answer2_7')
        personal_pressure = (int(answer1_1) + int(answer1_2) + int(answer1_3) + int(answer1_4) + int(answer1_5) + int(answer1_6)) / 6
        work_pressure = (int(answer2_1) + int(answer2_2) + int(answer2_3) + int(answer2_4) + int(answer2_5) + int(answer2_6) + int(answer2_7)) / 7

        user = api.user.get_current().getUserName()
        execSql  = SqlObj()

        execStr = """INSERT INTO pressure(user, personal_pressure, work_pressure) 
                VALUES('{}', '{}', '{}')""".format(user, personal_pressure, work_pressure)
        execSql.execSql(execStr)

        self.personal_pressure = personal_pressure
        self.work_pressure = work_pressure

        return self.template()


class TotalPressureResult(BrowserView):
    template = ViewPageTemplateFile('template/total_pressure_result.pt')
    def __call__(self):
        roles = api.user.get_current().getRoles()
        if 'Manager' not in roles:
            return '????????????'
        else:
            execSql = SqlObj()
            execStr = """SELECT * FROM `pressure` ORDER BY time"""
            result = execSql.execSql(execStr)
            data = []
            users = api.user.get_users()
            all_user = {}
            for user in users:
                email = user.getProperty('email')
                fullname = user.getProperty('fullname')
                en_name = user.getProperty('en_name')
                user_id = user.getProperty('user_id')
                all_user[email] = {
                    'fullname': fullname,
                    'en_name': en_name,
                    'user_id': user_id
                }
            for item in result:
                tmp = dict(item)
                user = tmp['user']
                if all_user.has_key(user):
                    fullname = all_user[user]['fullname']
                    en_name = all_user[user]['en_name']
                    user_id = all_user[user]['user_id']
                    personal_pressure = tmp['personal_pressure']
                    work_pressure = tmp['work_pressure']
                    time = tmp['time'].strftime('%Y/%m/%d  %H:%M')
                    data.append([user, personal_pressure, work_pressure, time, fullname, en_name, user_id])
            self.data = data
        return self.template()

class Create(BrowserView):
    def __call__(self):
        request = self.request
        portal = api.portal.get()
        alsoProvides(request, IDisableCSRFProtection)

        file = open('/home/henryc/aa.csv', 'r')
        csv_data = csv.reader(file)
        for data in csv_data:
            try:
                en_name = data[1].split('\xef\xbc\x88')[0]
                ch_name = data[1].split('\xef\xbc\x88')[1].split('\xef\xbc\x89')[0]
                user_id = data[0]
                email = data[2].strip()
                if data[3] == 'Taipei':
                    location = '??????'
                elif data[3] == 'Taichung':
                    location = '??????'
                elif data[3] == 'Kaohsiung':
                    location = '??????'

                properties = dict(
                    fullname=ch_name,
                    location=location,
                    en_name=en_name,
                    user_id=user_id
                )
                user = api.user.create(
                    email=email,
                    password=user_id,
                    properties=properties,
                )
                print ch_name
            except:
                import pdb;pdb.set_trace()


class DeleteUser(BrowserView):
    def __call__(self):
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)

        users = api.user.get_users()
        for user in users:
            api.user.delete(user=user)
        return
        file = open('/hpe/aa.csv', 'r')
        csv_data = csv.reader(file)
        for data in csv_data:
            try:
                api.user.delete(username=data[3])
            except:
                pass



class CheckUsers(BrowserView):
    def __call__(self):
        users = api.user.get_users()
        file = open('/home/henryc/ccc.csv', 'r')
        user_list = []
        count = 0
        for user in users:
            email = user.getProperty('email')
            user_list.append(email)
        for item in csv.reader(file):
            if item[6] not in user_list:
                count += 1
                print item[6]
                import pdb;pdb.set_trace()
        if count == 0:
            print 'all pass~~~~~~~~~~~~'



class AntiCancerView(BrowserView):
    template = ViewPageTemplateFile('template/anti_cancer_view.pt')
    def __call__(self):
        return self.template()
