from localstack.utils.aws import aws_models
TObDq=super
TObDf=None
TObDe=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TObDq(LambdaLayer,self).__init__(arn)
  self.cwd=TObDf
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TObDe.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TObDe,env=TObDf):
  TObDq(RDSDatabase,self).__init__(TObDe,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TObDe,env=TObDf):
  TObDq(RDSCluster,self).__init__(TObDe,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TObDe,env=TObDf):
  TObDq(AppSyncAPI,self).__init__(TObDe,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TObDe,env=TObDf):
  TObDq(AmplifyApp,self).__init__(TObDe,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TObDe,env=TObDf):
  TObDq(ElastiCacheCluster,self).__init__(TObDe,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TObDe,env=TObDf):
  TObDq(TransferServer,self).__init__(TObDe,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TObDe,env=TObDf):
  TObDq(CloudFrontDistribution,self).__init__(TObDe,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TObDe,env=TObDf):
  TObDq(CodeCommitRepository,self).__init__(TObDe,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
