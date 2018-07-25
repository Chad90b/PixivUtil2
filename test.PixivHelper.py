#!/c/Python27/python.exe
# -*- coding: UTF-8 -*-
from __future__ import print_function

import PixivHelper
import os
import unittest
from PixivModelWhiteCube import PixivImage
from PixivModel import PixivArtist
import PixivConfig
from BeautifulSoup import BeautifulSoup

import pytest


class TestPixivHelper(unittest.TestCase):
    currPath = unicode(os.path.abspath('.'))
    PixivHelper.GetLogger()

    def testSanitizeFilename(self):
        rootDir = '.'
        filename = u'12345.jpg'
        currentDir = os.path.abspath('.')
        expected = currentDir + os.sep + filename

        result = PixivHelper.sanitizeFilename(filename, rootDir)

        self.assertEqual(result, expected)
        self.assertTrue(len(result) < 255)

    def testSanitizeFilename2(self):
        rootDir = '.'
        filename = u'12345.jpg'
        currentDir = os.path.abspath('.')
        expected = currentDir + os.sep + filename

        result = PixivHelper.sanitizeFilename(filename, rootDir)

        self.assertEqual(result, expected)
        self.assertTrue(len(result) < 255)

    @pytest.mark.xfail
    def testCreateMangaFilename(self):
        p = open('./test/test-image-manga.htm', 'r')
        page = BeautifulSoup(p.read())
        imageInfo = PixivImage(28820443, page)
        imageInfo.imageCount = 100
        page.decompose()
        del page
        # print(imageInfo.PrintInfo())
        nameFormat = '%member_token% (%member_id%)\%urlFilename% %page_number% %works_date_only% %works_res% %works_tools% %title%'

        expected = unicode(u'ffei (554800)\\28865189_p0 001 7-23-2012 複数枚投稿 2P Photoshop C82おまけ本 「沙耶は俺の嫁」サンプル.jpg')
        result = PixivHelper.makeFilename(nameFormat, imageInfo, artistInfo=None, tagsSeparator=' ', fileUrl='http://i2.pixiv.net/img26/img/ffei/28865189_p0.jpg')
        # print(result)
        self.assertEqual(result, expected)

        expected = unicode(u'ffei (554800)\\28865189_p14 015 7-23-2012 複数枚投稿 2P Photoshop C82おまけ本 「沙耶は俺の嫁」サンプル.jpg')
        result = PixivHelper.makeFilename(nameFormat, imageInfo, artistInfo=None, tagsSeparator=' ', fileUrl='http://i2.pixiv.net/img26/img/ffei/28865189_p14.jpg')
        # print(result)
        self.assertEqual(result, expected)

        expected = unicode(u'ffei (554800)\\28865189_p921 922 7-23-2012 複数枚投稿 2P Photoshop C82おまけ本 「沙耶は俺の嫁」サンプル.jpg')
        result = PixivHelper.makeFilename(nameFormat, imageInfo, artistInfo=None, tagsSeparator=' ', fileUrl='http://i2.pixiv.net/img26/img/ffei/28865189_p921.jpg')
        # print(result)
        self.assertEqual(result, expected)

    @pytest.mark.xfail
    def testCreateFilenameUnicode(self):
        p = open('./test/test-image-unicode.htm', 'r')
        page = BeautifulSoup(p.read())
        imageInfo = PixivImage(2493913, page)
        page.decompose()
        del page

        nameFormat = '%member_token% (%member_id%)\%urlFilename% %works_date_only% %works_res% %works_tools% %title%'
        expected = unicode(u'balzehn (267014)\\2493913 12-23-2008 852x1200 Photoshop SAI つけペン アラクネのいる日常２.jpg')
        result = PixivHelper.makeFilename(nameFormat, imageInfo, artistInfo=None, tagsSeparator=' ', fileUrl='http://i2.pixiv.net/img16/img/balzehn/2493913.jpg')
        # print(result)
        self.assertEqual(result, expected)

    def testcreateAvatarFilenameFormatNoSubfolderNoRootDir(self):
        p = open('./test/test-helper-avatar-name.htm', 'r')
        page = BeautifulSoup(p.read())
        artist = PixivArtist(mid=1107124, page=page)
        targetDir = ''
        # change the config value
        _config = PixivConfig.PixivConfig()
        _config.avatarNameFormat = ''
        _config.filenameFormat = '%image_id% - %title%'
        _config.tagsSeparator = ' '
        _config.tagsLimit = 0
        PixivHelper.setConfig(_config)
        filename = PixivHelper.createAvatarFilename(artist, targetDir)
        self.assertEqual(filename, self.currPath + os.sep + u'folder.jpg')

    def testcreateAvatarFilenameFormatWithSubfolderNoRootDir(self):
        p = open('./test/test-helper-avatar-name.htm', 'r')
        page = BeautifulSoup(p.read())
        artist = PixivArtist(mid=1107124, page=page)
        targetDir = ''
        _config = PixivConfig.PixivConfig()
        _config.avatarNameFormat = ''
        _config.filenameFormat = '%member_token% (%member_id%)\%image_id% - %title% - %tags%'
        _config.tagsSeparator = ' '
        _config.tagsLimit = 0
        PixivHelper.setConfig(_config)
        filename = PixivHelper.createAvatarFilename(artist, targetDir)
        self.assertEqual(filename, self.currPath + os.sep + u'kirabara29 (1107124)\\folder.jpg')

    def testcreateAvatarFilenameFormatNoSubfolderWithRootDir(self):
        p = open('./test/test-helper-avatar-name.htm', 'r')
        page = BeautifulSoup(p.read())
        artist = PixivArtist(mid=1107124, page=page)
        targetDir = os.path.abspath('.')
        _config = PixivConfig.PixivConfig()
        _config.avatarNameFormat = ''
        _config.filenameFormat = '%image_id% - %title%'
        _config.tagsSeparator = ' '
        _config.tagsLimit = 0
        filename = PixivHelper.createAvatarFilename(artist, targetDir)
        self.assertEqual(filename, targetDir + os.sep + u'folder.jpg')

    def testcreateAvatarFilenameFormatWithSubfolderWithRootDir(self):
        p = open('./test/test-helper-avatar-name.htm', 'r')
        page = BeautifulSoup(p.read())
        artist = PixivArtist(mid=1107124, page=page)
        targetDir = os.path.abspath('.')
        _config = PixivConfig.PixivConfig()
        _config.avatarNameFormat = ''
        _config.filenameFormat = '%member_token% (%member_id%)\%R-18%\%image_id% - %title% - %tags%'
        _config.tagsSeparator = ' '
        _config.tagsLimit = 0
        filename = PixivHelper.createAvatarFilename(artist, targetDir)
        self.assertEqual(filename, targetDir + os.sep + u'kirabara29 (1107124)\\folder.jpg')

    def testcreateAvatarFilenameFormatNoSubfolderWithCustomRootDir(self):
        p = open('./test/test-helper-avatar-name.htm', 'r')
        page = BeautifulSoup(p.read())
        artist = PixivArtist(mid=1107124, page=page)
        targetDir = 'C:\\images'
        _config = PixivConfig.PixivConfig()
        _config.avatarNameFormat = ''
        _config.filenameFormat = '%image_id% - %title%'
        _config.tagsSeparator = ' '
        _config.tagsLimit = 0
        filename = PixivHelper.createAvatarFilename(artist, targetDir)
        self.assertEqual(filename, u'C:\\images\\folder.jpg')

    def testcreateAvatarFilenameFormatWithSubfolderWithCustomRootDir(self):
        p = open('./test/test-helper-avatar-name.htm', 'r')
        page = BeautifulSoup(p.read())
        artist = PixivArtist(mid=1107124, page=page)
        targetDir = 'C:\\images'
        _config = PixivConfig.PixivConfig()
        _config.avatarNameFormat = ''
        _config.filenameFormat = '%member_token% (%member_id%)\%R-18%\%image_id% - %title% - %tags%'
        _config.tagsSeparator = ' '
        _config.tagsLimit = 0
        filename = PixivHelper.createAvatarFilename(artist, targetDir)
        self.assertEqual(filename, u'C:\\images\\kirabara29 (1107124)\\folder.jpg')

    def testParseLoginError(self):
        p = open('./test/test-login-error.htm', 'r')
        page = BeautifulSoup(p.read())
        r = page.findAll('span', attrs={'class': 'error'})
        self.assertTrue(len(r) > 0)
        self.assertEqual(u'Please ensure your pixiv ID, email address and password is entered correctly.', r[0].string)

    def testParseLoginForm(self):
        p = open('./test/test-login-form.html', 'r')
        page = BeautifulSoup(p.read())
        r = page.findAll('form', attrs={'action': '/login.php'})
        # print(r)
        self.assertTrue(len(r) > 0)


if __name__ == '__main__':
        # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPixivHelper)
    unittest.TextTestRunner(verbosity=5).run(suite)
