from localstack.utils.aws import aws_models
OhPEe=super
OhPEB=None
OhPEK=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  OhPEe(LambdaLayer,self).__init__(arn)
  self.cwd=OhPEB
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.OhPEK.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,OhPEK,env=OhPEB):
  OhPEe(RDSDatabase,self).__init__(OhPEK,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,OhPEK,env=OhPEB):
  OhPEe(RDSCluster,self).__init__(OhPEK,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,OhPEK,env=OhPEB):
  OhPEe(AppSyncAPI,self).__init__(OhPEK,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,OhPEK,env=OhPEB):
  OhPEe(AmplifyApp,self).__init__(OhPEK,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,OhPEK,env=OhPEB):
  OhPEe(ElastiCacheCluster,self).__init__(OhPEK,env=env)
class TransferServer(BaseComponent):
 def __init__(self,OhPEK,env=OhPEB):
  OhPEe(TransferServer,self).__init__(OhPEK,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,OhPEK,env=OhPEB):
  OhPEe(CloudFrontDistribution,self).__init__(OhPEK,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,OhPEK,env=OhPEB):
  OhPEe(CodeCommitRepository,self).__init__(OhPEK,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
