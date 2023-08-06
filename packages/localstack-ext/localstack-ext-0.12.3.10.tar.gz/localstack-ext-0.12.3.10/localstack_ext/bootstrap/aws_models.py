from localstack.utils.aws import aws_models
TOhcP=super
TOhcM=None
TOhck=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TOhcP(LambdaLayer,self).__init__(arn)
  self.cwd=TOhcM
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TOhck.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TOhck,env=TOhcM):
  TOhcP(RDSDatabase,self).__init__(TOhck,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TOhck,env=TOhcM):
  TOhcP(RDSCluster,self).__init__(TOhck,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TOhck,env=TOhcM):
  TOhcP(AppSyncAPI,self).__init__(TOhck,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TOhck,env=TOhcM):
  TOhcP(AmplifyApp,self).__init__(TOhck,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TOhck,env=TOhcM):
  TOhcP(ElastiCacheCluster,self).__init__(TOhck,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TOhck,env=TOhcM):
  TOhcP(TransferServer,self).__init__(TOhck,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TOhck,env=TOhcM):
  TOhcP(CloudFrontDistribution,self).__init__(TOhck,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TOhck,env=TOhcM):
  TOhcP(CodeCommitRepository,self).__init__(TOhck,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
