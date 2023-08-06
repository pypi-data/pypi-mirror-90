from localstack.utils.aws import aws_models
Oupmg=super
OupmM=None
Oupmc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Oupmg(LambdaLayer,self).__init__(arn)
  self.cwd=OupmM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Oupmc.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Oupmc,env=OupmM):
  Oupmg(RDSDatabase,self).__init__(Oupmc,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Oupmc,env=OupmM):
  Oupmg(RDSCluster,self).__init__(Oupmc,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Oupmc,env=OupmM):
  Oupmg(AppSyncAPI,self).__init__(Oupmc,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Oupmc,env=OupmM):
  Oupmg(AmplifyApp,self).__init__(Oupmc,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Oupmc,env=OupmM):
  Oupmg(ElastiCacheCluster,self).__init__(Oupmc,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Oupmc,env=OupmM):
  Oupmg(TransferServer,self).__init__(Oupmc,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Oupmc,env=OupmM):
  Oupmg(CloudFrontDistribution,self).__init__(Oupmc,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Oupmc,env=OupmM):
  Oupmg(CodeCommitRepository,self).__init__(Oupmc,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
