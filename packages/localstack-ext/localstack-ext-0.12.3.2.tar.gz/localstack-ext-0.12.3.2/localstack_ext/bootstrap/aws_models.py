from localstack.utils.aws import aws_models
dfQVx=super
dfQVs=None
dfQVo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  dfQVx(LambdaLayer,self).__init__(arn)
  self.cwd=dfQVs
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.dfQVo.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,dfQVo,env=dfQVs):
  dfQVx(RDSDatabase,self).__init__(dfQVo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,dfQVo,env=dfQVs):
  dfQVx(RDSCluster,self).__init__(dfQVo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,dfQVo,env=dfQVs):
  dfQVx(AppSyncAPI,self).__init__(dfQVo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,dfQVo,env=dfQVs):
  dfQVx(AmplifyApp,self).__init__(dfQVo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,dfQVo,env=dfQVs):
  dfQVx(ElastiCacheCluster,self).__init__(dfQVo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,dfQVo,env=dfQVs):
  dfQVx(TransferServer,self).__init__(dfQVo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,dfQVo,env=dfQVs):
  dfQVx(CloudFrontDistribution,self).__init__(dfQVo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,dfQVo,env=dfQVs):
  dfQVx(CodeCommitRepository,self).__init__(dfQVo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
