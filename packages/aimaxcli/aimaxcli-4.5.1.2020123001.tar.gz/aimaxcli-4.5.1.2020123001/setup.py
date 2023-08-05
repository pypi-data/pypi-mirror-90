#!/usr/bin/env python
from setuptools import setup, find_packages
PROJECT = 'aimaxcli'

# Change docs/sphinx/conf.py too!
VERSION = '4.5.1.2020123001'



try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='AIMax python commands client',
    long_description=long_description,

    author='Gavin Li',
    author_email='gavin_li@amaxgs.com',

    #url='https://github.com/openstack/cliff',
    #download_url='https://github.com/openstack/cliff/tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff','requests'],
    #requests json
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.json']
    },
    entry_points={
        #'console_scripts': [
        #    'cliffdemo = cliffdemo.main:main' 'as = aimaxcmd.main:main'
        #],
        'console_scripts': [
            'aimax= aimaxcmd.main:main'
        ],
        'aimax.client': [
            # 'simple = cliffdemo.simple:Simple',
            # 'two_part = cliffdemo.simple:Simple',
            # 'error = cliffdemo.simple:Error',
            # 'list files = cliffdemo.list:Files',
            # 'files = cliffdemo.list:Files',
            # 'file = cliffdemo.show:File',
            # 'show file = cliffdemo.show:File',
            # 'unicode = cliffdemo.encoding:Encoding',
            # 'hooked = cliffdemo.hook:Hooked',
            # 'linked = cliffdemo.hook:Linked',
            'connect = aimaxcmd.cmds_base:Connect',#
            'disconnect = aimaxcmd.cmds_base:Disconnect',#

            #=======ClusterNodeProxyImpl begin============================================
            'node list = aimaxcmd.cmds_node:NodeList',# getNodeList
            'node info = aimaxcmd.cmds_node:NodeInfo',# getSingleNode
            #=======ClusterNodeProxyImpl end============================================

            #=======GroupProxyImpl begin============================================
            'group list = aimaxcmd.cmds_user:GroupList',# listAllGroups
            'group info = aimaxcmd.cmds_user:GroupInfo',# getGroupByName
            'group add = aimaxcmd.cmds_user:GroupAdd',# addGroup
            'group delete = aimaxcmd.cmds_user:GroupDelete',# deleteGroup
            'role list = aimaxcmd.com_list:CommonList',# listAllRoles
            'group update = aimaxcmd.com_list:CommonPut',# updateGroup
            #=======GroupProxyImpl end============================================

            #=======ImagesProxyImpl begin============================================
            'nvidia adduser = aimaxcmd.com_list:CommonAdd',# addNividiaUser
            'nvidia update = aimaxcmd.com_list:CommonPut',# updateNividiaUser
            'nvidia get = aimaxcmd.com_list:CommonShow',# getNividiaUser
            'nvidia showImages = aimaxcmd.com_list:CommonShow',# showNividiaImages
            'nvidia getVersion = aimaxcmd.com_list:CommonShow',# getNividiaVersion
            'nvidia pullImage = aimaxcmd.com_list:CommonAdd',# pullNividiaImage
            'nvidia pullEventInfo = aimaxcmd.com_list:CommonShow',# pullNiviImgEventInfo
            'image getPublic  = aimaxcmd.com_list:CommonShow',# getPublicImages
            'image getByUsername  = aimaxcmd.com_list:CommonShow',# getSomeoneImages
            'image getRepositories  = aimaxcmd.com_list:CommonShow',# getRepositories
            'image getVersion  = aimaxcmd.com_list:CommonShow',# getVersion
            'image showAli  = aimaxcmd.com_list:CommonShow',# showAliImages
            'image getAliIVersion  = aimaxcmd.com_list:CommonShow',# getAliImageVersion
            'image pushTxt  = aimaxcmd.com_list:CommonShow',# pushImageTxt
            'image getInfoDetect  = aimaxcmd.com_list:CommonShow',# getImageInfoDetect
            'image getInfo  = aimaxcmd.com_list:CommonShow',# getImageInfomation
            'image cancel  = aimaxcmd.com_list:CommonShow',# cancelImageInfomation
            'container createAndStart  = aimaxcmd.com_list:CommonAdd',# createAndStartContainer
            'container commit  = aimaxcmd.com_list:CommonAdd',# commitContainer
            'container remove  = aimaxcmd.com_list:Commondelete',# removeContainer
            'image make  = aimaxcmd.com_list:CommonAdd',# makeImage
            'image search  = aimaxcmd.com_list:CommonShow',# searchImage
            'image pull  = aimaxcmd.com_list:CommonAdd',# pullImage
            # pullImageProgress 进度
            # makeImageProgress 进度
            'image list =aimaxcmd.com_list:CommonList',# listAllImages 获取镜像列表
            'image forjob =aimaxcmd.com_list:CommonList',# listImagesForjob 根据job获取适配的镜像
            'image disclose =aimaxcmd.com_list:CommonAdd',# discloseImage 公开镜像
            'image syncImage =aimaxcmd.com_list:CommonAdd',# syncImage 同步镜像
            'image share =aimaxcmd.com_list:CommonAdd',# shareImage 分享镜像
            'image shareObj =aimaxcmd.com_list:CommonList',# getShareObjs 获取共享对象
            'image getshare =aimaxcmd.com_list:CommonShow',# getShareImage 查看某用户的分享镜像列表
            'image cancelShare =aimaxcmd.com_list:CommonDelete',# cancelShare 取消分享镜像
            'image getImageByName =aimaxcmd.com_list:CommonShow',# getImageByName 根据名称获取镜像
            'image doNewTags =aimaxcmd.com_list:CommonAdd',# doNewTags 打标签
            'image uploadTar =aimaxcmd.com_list:CommonUpload',# uploadTarImage 文件上传具体实现方法（单文件上传）
            'image uploadDockfile =aimaxcmd.com_list:CommonUpload',# uploadDockfileImage 上传dokcerfile
            'image delete =aimaxcmd.com_list:CommonDelete',# deleteImage 删除镜像
            'image isContainerMaking =aimaxcmd.com_list:CommonShow',# isContainerMaking
            #=======ImagesProxyImpl end============================================

            #=======JobProxyImpl begin============================================
            'job createJob =aimaxcmd.com_list:CommonAdd',# create
            'job createDeployment =aimaxcmd.com_list:CommonAdd',# createDeployment
            'job list =aimaxcmd.com_list:CommonList',# list
            'job listDeployment =aimaxcmd.com_list:CommonList',# listDeployment 获取模型部署列表
            'job info =aimaxcmd.com_list:CommonShow',# job 获取任务信息
            'job removeJob =aimaxcmd.com_list:CommonDelete',# remove 移除任务
            'job removeDeploymentAndSVC =aimaxcmd.com_list:CommonDelete',# removeDeploymentAndSVC 移除任务
            'job pause =aimaxcmd.com_list:CommonPut',# pause 挂起任务
            'job resume =aimaxcmd.com_list:CommonPut',# resume 重新开始任务
            'job pauseDeployment =aimaxcmd.com_list:CommonPut',# pauseDeployment 挂起部署任务
            'job resumeDeployment =aimaxcmd.com_list:CommonPut',# resumeDeployment 重新开始部署任务
            'job getgpuList =aimaxcmd.com_list:CommonList',# getgpuList 创建任务前 获取 gpu类型列表
            'job getErrorInfo =aimaxcmd.com_list:CommonShow',# getErrorInfo 获取任务错误信息
            'job getErrorList =aimaxcmd.com_list:CommonList',# getErrorList 获取任务错误信息列表
            'job getPredictResult =aimaxcmd.com_list:CommonAdd',# getPredictResult 获取结果
            'job getInputParameterSample =aimaxcmd.com_list:CommonShow',# getInputParameterSample 模型部署时 测试
            'job generateImageFromContainer =aimaxcmd.com_list:CommonAdd',# generateImageFromContainer 获取结果
            'job getJobSaveImgInfo =aimaxcmd.com_list:CommonShow',# getJobSaveImgInfo 获取任务镜像信息
            'job getJobLog =aimaxcmd.com_list:CommonShow',# getJobLog 获取任务信息
            'job unschedule =aimaxcmd.com_list:CommonPut',# unschedule 取消定时任务
            'job getNodeTaintStatus =aimaxcmd.com_list:CommonShow',# getNodeTaintStatus
            'job schedule =aimaxcmd.com_list:CommonPut',# schedule 定时任务
            'job listPods =aimaxcmd.com_list:CommonShow',# listPods 测试用的接口
            'job getNodeAllocatable =aimaxcmd.com_list:CommonShow',# getNodeAllocatable 未找到controller的实现
            #=======JobProxyImpl end============================================

            #=======MonitorProxyImpl begin============================================
            'monitor getNodeDockers =aimaxcmd.com_list:CommonShow',# getNodeDockers 获取节点的docker
            'monitor getNodeHistory =aimaxcmd.com_list:CommonShow',# getNodeHistory 获取节点历史
            'monitor getNodeInfo =aimaxcmd.com_list:CommonShow',# getNodeInfo 获取节点信息
            'monitor getNodeItem =aimaxcmd.com_list:CommonShow',# getNodeItem 获取节点信息item
            'monitor getClusterHistory =aimaxcmd.com_list:CommonShow',# getClusterHistory 获取监控历史
            'monitor getClusterHealth =aimaxcmd.com_list:CommonShow',# getClusterHealth 获取集群健康
            'monitor getClusterItem =aimaxcmd.com_list:CommonShow',# getClusterItem 获取集群健康
            'monitor getJobHistory =aimaxcmd.com_list:CommonShow',# getJobHistory 获取任务历史
            'monitor getJobInfo =aimaxcmd.com_list:CommonShow',# getJobInfo 获取任务信息
            'monitor getJobSummery =aimaxcmd.com_list:CommonShow',# getJobSummery 获取任务summery
            'monitor getNodeDashboard =aimaxcmd.com_list:CommonShow',# getNodeDashboard 获取任务仪表
            'monitor getNamespaceDashboard =aimaxcmd.com_list:CommonShow',# getNamespaceDashboard 获取命名空间仪表
            'monitor getReportTnterval =aimaxcmd.com_list:CommonShow',# getReportTnterval 获取报告
            'monitor getReportHistory =aimaxcmd.com_list:CommonShow',# getReportHistory 获取报告
            #=======MonitorProxyImpl end============================================

            #=======NodeProxyImpl begin============================================
            'node overview = aimaxcmd.cmds_node:NodeOverview',# getNodeOverview
            'node add = aimaxcmd.cmds_node:NodeAdd',# autoAddNode
            'node delete = aimaxcmd.cmds_node:NodeDelete',# removeSingleNode
            'node poweron = aimaxcmd.cmds_node:PowerOn',# powerOn
            'node poweroff = aimaxcmd.cmds_node:PowerOff',# powerOff
            'node reset = aimaxcmd.cmds_node:PowerReset',# powerReset
            'node tag = aimaxcmd.cmds_node:NodeTag',# updateNode
            #=======NodeProxyImpl end============================================

            #=======StorageProxyImpl begin============================================
            'storage createVolumes =aimaxcmd.com_list:CommonAdd',# createVolumes
            'storage createNFSVolumes =aimaxcmd.com_list:CommonAdd',# createNFSVolumes 创建NFS卷
            'storage listDirs =aimaxcmd.com_list:CommonList',# listDirs 获取共享对象
            'storage getFileInfo =aimaxcmd.com_list:CommonShow',# getFileInfo 获取共享数据
            'storage getVolumeInfo =aimaxcmd.com_list:CommonList',# getVolumeInfo 获取卷信息
            'storage getPrivateVol =aimaxcmd.com_list:CommonShow',# getPrivateVol 获取共享数据
            'storage createFolder =aimaxcmd.com_list:CommonAdd',# createFolder 创建文件夹
            'storage deleteDirs =aimaxcmd.com_list:CommonDelete',# deleteDirs
            'storage uploadvolumes =aimaxcmd.com_list:CommonUpload',# upload 更新卷
            'storage downloadvolumes =aimaxcmd.com_list:CommonDownload',# download 下载 目前前台使用 FTP 直接获取 不走api
            'storage downloadBigFile =aimaxcmd.com_list:CommonDownload',# downloadBigFile 下载
            'storage zipFolder =aimaxcmd.com_list:CommonDownload',# zipFolder 下载
            'storage unzipFolder =aimaxcmd.com_list:CommonPut',# unzipFolder 下载
            'storage progress =aimaxcmd.com_list:CommonShow',# progress 查询下载的的进度
            'storage copyData =aimaxcmd.com_list:CommonShow',# copyData 复制
            'storage moveData =aimaxcmd.com_list:CommonShow',# moveData 移动
            # listBricks # gluster转块 暂不实现
            'storage listVolumes =aimaxcmd.com_list:CommonList',# listVolumes
            'storage listNFSVolumes =aimaxcmd.com_list:CommonPut',# listNFSVolumes 获取NFS卷
            'storage getJobFileLocation =aimaxcmd.com_list:CommonShow',# getJobFileLocation 获取
            'storage shareData =aimaxcmd.com_list:CommonAdd',# shareData 分享数据
            'storage getShareData =aimaxcmd.com_list:CommonShow',# getShareData 获取共享数据
            'storage getMyShareData =aimaxcmd.com_list:CommonShow',# getMyShareData 获取共享数据
            'storage cancleShareData =aimaxcmd.com_list:CommonDelete',# cancelShare 取消分享
            'storage copyShareData =aimaxcmd.com_list:CommonShow',# copyShareData 获取共享数据
            'storage getShareObjs =aimaxcmd.com_list:CommonShow',# getShareObjs 获取共享数据
            'storage getDecompressInfo =aimaxcmd.com_list:CommonShow',# getDecompressInfo 获取共享数据
            'storage getShareDataOpInfo =aimaxcmd.com_list:CommonShow',# getShareDataOpInfo 获取共享数据
            # expandeVolume : # gluster转块 暂不实现
            'storage rename =aimaxcmd.com_list:CommonPut',# rename 重命名
            'storage cancelDecompress =aimaxcmd.com_list:CommonShow',# cancelDecompress 获取共享数据
            'storage chmodFile =aimaxcmd.com_list:CommonPut',# setFilePermission 设置权限
            'storage createUserFolder =aimaxcmd.com_list:CommonAdd',# createUserFolder 创建用户文件夹
            'storage updateVolumeQuota =aimaxcmd.com_list:CommonPut',# updateVolumeQuota 更新卷用量
            'storage tagDeletedForHomeDir =aimaxcmd.com_list:CommonDelete',# tagDeletedForHomeDir 删除目录
            #=======StorageProxyImpl end============================================

            #=======TemplateProxyImpl begin============================================
            'job createTemplate =aimaxcmd.com_list:CommonAdd',# createTemplate 创建模板
            'job getTemplate =aimaxcmd.com_list:CommonShow',# getTemplate 获取模板
            'job delTemplate =aimaxcmd.com_list:CommonDelete',# delTemplate 删除模板 软删除 只是改了状态位0变1
            'job updateTemplate =aimaxcmd.com_list:CommonPut',# updateTemplate 更新模板
            'job getTemplateList =aimaxcmd.com_list:CommonList',# getTemplateList 获取模板列表
            #=======TemplateProxyImpl end============================================

            #=======UserProxyImpl begin============================================
            'user list = aimaxcmd.cmds_user:UserList',# listAllUsers
            'user info = aimaxcmd.cmds_user:UserInfo',# getUserByName
            'user getViewGroups = aimaxcmd.com_list:CommonShow',# getViewGroups
            'user getUserById = aimaxcmd.com_list:CommonShow',# getUserById
            'users add = aimaxcmd.cmds_user:UserAdds',# addUser 增加用户
            'user addHarborUser = aimaxcmd.com_list:CommonAdd',# addUser 增加harbor用户
            'user add = aimaxcmd.com_list:CommonAdd',# addUser 增加用户
            'user updateHarborUser = aimaxcmd.com_list:CommonAdd',# updateUser 更新harbor用户
            'user update = aimaxcmd.com_list:CommonAdd',# updateUser 更新用户
            'user resetUserPassword = aimaxcmd.com_list:CommonPut',# resetUserPassword 增加用户
            'user delHarborUser = aimaxcmd.com_list:CommonDelete',# updateUser 更新用户
            'user deleteUser = aimaxcmd.com_list:CommonDelete',# resetUserPassword 增加用户
            # checkPassword web端 客戶端暂不需要
            #=======UserProxyImpl end============================================

            #=======UserQuotaProxyImpl begin============================================
            'userQuota get = aimaxcmd.com_list:CommonShow',# getUserQuotaByUserId
            'userQuota update = aimaxcmd.com_list:CommonPut',# updateUserQuota
            #resetGpuUsed 内部调用无需实现
            'user quotas = aimaxcmd.com_list:CommonAdd',# addQuota
            #=======UserQuotaProxyImpl end============================================

            #=======VisualProxyImpl begin============================================
            'job getVisualInfoList =aimaxcmd.com_list:CommonList',# getList 根据用户和任务名获取可视化任务
            #TODO getEntity
            'job visualForCaffe =aimaxcmd.com_list:CommonShow',# getVisualForCaffe
            'job removeVisual =aimaxcmd.com_list:CommonDelete',# removeEntity 删除visual
            'job getCaffeEntity =aimaxcmd.com_list:CommonShow',# getCaffeEntity 获取caffe
            #TODO getVisdomEntity
            #=======VisualProxyImpl begin============================================

            #=======ZoneProxyImpl begin============================================
            'zone list =aimaxcmd.com_list:CommonList',# listAllZones
            'zone get =aimaxcmd.com_list:CommonShow',# getZoneByName
            'zone add =aimaxcmd.com_list:CommonAdd',# addZone
            'zone update =aimaxcmd.com_list:CommonPut',# updateZone
            'zone del =aimaxcmd.com_list:CommonDelete',# deleteZone
            #=======ZoneProxyImpl end============================================



            'user getgpuList =aimaxcmd.com_list:CommonList',#创建用户前 获取 gpu类型列表
            #'zone list = aimaxcmd.cmds_zone:NodeList',#
            #'zone info = aimaxcmd.cmds_node:NodeInfo',#

            'image repositoriesByprojectId =aimaxcmd.com_list:CommonList',# 根据用户获取镜像
            'image getImagesByProjectId =aimaxcmd.com_list:CommonList',# 根据项目id获取镜像
            'job visualForTensorflow =aimaxcmd.com_list:CommonShow',# getVisualForCaffe

            'list = aimaxcmd.com:CommonList',#get 17
            'put = aimaxcmd.com:CommonPut',#put 13
            'add = aimaxcmd.com:CommonAdd',#post 6
            #'creat = aimaxcmd.com:CommonAdd',#post
            'post = aimaxcmd.com:CommonAdd',# 11
            'del = aimaxcmd.com:CommonDelete',#del 11
            'get = aimaxcmd.com:CommonShow',#get 40
            'upload = aimaxcmd.com:CommonUpload',#post 3
            'download = aimaxcmd.com:CommonDownload',#get 3
            #'cmdimage list = aimaxcmd.cmds_image:CommonList',#

            'json = aimaxcmd.com:CommonDownload',#get 3
        ],

        'cliff.demo.hooked': [
            'sample-hook = cliffdemo.hook:Hook',
        ],
    },

    zip_safe=False,
)
