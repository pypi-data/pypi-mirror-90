from localstack.utils.aws import aws_models
pQRWu=super
pQRWo=None
pQRWe=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  pQRWu(LambdaLayer,self).__init__(arn)
  self.cwd=pQRWo
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.pQRWe.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,pQRWe,env=pQRWo):
  pQRWu(RDSDatabase,self).__init__(pQRWe,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,pQRWe,env=pQRWo):
  pQRWu(RDSCluster,self).__init__(pQRWe,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,pQRWe,env=pQRWo):
  pQRWu(AppSyncAPI,self).__init__(pQRWe,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,pQRWe,env=pQRWo):
  pQRWu(AmplifyApp,self).__init__(pQRWe,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,pQRWe,env=pQRWo):
  pQRWu(ElastiCacheCluster,self).__init__(pQRWe,env=env)
class TransferServer(BaseComponent):
 def __init__(self,pQRWe,env=pQRWo):
  pQRWu(TransferServer,self).__init__(pQRWe,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,pQRWe,env=pQRWo):
  pQRWu(CloudFrontDistribution,self).__init__(pQRWe,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,pQRWe,env=pQRWo):
  pQRWu(CodeCommitRepository,self).__init__(pQRWe,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
