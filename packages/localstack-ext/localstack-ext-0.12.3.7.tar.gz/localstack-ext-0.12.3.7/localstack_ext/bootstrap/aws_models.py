from localstack.utils.aws import aws_models
kBFWi=super
kBFWe=None
kBFWc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  kBFWi(LambdaLayer,self).__init__(arn)
  self.cwd=kBFWe
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.kBFWc.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,kBFWc,env=kBFWe):
  kBFWi(RDSDatabase,self).__init__(kBFWc,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,kBFWc,env=kBFWe):
  kBFWi(RDSCluster,self).__init__(kBFWc,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,kBFWc,env=kBFWe):
  kBFWi(AppSyncAPI,self).__init__(kBFWc,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,kBFWc,env=kBFWe):
  kBFWi(AmplifyApp,self).__init__(kBFWc,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,kBFWc,env=kBFWe):
  kBFWi(ElastiCacheCluster,self).__init__(kBFWc,env=env)
class TransferServer(BaseComponent):
 def __init__(self,kBFWc,env=kBFWe):
  kBFWi(TransferServer,self).__init__(kBFWc,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,kBFWc,env=kBFWe):
  kBFWi(CloudFrontDistribution,self).__init__(kBFWc,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,kBFWc,env=kBFWe):
  kBFWi(CodeCommitRepository,self).__init__(kBFWc,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
